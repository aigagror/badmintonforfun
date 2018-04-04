from api.cursor_api import http_response
from api.models import *

def get_most_recent_tournament():
    """
    Returns the most recent tournament
    :return:
    """
    most_recent_tournaments = Tournament.objects.raw("SELECT * FROM api_tournament ORDER BY date LIMIT 1")
    if len(list(most_recent_tournaments)) == 0:
        # No tournaments
        return http_response(message="No tournaments exists")

    most_recent_tournament = most_recent_tournaments[0]

    tournament_bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode")
