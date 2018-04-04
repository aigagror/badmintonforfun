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
    foo = 0

@csrf_exempt
@restrictRouter(allowed=["POST"])
def add_match(request):
    foo = 0