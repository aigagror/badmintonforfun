import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import current_election, edit_election, delete_election, start_election
from api.cursor_api import deserializeDate
from api.routers.router import restrictRouter

@csrf_exempt
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def electionRouter(request):
    """
    GET -- Gets the current election
        Required Keys: None
    POST -- Edits an election
        Required Keys: id
        Optional Keys: startDate, endDate
    DELETE -- Deletes an election
        Required Keys: id
    :param request:
    :return:
    """
    if request.method == "GET":
        return current_election()
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        idKey = "id"
        startKey = "startDate"
        endKey = "endDate"
        if idKey not in dict_post:
            return HttpResponse("Missing required param {}".format(idKey), status=400)
        id = int(dict_post[idKey])
        startDate = dict_post.get(startKey, None)
        startDate = deserializeDate(startDate) if startDate != None else None

        endDate = dict_post.get(endKey, None)
        endDate = deserializeDate(endDate) if endDate != None else None

        return edit_election(id, startDate, endDate)
    elif request.method == "DELETE":
        idKey = "id"
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        if idKey not in dict_delete:
            return HttpResponse(json.dumps({"message": "Missing required param {}".format(idKey)}, status=400))
        return delete_election(dict_delete[idKey])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def electionCreateRouter(request):
    """
    POST -- Creates an election
        Required Keys: startDate
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    startKey = "startDate"
    if startKey not in dict_post:
        return HttpResponse("Missing required param {}".format(startKey), status=400)
    startDate = deserializeDate(dict_post[startKey])
    return start_election(startDate)