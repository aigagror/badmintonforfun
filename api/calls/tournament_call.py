from api.cursor_api import http_response
from api.models import *

def get_most_recent_tournament():
    """
    Returns the most recent tournament, including the bracket nodes associated with it
    :return:
    """
    most_recent_tournaments = Tournament.objects.raw("SELECT * FROM api_tournament ORDER BY date LIMIT 1")
    if len(list(most_recent_tournaments)) == 0:
        # No tournaments
        return http_response(message="No tournaments exists")

    most_recent_tournament = most_recent_tournaments[0]
    t_id = most_recent_tournament.id

    # Get the bracket nodes associated with this tournament ordered by lowest 'level' and 'sibling_index' first
    tournament_bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id=%s ORDER BY level, sibling_index ASC", [t_id])
    tournament_bracket_nodes = list(tournament_bracket_nodes)
    # Get max 'level' among those bracket nodes (this will determine the depth of our bracket node dictionary
    # the 'root' tournament bracket node will be at level 0
    rawquery = BracketNode.objects.raw("SELECT MAX(level) AS max_level FROM api_bracketnode")
    max_level = rawquery[0].max_level
    height = max_level # Assuming that a root with one generation of children is height 1

    bracket_nodes = {}
    # Populate bracket_nodes
    for level in range(height+1):
        for sibling_index in range(2 ** level):
            foo = 0

    tournament_dict = {
        "tournament_id": most_recent_tournament.id,
        "date": most_recent_tournament.date,
        "end_date": most_recent_tournament.endDate,
        "bracket_nodes": bracket_nodes
    }