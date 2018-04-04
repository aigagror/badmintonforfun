from api.calls.match_call import get_top_players, create_match as get_create_match, edit_match as get_edit_match, delete_match as get_delete_match
from api.calls.match_call import find_current_match_by_member
from api.routers.router import restrictRouter
from .router import validate_keys, http_response
import json
from django.views.decorators.csrf import csrf_exempt

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
    return get_edit_match(dict_post["id"], dict_post["score_A"], dict_post["score_B"])

@restrictRouter(allowed=["POST"])
def finish_match(request):
    return None

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_match(request):
    """
    POST -- create a match
        PLEASE PASS IN AS RAW DATA.
        All sorts of things get real angry if you don't
        Required Keys: score_A, score_B, a_players (list), b_players (list)
    :param request:
    :return:
    """

    dict_post = json.loads(request.body.decode('utf8').replace("'", '"'))
    # write something to make sure a_players and b_players are lists
    validate_keys(["score_A", "score_B", "a_players", "b_players"], dict_post)
    return get_create_match(dict_post["score_A"], dict_post["score_B"], dict_post["a_players"], dict_post["b_players"])

@csrf_exempt
@restrictRouter(allowed=["DELETE"])
def delete_match(request):
    """
        DELETE -- delete a match
            PLEASE PASS IN AS RAW DATA.
            Required keys: id
    :param request:
    :return:
    """

    # django doesn't have anything that handles delete so...
    dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
    if not validate_keys(["id"], dict_delete):
        return HttpResponse(json.dumps({'message': 'Missing parameters'}),
                    content_type='application/json', status=400)
    return get_delete_match(dict_delete["id"])

@restrictRouter(allowed=["GET"])
def get_match(request):
    """
        GET -- The current match id of the match the member is playing
            Needs parameter id=member id
            ex: api/match/get/?id=1
    :param request:
    :return:
    """

    member_id = request.GET.get('id', None)
    if member_id is None:
        return http_response({}, message="Please pass in a member id", code=400)

    return find_current_match_by_member(member_id)