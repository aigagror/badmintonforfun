# Create your views here.

from api.calls.match_call import *
from django.contrib.auth.decorators import login_required
from api.calls.interested_call import get_member_class
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
                return redirect(LOGIN_URL)
            member_class = get_member_class(request.user.email)
            if member_class.isSuperSet(allowed):
                return HttpResponse('Not allowed', status=403)
            return func(request, *args, **kwargs)
        return _func
    return _auth_decorator


@restrictRouter(allowed=["POST"])
def sign_in(request):
    code = dict(request.POST.items())
    return logged_in(code)

def validate_keys(keys, validate_dict):
    for key in keys:
        if key not in validate_dict:
            return False

    return True



