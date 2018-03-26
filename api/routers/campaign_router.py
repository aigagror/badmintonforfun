import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import get_current_campaigns, edit_campaign, delete_campaign, get_campaign, start_campaign
from api.routers.router import restrictRouter, validate_keys


@csrf_exempt
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def campaignRouter(request):
    """
    GET -- Gets all campaigns of current election
    POST -- Edits a campaign
    :param request:
    :return:
    """
    if request.method == "GET":
        return get_current_campaigns()
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        validate_keys(["job", "pitch", "email"], dict_post)
        return edit_campaign(dict_post)
    elif request.method == "DELETE":
        # django doesn't have anything that handles delete so...

        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        if not validate_keys(["job", "email"], dict_delete):
            HttpResponse(json.dumps({'message': 'Missing parameters'}),
                         content_type='application/json', status=400)
        return delete_campaign(dict_delete["email"], dict_delete["job"])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignFindRouter(request):
    dict_post = dict(request.POST.items())
    if not validate_keys(["job", "email"], dict_post):
        HttpResponse(json.dumps({'message': 'Missing parameters'}),
                     content_type='application/json', status=400)
    return get_campaign(dict_post["email"], dict_post["job"])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignCreateRouter(request):
    """
    POST -- Creates an campaign
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