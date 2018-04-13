import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import current_election, edit_election, delete_election, start_election
from api.cursor_api import *
from api.routers.router import restrictRouter
from api.models import *
import datetime
from api.utils import MemberClass
from api.routers.router import auth_decorator

@auth_decorator(MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_election(request):
    """
    GET -- Gets the current election
        Required Keys: None

    :param request:
    :return:
    """
    with connection.cursor() as cursor:
        query = """
        SELECT * FROM api_election AS election
        WHERE election.endDate IS NULL OR election.endDate >= %s
        ORDER BY election.date DESC LIMIT 1
        """
        cursor.execute(query, [datetime.datetime.now().strftime("%Y%m%d")])
        elections = dictfetchall(cursor)

    print(elections)
    if len(list(elections)) == 0:
        return HttpResponse(json.dumps({"message":"No current election available", "status": "down"}), content_type="application/json")

    current_election = elections[0]

    with connection.cursor() as cursor:
        query = """
        SELECT * FROM api_campaign 
        JOIN api_interested ON api_campaign.campaigner_id = api_interested.id
        WHERE election_id = %s
        """
        cursor.execute(query, [current_election['id']])
        campaigns = dictfetchall(cursor)
        print(campaigns)

    context = {
        'election': (serializeDict(current_election)),
        'campaigns': (serializeDict(campaigns)),
        "order": list(map(lambda x: x[0], JOBS))
    }
    return http_response(context)


@auth_decorator(MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST", "DELETE"])
def edit_election(request):
    """
    POST -- Edits an election
        Optional Keys: startDate, endDate
    DELETE -- Deletes an election
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
        print(startDate)
        print(endDate)
        if startDate is not None:
            response = run_connection("UPDATE api_election SET date = %s WHERE id = %s", startDate.strftime('%Y-%m-%d'), id)
            if response.status_code != 200:
                return response
        if endDate is not None:
            response = run_connection("UPDATE api_election SET endDate = %s WHERE id = %s", endDate.strftime('%Y-%m-%d'), id)
            if response.status_code != 200:
                return response
        return response

    elif request.method == "DELETE":
        idKey = "id"
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        print(dict_delete)
        if idKey not in dict_delete:
            return HttpResponse(json.dumps({"message": "Missing required param {}".format(idKey)}, status=400))
        return delete_election(dict_delete[idKey])


@auth_decorator(MemberClass.BOARD_MEMBER)
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
