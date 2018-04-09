import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import get_current_campaigns, edit_campaign, delete_campaign, get_campaign, \
    get_current_election
from api.routers.router import restrictRouter, validate_keys
from api.models import *
from api.cursor_api import *


@csrf_exempt
@restrictRouter(allowed=["POST", "DELETE"])
def campaignRouter(request):
    """
    POST -- Edits the corresponding campaign
        Required Keys: id
        Optional Keys: job, email
    DELETE -- Deletes a campaign
        Required Keys: id
    :param request:
    :return:
    """

    if request.method == "POST":
        dict_post = dict(request.POST.items())
        validate_keys(["id", "job", "pitch", "email"], dict_post)
        return edit_campaign(dict_post)
    elif request.method == "DELETE":
        # django doesn't have anything that handles delete so...
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        print(dict_delete)
        if not validate_keys(["id", "job", "email"], dict_delete):
            HttpResponse(json.dumps({'message': 'Missing parameters'}),
                         content_type='application/json', status=400)
        print(dict_delete)
        return delete_campaign(dict_delete["id"], dict_delete["email"], dict_delete["job"])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignFindRouter(request):
    """
        I should probably change this later so it's a get request but no one seems to be using this route anyway so
        POST -- Takes json data with campaign id, job, and email to find a corresponding campaign
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    if not validate_keys(["id", "job", "email"], dict_post):
        HttpResponse(json.dumps({'message': 'Missing parameters'}),
                     content_type='application/json', status=400)
    return get_campaign(dict_post["id"], dict_post["email"], dict_post["job"])

@restrictRouter(allowed=["GET"])
def get_all_campaigns(request):
    elections = Election.objects.raw("SELECT * FROM api_election AS election\
            WHERE endDate IS NULL OR endDate >= date('now')\
            ORDER BY election.date DESC LIMIT 1;")
    if len(list(elections)) == 0:
        return http_response({}, message='No campaigns currently')

    current_election = elections[0]

    campaigns = Campaign.objects.raw("SELECT * FROM api_campaign WHERE election_id = %s", [current_election.id])

    context = {
        'campaigns': serializeSetOfModels(campaigns)
    }
    return http_response(context)


@restrictRouter(allowed=["GET"])
def get_campaign_from_campaigner(request, campaigner_id):

    campaigns = Campaign.objects.raw("SELECT * FROM api_campaign WHERE campaigner_id = %s", [campaigner_id])

    if len(list(campaigns)) <= 0:
        return http_response({}, message="Member is not campaigning")

    campaign = campaigns[0]
    context = {
        'campaigns': serializeModel(campaign)
    }
    return http_response(context)

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_campaign(request):
    """
    POST -- Takes json data with campaign job, pitch, and campaigner id to create a new campaign
        Required Keys: job, pitch, id
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    jobKey = "job"
    pitchKey = "pitch"
    campaignerKey = "campaigner_id"

    keys = [jobKey, pitchKey, campaignerKey]

    if not validate_keys(keys, dict_post):
        return http_response({}, message="Missing parameters", code=400)


    job = dict_post[jobKey]
    pitch = dict_post[pitchKey]
    campaigner_id = dict_post[campaignerKey]

    campaigner_query = """
    SELECT * FROM api_interested WHERE api_interested.id = %s AND EXISTS(SELECT * FROM api_member WHERE interested_ptr_id = id)
    """
    interesteds = Interested.objects.raw(campaigner_query, [campaigner_id])

    if len(list(interesteds)) <= 0:
        return http_response({}, message="No such member found", status="down", code=400)

    interested = interesteds[0]

    curr_election_dict = get_current_election()
    curr_election = curr_election_dict['election']
    if curr_election is not None:
        return run_connection("INSERT INTO api_campaign (job, pitch, election_id, campaigner_id) VALUES\
                                    (%s, %s, %s, %s)", job, pitch, curr_election.id,
                              interested.id)
    else:
        return http_response({}, message="There is no election to campaign for!", status="down", code=400)
