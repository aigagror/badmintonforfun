from api.cursor_api import *
from django.db import connection
from django.http import HttpResponse
from ..models import *
import json


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
    if match.scoreA > match.scoreB:
        playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'A'", [match.id])
    else:
        playedins = PlayedIn.objects.raw("SELECT * FROM api_playedin WHERE match_id = %s AND team = 'B'", [match.id])

    winners = []
    for playedin in playedins:
        member = playedin.member
        winners.append(member)

    return winners

def finish_match(id):
    """
        Ends the match, updates the scores, removes court id
    :param id:
    :param scoreA:
    :param scoreB:
    :return:
    """

    # Check that the scores are valid
    matches = Match.objects.raw("SELECT * FROM api_match WHERE id = %s", [id])
    if len(list(matches)) <= 0:
        return http_response(message='No such match', code=400)

    match = matches[0]
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
                            parent_index = index // 2
                            bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND level = %s AND sibling_index = %s", [tournament.id, level - 1, parent_index])
                            parent_node = bracket_nodes[0]
                            if parent_node.match is None:
                                new_match = Match(startDateTime=datetime.datetime.now(), scoreA=0, scoreB=0)
                                new_match.save()

                                winners_of_match = _get_winners(match)
                                winners_of_sibling_match = _get_winners(sibling_match)

                                for winner in winners_of_match:
                                    response = run_connection("INSERT INTO api_playedin(team, match_id, member_id) VALUES(%s, %s, %s)", "A", new_match.id, winner.id)
                                    if response.status_code != 200:
                                        return response

                                for winner in winners_of_sibling_match:
                                    response = run_connection("INSERT INTO api_playedin(team, match_id, member_id) VALUES(%s, %s, %s)", "B", new_match.id, winner.id)
                                    if response.status_code != 200:
                                        return response

                                response = run_connection("UPDATE api_bracketnode SET match_id = %s WHERE id = %s", new_match.id, parent_node.id)


        return response
    else:
        return http_response(message='Violating win by 2 rule or at least one player having at least 21 points', code=400)


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