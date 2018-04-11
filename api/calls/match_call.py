from api.cursor_api import *
from django.db import connection
from django.http import HttpResponse
from ..models import *
import json
from .queue_call import get_parties_by_playtime


def edit_match(id, score_a, score_b):
    query = """
    UPDATE api_match SET scoreA = %s, scoreB = %s WHERE id = %s
    """
    response = run_connection(query, score_a, score_b, id)

    return response


def delete_match(id):
    playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s", [id])
    for p in playedins:
        query = """
            DELETE FROM api_playedin 
            WHERE id = %s
            """
        response = run_connection(query, p.pk)

    query = """
    DELETE FROM api_match WHERE id = %s
    """
    response = run_connection(query, id)
    return response


def create_match(score_a, score_b, a_players, b_players):
    with connection.cursor() as cursor:
        query = """
        SELECT MAX(id)
        FROM api_match
        """
        result = cursor.execute(query)
        if not result:
            newID = result[0] + 1
        else:
            newID = 0


    query = """
    INSERT INTO api_match(id, startDateTime, scoreA, scoreB) VALUES (%s, %s, %s, %s)
    """
    today = datetime.datetime.now()
    response = run_connection(query, newID, serializeDateTime(today), score_a, score_b)
    for p in a_players:
        query = """
        INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)
        """
        response = run_connection(query, p, "A", newID)

    for p in b_players:
        query = """
           INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)
           """
        response = run_connection(query, p, "B", newID)

    return response


def find_current_match_by_member(id):
    """
        Finds the match the member with given id is in
        returns match id
    :param id:
    :return:
    """
    with connection.cursor() as cursor:
        query = '''SELECT api_match.id AS match_id FROM api_match, api_playedin
        WHERE api_playedin.member_id=%s AND api_match.id=api_playedin.match_id AND api_match.endDateTime IS NULL
        '''

        cursor.execute(query, [id])
        result = dictfetchone(cursor)
        if result:
            return http_response({"match_id": result["match_id"]})
        else:
            return http_response({}, message="Couldn't find a current match for this member. Are you sure this member is in a match?",
                                 code=400)


def _get_winners(match):
    """
        Returns a list of the team of winners
    :param match:
    :return:
    """
    if match.scoreA > match.scoreB:
        playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'A'", [match.id])
    else:
        playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'B'", [match.id])

    winners = []
    for playedin in playedins:
        member = playedin.member
        winners.append(member)

    return winners

def finish_match(id, scoreA, scoreB):
    """
        Ends the match, updates the scores, removes court id
    :param id:
    :param scoreA:
    :param scoreB:
    :return:
    """

    # Check that the match exists
    matches = Match.objects.raw("SELECT * FROM api_match WHERE id = %s", [id])
    if len(list(matches)) <= 0:
        return http_response(message='No such match', code=400)

    resp = edit_match(id, scoreA, scoreB)
    if resp.status_code == 400:
        return http_response(message='There was an error updating your scores!', code=400)

    match = matches[0]
    court_id = match.court_id
    if abs(match.scoreA - match.scoreB) >= 2 and (match.scoreB >= 21 or match.scoreA >= 21):
        query = '''
            UPDATE api_match SET court_id=NULL, endDateTime=datetime('now') WHERE api_match.id=%s
            '''

        response = run_connection(query, id)

        # Check if this match belongs to a tournament. If so, we may need to update the tournament too
        tournaments = Tournament.objects.raw("SELECT * FROM api_tournament WHERE endDate IS NULL")
        if len(list(tournaments)) > 0:
            tournament = tournaments[0]
            bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND match_id IS NOT NULL AND match_id = %s", [tournament.id, match.id])
            if len(list(bracket_nodes)) > 0:
                bracket_node = bracket_nodes[0]
                level = bracket_node.level
                if level > 0:
                    index = bracket_node.sibling_index
                    index_of_sibling = index + 1 if index % 2 == 0 else index - 1

                    # See if sibling exists
                    bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND level = %s AND sibling_index = %s", [tournament.id, level, index_of_sibling])
                    if len(list(bracket_nodes)) > 0:
                        bracket_node_sibling = bracket_nodes[0]

                        sibling_match = bracket_node_sibling.match
                        if sibling_match is not None and sibling_match.endDateTime is not None:
                            # We must add a match to the parent node!
                            parent_node = _get_parent_node(tournament.id, level, index)
                            if parent_node.match is None:
                                # new_match = Match(startDateTime=datetime.datetime.now(), scoreA=0, scoreB=0)
                                # new_match.save()

                                winners_of_match = _get_winners(match)
                                winners_of_sibling_match = _get_winners(sibling_match)

                                new_match = create_match(scoreA=0, scoreB=0, a_players=winners_of_match,
                                                         b_players=winners_of_sibling_match)
                                if new_match.status_code != 200:
                                    return http_response('Could not create new match properly!', code=400)

                                response = run_connection("UPDATE api_bracketnode SET match_id = %s WHERE id = %s", new_match.id, parent_node.id)
                    else:
                        # there's no sibling and it's not the 0 level, which shouldn't exist - return error
                        return http_response('Could not find a sibling for your match!', code=400)

        #put the next match on the court
        court = Court.objects.raw("SELECT * FROM api_court WHERE id=%s AND queue_id IS NOT NULL")

        if len(list(court)) > 0:
            #that means it has a queue id
            queue = Queue.objects.raw("SELECT * FROM api_queue WHERE id=%s", court.queue_id)
            dequeue_resp = dequeue_next_party_to_court(queue.type, court.id)

            if dequeue_resp.message == 'No parties on this queue':
                return http_response(message='No parties on this queue')


        return response
    else:
        return http_response(message='Violating win by 2 rule or at least one player having at least 21 points', code=400)


def dequeue_next_party_to_court(queue_type, court_id):

    response = get_parties_by_playtime(queue_type)
    my_json = json.loads(response.content.decode())
    parties = my_json['parties']
    if len(parties) == 0:
        return http_response({}, message='No parties on this queue', code=400)

    party_to_dequeue = parties[0]

    party_id = party_to_dequeue['party_id']

    queues = Queue.objects.raw("SELECT * FROM api_queue WHERE type = %s", [queue_type])
    if len(list(queues)) == 0:
        return http_response({}, message='No such queue found', code=400)

    queue = queues[0]

    # Get the members from the party
    members = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party_id])

    # Remove party from queue
    response = run_connection("DELETE FROM api_party WHERE id = %s", party_id)
    if response.status_code != 200:
        # Error
        return response

    # Create match on court

    a_players, b_players = []
    # Assign teams
    num_members = len(list(members))
    for i in range(num_members):
        team = "A" if i % 2 == 0 else "B"
        member = members[i]
        if team == "A":
            a_players.append(member)
        else:
            b_players.append(member)

    return create_match(scoreA=0, scoreB=0, a_players=a_players, b_players=b_players)

def _get_parent_node(tournament_id, curr_level, index):
    parent_index = index // 2
    bracket_nodes = BracketNode.objects.raw(
        "SELECT * FROM api_bracketnode WHERE tournament_id = %s AND level = %s AND sibling_index = %s",
        [tournament_id, curr_level - 1, parent_index])
    parent_node = bracket_nodes[0]
    return parent_node

def _top_players():
    with connection.cursor() as cursor:
        query = """
        SELECT 
            member.interested_ptr_id AS id, 
            COUNT(CASE WHEN 
                (playedin.team = 'A' AND match.scoreA > match.scoreB) OR
                (playedin.team = 'B' AND match.scoreB > match.scoreA) THEN 1 ELSE NULL END) AS wins, 
            COUNT(*) AS total_games,
            api_interested.first_name AS first_name,
            api_interested.last_name AS last_name
        FROM ((api_member AS member
          INNER JOIN api_playedin AS playedin ON member.interested_ptr_id = playedin.member_id)
          INNER JOIN api_match AS match ON match.id = playedin.match_id)
          INNER JOIN api_interested AS api_interested ON member.interested_ptr_id = api_interested.id
        WHERE member.private = 0
        GROUP BY member.interested_ptr_id
        ORDER BY wins * 1.0 / total_games DESC, total_games DESC 
        LIMIT 5;
        """

        cursor.execute(query)
        results = dictfetchall(cursor)

    return results

def get_top_players():
    results = _top_players()

    return HttpResponse(json.dumps(results), content_type='application/json')

def _all_matches():
    all_matches = Match.objects.raw("SELECT * FROM api_match")
    return all_matches

def _players(match_id, team):
    query = """
    SELECT * 
    FROM api_interested, api_playedin 
    WHERE api_playedin.match_id = %s AND api_playedin.member_id = api_interested.id
      AND api_playedin.team = %s
    """
    players = Interested.objects.raw(query, [match_id, team])
    return players

def get_match(id):
    query = Match.objects.raw("SELECT * FROM api_match WHERE id = %s", [id])
    match = query[0]
    a_players = _players(id, "A")
    b_players = _players(id, "B")

    ret = serializeModel(match)
    ret["A"] = serializeSetOfModels(a_players)
    ret["B"] = serializeSetOfModels(b_players)

    return HttpResponse(json.dumps(ret), content_type='applications/json')

def get_all_matches():
    all_matches = _all_matches()
    result = {}
    result["matches"] = []

    for match in all_matches:
        s = serializeModel(match)
        a_players = _players(match.id, "A")
        b_players = _players(match.id, "B")
        s["A"] = serializeSetOfModels(a_players)
        s["B"] = serializeSetOfModels(b_players)

        result["matches"].append(s)

    return HttpResponse(json.dumps(result), content_type='applications/json')