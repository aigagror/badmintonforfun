# Create your views here.

from api.calls.match_call import *

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


def validate_keys(keys, validate_dict):
    for key in keys:
        if key not in validate_dict:
            return False

    return True

