from ..cursor_api import *
from django.db import connection
from django.http import HttpResponse
import json

def get_top_players():
    with connection.cursor() as cursor:
        query = """
        SELECT member.interested_ptr_id, COUNT(CASE WHEN (playedin.team = 'A' AND match.scoreA > match.scoreB) OR
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
    return HttpResponse(json.dumps(results), content_type='applications/json')