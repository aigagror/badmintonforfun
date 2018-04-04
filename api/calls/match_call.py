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
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            newID = result[0] + 1
        else:
            newID = 0


    query = """
    INSERT INTO api_match(id, startDate, scoreA, scoreB) VALUES (%s, %s, %s, %s)
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


def _top_players():
    with connection.cursor() as cursor:
        query = """
        SELECT member.interested_ptr_id AS email, COUNT(CASE WHEN (playedin.team = 'A' AND match.scoreA > match.scoreB) OR
                                                         (playedin.team = 'B' AND match.scoreB > match.scoreA) THEN 1 ELSE NULL END) AS wins, 
                                         COUNT(*) AS total_games
        FROM (api_member AS member
          INNER JOIN api_playedin AS playedin ON member.interested_ptr_id = playedin.member_id)
          INNER JOIN api_match AS match ON match.id = playedin.match_id
        GROUP BY member.interested_ptr_id
        ORDER BY wins * 1.0 / total_games DESC, total_games DESC LIMIT 5;
        """

        cursor.execute(query)
        results = dictfetchall(cursor)

    return results

def get_top_players():
    results = _top_players()
    for result in results:
        member = Interested.objects.raw("SELECT * FROM api_interested WHERE email = %s", [result['email']])[0]
        result["info"] = serializeModel(member)

    return HttpResponse(json.dumps(results), content_type='applications/json')

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