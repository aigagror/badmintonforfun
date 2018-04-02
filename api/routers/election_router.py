import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import current_election, edit_election, delete_election, start_election
from api.cursor_api import *
from api.routers.router import restrictRouter
from api.models import *

@csrf_exempt
@restrictRouter(allowed=["GET"])
def get_election(request):
    """
    GET -- Gets the current election
        Required Keys: None

    :param request:
    :return:
    """
    elections = Election.objects.raw("SELECT * FROM api_election AS election\
        WHERE endDate IS NULL OR endDate >= date('now')\
        ORDER BY election.date DESC LIMIT 1;")
    if len(list(elections)) == 0:
        return http_response({}, message="No current election available")

    current_election = elections[0]

    campaigns = Campaign.objects.raw("SELECT * FROM api_campaign WHERE election_id = %s", [current_election.id])

    context = {
        'election': serializeModel(current_election),
        'campaigns': serializeSetOfModels(campaigns)
    }
    return http_response(context)


@csrf_exempt
@restrictRouter(allowed=["POST", "DELETE"])
def edit_election(request):
    """
    POST -- Edits an election
        Required Keys: id
        Optional Keys: startDate, endDate
    DELETE -- Deletes an election
        Required Keys: id
    :param request:
    :return:
    """
    if request.method == "POST":
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

        if startDate is not None:
            response = run_connection("UPDATE api_election SET date = %s", startDate)
            if response.status_code != 200:
                return response
        if endDate is not None:
            response = run_connection("UPDATE api_election SET endDate = %s", endDate)
            if response.status_code != 200:
                return response
        return response

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