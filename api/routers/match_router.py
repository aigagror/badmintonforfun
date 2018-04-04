from api.calls.match_call import get_top_players
from api.routers.router import restrictRouter
from .router import validate_keys


@restrictRouter(allowed=["GET"])
def top_players(request):
    """
    GET -- Gets the top 5 players
        Required Keys: None
    :param request:
    :return:
    """
    return get_top_players()

@restrictRouter(allowed=["POST"])
def edit_match(request):
    """
    POST -- edits the match score, provide the score of the match
        Required Keys: id (match ID), score_A, score_B
    :param request:
    :return:
    """

    dict_post = dict(request.POST.items())
    validate_keys(["score_A", "score_B", "id"],dict_post)
    return edit_match(dict_post["id"], dict_post["score_A"], dict_post["score_B"])

@restrictRouter(allowed=["POST"])
def finish_match(request):
    return None

@restrictRouter(allowed=["POST"])
def create_match(request):
    """
    POST -- create a match
        Required Keys: score_A, score_B, a_players (list), b_players (list)
    :param request:
    :return:
    """

    dict_post = dict(request.POST.items())
    # write something to make sure a_players and b_players are lists
    validate_keys(["score_A", "score_B", "a_players", "b_players"])
    return create_match(dict_post["score_A"], dict_post["score_B"], dict_post["a_players"], dict_post["b_players"])