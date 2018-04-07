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

    bracket_nodes = _build_bracket_dictionary(tournament_bracket_nodes, max_level, 0, 0)

    tournament_dict = {
        "tournament": {
            "tournament_id": most_recent_tournament.id,
            "date": most_recent_tournament.date,
            "end_date": most_recent_tournament.endDate,
            "bracket_nodes": bracket_nodes
        }
    }
    return tournament_dict


def _build_bracket_dictionary(bracket_nodes, max_level, curr_level, curr_sibling_index):
    """
    Recursive helper function to build a dictionary representing the bracket
     in a tournament with a complete, full binary tree
    :param bracket_nodes: list of bracket node objects
    :param max_level:
    :param curr_level:
    :param curr_sibling_index:
    :return:
    """
    if curr_level > max_level:
        return {}
    curr_bracket_node = _get_bracket_node(bracket_nodes, curr_level, curr_sibling_index)
    if not curr_bracket_node:
        return {}

    # Build the children first
    left_node = _build_bracket_dictionary(bracket_nodes, max_level, curr_level + 1, 2*curr_sibling_index)
    right_node = _build_bracket_dictionary(bracket_nodes, max_level, curr_level + 1, 2*curr_sibling_index + 1)

    # Form current node information
    match = curr_bracket_node.match
    if not match:
        match_info = {}
    else:
        match_info = {
            "startDateTime": match.startDateTime,
            "scoreA": match.scoreA,
            "scoreB": match.scoreB,
            "court": match.court,
            "endDateTime": match.endDateTime
        }

    ret = {
        "left_node": left_node,
        "right_node": right_node,
        "match_info": match_info,
        "level": curr_level,
        "sibling_index": curr_sibling_index
    }
    return ret


def _get_bracket_node(bracket_nodes, level, sibling_index):
    """
    Run through the list of bracket_nodes and see if any matches the given level and sibling_index
    :param bracket_nodes:
    :param level:
    :param sibling_index:
    :return:
    """
    for node in bracket_nodes:
        if node.level == level and node.sibling_index == sibling_index:
            return node

    return None
