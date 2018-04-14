from api.cursor_api import *

def get_top_players_by_level():
    results = _top_players_by_level()

    return HttpResponse(json.dumps(results), content_type='application/json')

def _top_players_by_level():
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
        ORDER BY level DESC
        LIMIT 5;
        """

        cursor.execute(query)
        results = dictfetchall(cursor)

    return results