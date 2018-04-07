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
    """
    POST function to create a new tournament entry.
    Expect the input dictionary to be
    {
        "num_leaf_matches": _
    }
    :param request:
    :return:
    """
    json_post_data = json.loads(request.body.decode('utf8').replace("'", '"'))
    if not validate_keys(["num_leaf_matches"], json_post_data):
        HttpResponse(json.dumps({'message': 'Missing parameters members'}),
                     content_type='application/json', status=400)
    return create_tournament(json_post_data)


@csrf_exempt
@restrictRouter(allowed=["GET"])
def get_bracket_node(request):
    foo = 0

@csrf_exempt
@restrictRouter(allowed=["POST"])
def add_match(request):
    foo = 0