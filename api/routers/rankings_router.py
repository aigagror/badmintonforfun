from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.utils import MemberClass
from api.calls.rankings_call import get_top_players_by_level
from api.routers.router import *


@csrf_exempt
@login_required
@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_rankings_by_level(request):
    response = get_top_players_by_level()
    content = response.content.decode()

    context = {
        'rankings': json.loads(content)
    }
    print(context)
    return http_response(dict=context)


@csrf_exempt
@login_required
@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_rankings_by_win_ratio(request):
    response = get_top_players()
    content = response.content.decode()

    context = {
        'rankings': json.loads(content)
    }
    print(context)
    return http_response(dict=context)
