# Create your views here.

from api.calls.match_call import *
from django.contrib.auth.decorators import login_required
from api.utils import get_member_class
from badminton_server.settings import LOGIN_URL
from django.shortcuts import redirect

def restrictRouter(allowed=list(), incomplete=list()):
    def _restrictRouter(func):
        def _func(request, *args, **kwargs):
            if request.method in incomplete:
                return HttpResponse("Coming soon!", status=501)
            elif request.method not in allowed:
                return HttpResponse("Invalid request verb {}".format(request.method), status=400)
            else:
                return func(request, *args, **kwargs)

        return _func
    return _restrictRouter


def auth_decorator(allowed=None):
    def _auth_decorator(func):
        def _func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                result = redirect(LOGIN_URL)
                return result
            member_class = get_member_class(request.user.email)
            if member_class.isSuperSet(allowed):
                return HttpResponse('Not allowed', status=403)
            return func(request, *args, **kwargs)
        return _func
    return _auth_decorator


def validate_keys(keys, validate_dict):
    for key in keys:
        if key not in validate_dict:
            return False

    return True


def get_member_id_from_email(email):
    members = Interested.objects.raw("SELECT * FROM api_interested WHERE email = %s", [email])
    if len(list(members)) <= 0:
        return http_response({}, message="Member does not exist", code=400)
    member = members[0]
    return member.id


def get_match_from_member_id(member_id):
    match = find_current_match_by_member(member_id)
    match_id = (json.loads(match.content.decode('utf8').replace("'", '"')))["match"]["match_id"]
    return match_id



