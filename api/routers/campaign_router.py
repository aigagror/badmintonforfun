import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import get_current_campaigns, edit_campaign, delete_campaign, get_campaign, start_campaign
from api.routers.router import restrictRouter, validate_keys


@csrf_exempt
@restrictRouter(allowed=["POST", "DELETE"])
def campaignRouter(request):
    """
    POST -- Takes json data with campaign id, job, and email to edit the corresponding campaign
    DELETE -- Takes raw data with campaign id, job, and email to delete the corresponding campaign
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


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignCreateRouter(request):
    """
    POST -- Takes json data with campaign job, pitch, and email to create a new campaign
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    jobKey = "job"
    pitchKey = "pitch"
    email = "email"

    keys = [jobKey, pitchKey, email]

    if not validate_keys(keys, dict_post):
        HttpResponse(json.dumps({'message': 'Missing parameters'}),
                     content_type='application/json', status=400)

    campaign_dict = {
        "job": dict_post[jobKey],
        "pitch": dict_post[pitchKey],
        "email": dict_post[email],
    }
    return start_campaign(campaign_dict)