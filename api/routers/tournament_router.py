import json

from django.views.decorators.csrf import csrf_exempt

from api.calls.tournament_call import *
from api.routers.router import restrictRouter, validate_keys
from api.models import *
from api.cursor_api import *

@csrf_exempt
@restrictRouter(allowed=["GET"])
def get_tournament(request):
    return get_most_recent_tournament()

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_tournament_router(request):
    """
    POST function to create a new tournament entry.
    Expect the input dictionary to be
    {
        "num_players": _,
        "tournament_type": _ (Doubles, Singles)
    }
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(["num_players", "tournament_type"], post_dict):
        HttpResponse(json.dumps({'message': 'Missing parameters num_players or tournament_type'}),
                     content_type='application/json', status=400)
    return create_tournament(post_dict)

@csrf_exempt
@restrictRouter(allowed=["POST"])
def finish_tournament_router(request):
    """
    Finish a tournament.
    Expect the dictionary to be
    {
        "tournament_id": _
    }
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(["tournament_id"], post_dict):
        http_response(message="Missing parameter tournament_id", code=400)
    return finish_tournament(post_dict)

@csrf_exempt
@restrictRouter(allowed=["GET"])
def get_bracket_node(request):
    dict_get = dict(request.GET.items())
    validate_keys(['tournament_id', 'level', 'index'], dict_get)

    tournament_id = int(dict_get['tournament_id'])
    level = int(dict_get['level'])
    index = int(dict_get['index'])

    nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND sibling_index = %s AND level = %s", [tournament_id, index, level])
    if len(list(nodes)) > 0:
        node = nodes[0]
        node_dict = serializeModel(node)

        # See if there's a match
        if node.match is not None:
            matches = Match.objects.raw("SELECT * FROM api_match WHERE id = %s", [node.match.id])
            if len(list(matches)) > 0:
                match = matches[0]
                match_dict = serializeModel(match)
                node_dict['match'] = match_dict

        context = {
            'bracket_node': node_dict
        }
        return http_response(context)
    else:
        return http_response(message='No such bracket node', code=400)


@csrf_exempt
@restrictRouter(allowed=["POST"])
def add_match(request):
    post_dict = dict(request.POST.items())
    validate_keys(['tournament_id', 'match_id', 'level', 'index'], post_dict)

    tournament_id = int(post_dict['tournament_id'])
    match_id = int(post_dict['match_id'])
    level = int(post_dict['level'])
    index = int(post_dict['index'])

    # Assert tournament exists
    tournaments = Tournament.objects.raw("SELECT * FROM api_tournament WHERE id = %s", [tournament_id])
    if len(list(tournaments)) <= 0:
        return http_response(message='Tournament does not exist', code=400)

    # Assert match exists
    matches = Tournament.objects.raw("SELECT * FROM api_match WHERE id = %s", [match_id])
    if len(list(matches)) <= 0:
        return http_response(message='Match does not exist', code=400)

    match = matches[0]

    # Assert bracket node exists
    nodes = BracketNode.objects.raw("SELECT * FROM api_bracketnode WHERE tournament_id = %s AND level = %s AND sibling_index = %s", [tournament_id, level, index])
    if len(list(nodes)) <= 0:
        return http_response(message='Tournament has no such bracket node', code=400)

    bracket_node = nodes[0]

    response = run_connection("UPDATE api_bracketnode SET match_id = %s WHERE id = %s", match.id, bracket_node.id)
    return response
