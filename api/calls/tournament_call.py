from api.cursor_api import *
from api.models import *
from django.db import connection
import datetime

def get_most_recent_tournament():
    """
    Returns the most recent tournament, including the bracket nodes associated with it
    :return:
    """
    most_recent_tournaments = Tournament.objects.raw("SELECT * FROM api_tournament ORDER BY date DESC LIMIT 1")
    if len(list(most_recent_tournaments)) == 0:
        return http_response({"status":"down"},message="No tournaments exist", code=200)

    most_recent_tournament = most_recent_tournaments[0]
    t_id = most_recent_tournament.id

    # Get the bracket nodes associated with this tournament ordered by lowest 'level' and 'sibling_index' first
    tournament_bracket_nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id=%s ORDER BY level, sibling_index ASC", [t_id])
    tournament_bracket_nodes = list(tournament_bracket_nodes)
    # Get max 'level' among those bracket nodes (this will determine the depth of our bracket node dictionary
    # the 'root' tournament bracket node will be at level 0
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(level) AS max_level FROM api_bracketnode")
        row = cursor.fetchone()

        max_level = row[0]

    bracket_nodes = _build_bracket_dictionary_it(tournament_bracket_nodes, max_level)

    tournament_dict = {
        "tournament": {
            "tournament_id": most_recent_tournament.id,
            "date": serializeDate(most_recent_tournament.date),
            "end_date": serializeDate(most_recent_tournament.endDate)if most_recent_tournament.endDate is not None else "None",
            "bracket_nodes": bracket_nodes
        }
    }



    return http_response(tournament_dict)


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

    matches = Match.objects.raw("SELECT * FROM api_match WHERE bracket_node_id=%s", [curr_bracket_node.id])
    if not matches:
        match_info = {}
    else:
        match_info = []
        for match in matches:
            match_dict = {
                "match_id": match.id,
                "startDateTime": serializeDateTime(match.startDateTime),
                "scoreA": match.scoreA,
                "scoreB": match.scoreB,
                "endDateTime": serializeDateTime(match.endDateTime) if match.endDateTime is not None else "None"
            }
            match_info.append(match_dict)

    ret = {
        "left_node": left_node,
        "right_node": right_node,
        "matches": match_info,
        "level": curr_level,
        "sibling_index": curr_sibling_index
    }
    return ret

def _build_bracket_dictionary_it(bracket_nodes, max_level):
    """
        Start from root, traverse level by level (left -> right)

    :param bracket_nodes:
    :param max_level:
    :return:
    """
    bracket_node_id = bracket_nodes[0].id

    bracket_list = []
    for i in range(0, max_level + 1):
        num_range = 2 ** i
        for j in range(0, num_range):
            bracket_dict = {"bracket_node_id": bracket_node_id}
            matches = Match.objects.raw("SELECT * FROM api_match WHERE bracket_node_id=%s", [bracket_node_id])
            match_info = []
            query = """
            SELECT api_playedin.member_id, api_interested.first_name, api_interested.last_name 
            FROM api_playedin
            JOIN api_interested ON api_playedin.member_id = api_interested.id
            WHERE match_id=%s AND team=%s
            """
            for match in matches:
                with connection.cursor() as cursor:
                    cursor.execute(query, [match.id, "A"])
                    team_a = dictfetchall(cursor)
                    cursor.execute(query, [match.id, "B"])
                    team_b = dictfetchall(cursor)
                match_dict = {
                    "match_id": match.id,
                    "startDateTime": serializeDateTime(match.startDateTime),
                    "scoreA": match.scoreA,
                    "scoreB": match.scoreB,
                    "endDateTime": serializeDateTime(match.endDateTime) if match.endDateTime is not None else None,
                    "team_A": team_a,
                    "team_B": team_b
                }
                match_info.append(match_dict)
            bracket_dict["matches"] = match_info
            bracket_dict["level"] = i
            bracket_dict["sibling_index"] = j
            bracket_list.append(bracket_dict)
            bracket_node_id += 1
    return bracket_list


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


def create_tournament(dict_post):
    today = datetime.date.today()
    date = serializeDate(today)
    num_players = int(dict_post["num_players"])
    tournament_type = dict_post["tournament_type"]
    elimination_type = dict_post["elimination_type"]

    if tournament_type == "DOUBLES":
        assert num_players % 4 == 0
    elif tournament_type == "SINGLES":
        assert num_players % 2 == 0
    else:
        return http_response(message="Invalid tournament type", code=400)

    num_leaf_matches = int(num_players/2) if tournament_type == "SINGLES" else int(num_players/4)

    # Add tournament
    new_tournament_id = _get_next_tournament_id()  # We need this for creating the bracket nodes
    resp = _add_tournament(new_tournament_id, date, tournament_type, elimination_type)

    # Add empty bracket nodes associated with this new tournament
    # Determine max level
    max_level = _get_max_level(num_leaf_matches)
    # Add bracket nodes
    _add_bracket_nodes(new_tournament_id, max_level, num_leaf_matches)

    return http_response({})


def _add_bracket_nodes(tournament_id, max_level, num_leaf_matches):
    # Bracket nodes for the perfect tree of with the max level of max_level-1
    for level in range(max_level):  # Iterate "max_level"-1 times
        for sibling_index in range(2**max_level):
            _add_bracket_node(tournament_id, level, sibling_index)

    # Add the remaining bracket nodes on the last level
    num_remaining_nodes = (2**max_level) - (2 * (2**max_level - num_leaf_matches))
    for sibling_index in range(num_remaining_nodes):
        _add_bracket_node(tournament_id, max_level, sibling_index)


def _add_bracket_node(tournament_id, level, sibling_index):
    query = '''
        INSERT INTO api_bracketnode (tournament_id, level, sibling_index)
        VALUES (%s, %s, %s);
        '''
    return run_connection(query, tournament_id, level, sibling_index)


def _get_max_level(num_leaf_matches):
    max_level = 0
    while 2 ** max_level < num_leaf_matches:
        max_level += 1
    return max_level


def _get_next_tournament_id():
    """
    Returns the id of the most recent tournament + 1
    :return:
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) AS max_id FROM api_tournament")
        row = cursor.fetchone()

    max_id = row[0] + 1 if row[0] else 0
    return max_id


def _add_tournament(new_tournament_id, date, tournament_type, elimination_type):
    query = '''
    INSERT INTO api_tournament (id, date, match_type, elimination_type)
    VALUES (%s, %s, %s, %s);
    '''
    return run_connection(query, new_tournament_id, date, tournament_type, elimination_type)


def finish_tournament(dict_post):
    tournament_id = int(dict_post["tournament_id"])
    today = datetime.date.today()
    endDate = serializeDate(today)
    query = '''
    UPDATE api_tournament
    SET endDate=%s
    WHERE id=%s;
    '''
    return run_connection(query, endDate, tournament_id)

def add_match_call(bracket_node_id, team_A, team_B):
    """
    Create a new match for the specified bracket node.
    Inserts into Match and PlayedIn.
    :param bracket_node_id:
    :param team_A: list of strings representing member ids
    :param team_B:
    :return:
    """
    # Get the next match id to be used
    with connection.cursor() as cursor:
        query = """
        SELECT COALESCE(MAX(id)+1, 0) AS newID
        FROM api_match
        """
        result = cursor.execute(query)
        newID = dictfetchall(cursor)[0]['newID']

    query = """
        INSERT INTO api_match(id, startDateTime, scoreA, scoreB, bracket_node_id) VALUES (%s, %s, 0, 0, %s)
        """
    today = datetime.datetime.now()
    response = run_connection(query, newID, serializeDateTime(today), bracket_node_id)

    for p in team_A:
        # It seems to be passed as a list of int strings rather than just ints
        p = int(p)
        query = """
           INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)
           """
        response = run_connection(query, p, "A", newID)

    for p in team_B:
        p = int(p)
        query = """
          INSERT INTO api_playedin(member_id, team, match_id) VALUES (%s, %s, %s)
          """
        response = run_connection(query, p, "B", newID)

    return http_response(message="OK", code=200)
