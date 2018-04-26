from api.cursor_api import *
from django.db import connection
from django.http import HttpResponse
from ..models import *
import json
from .queue_call import get_parties_by_playtime, dequeue_party_to_court_call

"""
    FUNCTIONS: (*) = not sure if works, look at this later
    
    edit_match(id, score_a, score_b) returns an http response
    join_match(match_id, member_id, team) returns an http response
    leave_match(match_id, member_id) returns an http response
    delete_match(id) returns an http response
    create_match(a_players, b_players, court_id) returns an http response
    find_current_match_by_member(id) returns an http response
    finish_match(id, scoreA, scoreB) returns an http response
    (* HAVEN'T TESTED PROPERLY YET) dequeue_next_party_to_court(queue_type, court_id) returns an http response
    get_top_players() returns an http response
    get_match(id) returns an http response
    get_all_matches() returns an http response
    
    _get_winners(match) returns a list of winners (Member objects)
    (* SHOULD THIS RETURN AN HTTP RESPONSE) _reward_winning_team(match_id, winning_team, points) returns an http response
    _get_parent_node(tournament_id, curr_level, index) returns BracketNode object
    _top_players() returns a dictionary
    _all_matches() returns a RawQuerySet of Match objects
    _players(match_id, team) returns a RawQuerySet of Interested objects(?)
    _num_players_in_match(id) returns an integer
    _is_finished_match(id) returns a boolean
    _is_tournament_match(id) returns a Tournament object or None
    _is_ranked_match(id) returns a boolean
    _get_bracket_node_and_level(id, tournament_id) returns a BracketNode object and the level of the BracketNode
"""

def edit_match(id, score_a, score_b):
    query = """
    UPDATE api_match SET scoreA = %s, scoreB = %s WHERE id = %s
    """
    response = run_connection(query, score_a, score_b, id)

    return response


def join_match(match_id, member_id, team):
    """
        Given a match ID and member_id, add the member to the match (by adding playedin)
    :param id:
    :return:
    """

    if _num_players_in_match(match_id) == 4:
        return http_response({}, message="Cannot join this match, there are already 4 people in it!", code=400)

    current_match = find_current_match_by_member(member_id)
    if current_match.status_code == 200:
        return http_response({}, message="Member is already in a match", code=400)

    if _is_finished_match(match_id):
        return http_response({}, message="Cannot join a finished match", code=400)

    member = list(Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s", [member_id]))[0]
    if member.party_id is not None:
        return http_response({}, message="Member is already in a party. Can only join matches if alone.", code=400)

    query = "INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)"
    response = run_connection(query, member_id, team, match_id)

    return response


def leave_match(match_id, member_id):
    """
        Given a match id and member id, let the member leave a match
    :param match_id:
    :param member_id:
    :return:
    """
    match_id = int(match_id)
    #if there's only one player in the match
    players = list(_players(match_id))
    found = 0
    for player in players:
        if player.id == member_id:
            found = 1

    if _num_players_in_match(match_id) == 1 and found == 1:
        run_connection("DELETE FROM api_playedin WHERE member_id=%s AND match_id=%s", member_id, match_id)
        return delete_match(match_id)

    if _is_finished_match(match_id):
        return http_response({}, message="Cannot leave a finished match", code=400)

    if found == 1:
        response = run_connection("DELETE FROM api_playedin WHERE member_id=%s AND match_id=%s", member_id, match_id)
        return response
    else:
        return http_response({}, message="Cannot leave a match you're not part of!", code=400)


def delete_match(id):
    """
        Delete a match, as well as the playedin relationship. Update the court relationship
    :param id:
    :return:
    """
    query = "UPDATE api_court SET match_id = NULL WHERE match_id=%s"
    run_connection(query, id)

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


def create_match(a_players, b_players, court_id):
    """
        Create a new match! Should only be used by queues
    :param a_players:
    :param b_players:
    :param court_id:
    :return:
    """
    with connection.cursor() as cursor:
        query = """
        SELECT COALESCE(MAX(id)+1, 0) AS newID
        FROM api_match
        """
        result = cursor.execute(query)
        newID = dictfetchall(cursor)[0]['newID']


    query = """
    INSERT INTO api_match(id, startDateTime, scoreA, scoreB) VALUES (%s, %s, 0, 0)
    """
    today = datetime.datetime.now()
    response = run_connection(query, newID, serializeDateTime(today))

    query = """
    UPDATE api_court SET match_id = %s WHERE id = %s
    """
    response = run_connection(query, newID, court_id)


    for p in a_players:
        # It seems to be passed as a list of int strings rather than just ints
        p = int(p)
        query = """
        INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)
        """
        response = run_connection(query, p, "A", newID)

    for p in b_players:
        p = int(p)
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
        query = '''SELECT * FROM api_match, api_playedin
        WHERE api_playedin.member_id=%s AND api_match.id=api_playedin.match_id AND api_match.endDateTime IS NULL
        '''

        cursor.execute(query, [id])
        result = dictfetchone(cursor)

        if result:
            match_id = result["match_id"]
            cursor.execute("SELECT * FROM api_playedin JOIN api_interested ON api_playedin.member_id = api_interested.id WHERE match_id=%s", [match_id])
            people = dictfetchall(cursor)
            if len(list(people)) <= 0:
                return http_response({}, message="Oops... this shouldn't happen!", code=400)

            teamA = []
            teamB = []
            for person in people:
                obj = {"name":person['first_name'] + ' ' + person['last_name'], "id": person['member_id'] }
                if person['team'] == "A":
                    teamA.append(obj)
                else:
                    teamB.append(obj)

            match_json = {'status':'playing', "match": {"match_id": match_id, "scoreA": result["scoreA"],
                                            "scoreB": result["scoreB"], "teamA": teamA, "teamB": teamB}}
            return http_response(match_json)
        else:
            return http_response({'status':'idle'}, message="Couldn't find a current match for this member. Are you sure this member is in a match?")


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
        Ends the match, updates the scores, removes court id. Also increases the level of
        all members of the winning team by 10.
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
    court_query = Court.objects.raw("SELECT * FROM api_court WHERE match_id = %s", [match.id])
    if len(list(court_query)) > 0:
        court = court_query[0]
        court_id = court.id
    else:
        court_id = None


    #check to make sure match should actually be finished
    if not (abs(match.scoreA - match.scoreB) >= 2) and not((match.scoreB >= 21 or match.scoreA >= 21)):
        return http_response(message='Violating win by 2 rule or at least one player having at least 21 points',
                             code=400)

    #check if this match is a ranked match
    if _is_ranked_match(id):
        # Reward the winners by giving 10 points to their level
        winning_team = "A" if scoreA > scoreB else "B"
        _reward_winning_team(match.id, winning_team, 10)

    today = datetime.datetime.now()
    serializedDate = serializeDateTime(today)
    query = "UPDATE api_match SET endDateTime=%s WHERE id=%s"

    response = run_connection(query, serializedDate, id)
    if response.status_code == 400:
        return http_response(message='Cannot update end date time!', code=400)

    # Check if this match belongs to a tournament. If so, we may need to update the tournament too
    tournament_id = _is_tournament_match(match.id)
    if tournament_id is not None:
        bracket_node, level = _get_bracket_node_and_level(match.id, tournament_id)
        if level > 0:
            index = bracket_node.sibling_index
            index_of_sibling = index + 1 if index % 2 == 0 else index - 1

            # See if sibling exists
            bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND level = %s AND sibling_index = %s", [tournament_id, level, index_of_sibling])
            if len(list(bracket_nodes)) > 0:
                bracket_node_sibling = bracket_nodes[0]

                sibling_match = bracket_node_sibling.match
                if sibling_match is not None and sibling_match.endDateTime is not None:
                    # We must add a match to the parent node!
                    parent_node = _get_parent_node(tournament_id, level, index)
                    if parent_node.match is None:
                        # new_match = Match(startDateTime=datetime.datetime.now(), scoreA=0, scoreB=0)
                        # new_match.save()

                        winners_of_match = _get_winners(match)
                        winners_of_sibling_match = _get_winners(sibling_match)

                        new_match = create_match(score_a=0, score_b=0, a_players=winners_of_match,
                                                 b_players=winners_of_sibling_match)
                        if new_match.status_code != 200:
                            return http_response('Could not create new match properly!', code=400)

                        response = run_connection("UPDATE api_bracketnode SET match_id = %s WHERE id = %s", new_match.id, parent_node.id)
            else:
                # there's no sibling and it's not the 0 level, which shouldn't exist - return error
                return http_response('Could not find a sibling for your match!', code=400)


    #put the next match on the court
    if court_id is not None:
        court = Court.objects.raw("SELECT * FROM api_court WHERE id = %s", [court_id])[0]
        queue = court.queue

        # Remove the finished match from the court before dequeueing
        remove_match_response = run_connection("UPDATE api_court SET match_id = NULL WHERE id = %s", court_id)

        if queue is not None:
            dequeue_resp = dequeue_party_to_court_call(queue.type)

    return response


def _reward_winning_team(match_id, winning_team, points):
    """
        Give the winning team ("A" or "B") of the match points.
    :param match_id:
    :param winning_team:
    :param points:
    :return:
    """
    query = """
    UPDATE api_member
    SET level=level+%s
    WHERE interested_ptr_id IN 
    (SELECT m.interested_ptr_id 
    FROM api_member AS m, api_playedin AS plin, api_match
    WHERE m.interested_ptr_id=plin.member_id AND plin.match_id=%s AND plin.team=%s)
    """
    return run_connection(query, points, match_id, winning_team)

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
            api_interested.last_name AS last_name,
            member.level AS level
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


def _players(match_id, team=None):
    if team is None:
        query = '''
        SELECT * FROM api_interested, api_playedin WHERE api_playedin.match_id=%s
        AND api_playedin.member_id=api_interested.id
        '''

        players = Interested.objects.raw(query, [match_id])

    else:
        query = """
        SELECT * 
        FROM api_interested, api_playedin 
        WHERE api_playedin.match_id = %s AND api_playedin.member_id = api_interested.id
          AND api_playedin.team = %s
        """

        players = Interested.objects.raw(query, [match_id, team])

    return players


def _num_players_in_match(id):
    """
        Given a match id, return the number of players in the match
    :param id:
    :return:
    """

    players = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id=%s", [id])
    return len(list(players))


def _is_finished_match(id):
    """
        Given a match id, return whether the match is finished or not
    :param id:
    :return:
    """

    match = Match.objects.raw("SELECT * FROM api_match WHERE id=%s", [id])
    if len(list(match)) > 0:
        match = match[0]
        if match.endDateTime is None:
            return False
        else:
            return True

    return False


def _is_tournament_match(id):
    """
        Given a match id, return tournament it's part of
        if it's not part of a tournament, return None
    :param id:
    :return:
    """
    match_query = Match.objects.raw("SELECT * FROM api_match WHERE id = %s", [id])
    if len(list(match_query)) > 0:
        match = match_query[0]
        bracket_node = match.bracket_node
        if bracket_node is None:
            return None
        tournament = bracket_node.tournament
        return tournament
    return None

def _is_ranked_match(id):
    """
        Given a match id, return True if it's a ranked match, False if not
    :param id:
    :return:
    """
    match_court = Match.objects.raw("SELECT * FROM api_match WHERE api_match.id=%s", [id])
    if len(list(match_court)) > 0:
        match = match_court[0]
        courts = Court.objects.raw("SELECT * FROM api_court WHERE match_id=%s", [match.id])
        if (len(list(courts))) > 0:
            court = courts[0]
            queues = Queue.objects.raw("SELECT * FROM api_queue WHERE api_queue.id=%s", [court.queue_id])
            if (len(list(queues))) > 0:
                queue = queues[0]
                if queue.type == "RANKED":
                    return True

    return False

def _get_bracket_node_and_level(id, tournament_id):
    """
        Given a match id and tournament id, get the match's bracket node and level
    :param id:
    :return:
    """

    if _is_tournament_match(id):
        bracket_nodes = BracketNode.objects.raw(
            "SELECT * FROM api_bracketnode WHERE tournament_id = %s AND match_id IS NOT NULL AND match_id = %s",
            [tournament_id, id])
        if len(list(bracket_nodes)) > 0:
            bracket_node = bracket_nodes[0]
            level = bracket_node.level

            return bracket_node, level
    else:
        return None

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