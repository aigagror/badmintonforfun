import json

from django.views.decorators.csrf import csrf_exempt

from api.calls.tournament_call import get_most_recent_tournament
from api.routers.router import restrictRouter, validate_keys
from api.models import *
from api.cursor_api import *

@csrf_exempt
@restrictRouter(allowed=["GET"])
def get_tournament(request):
    return get_most_recent_tournament()

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_tournament(request):
    foo = 0

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
    foo = 0