from api.calls.match_call import get_top_players
from api.routers.router import restrictRouter


@restrictRouter(allowed=["GET"])
def top_players(request):
    """
    GET -- Gets the top 5 players
        Required Keys: None
    :param request:
    :return:
    """
    return get_top_players()