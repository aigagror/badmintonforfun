from .models import *
import pytz
from datetime import datetime
import json

def start_campaign(campaign):
    """

    :param campaign: an object containing the email, pitch, and job for the campaign
    :return: 200 if successful, 400 if not
    """

    curr_election = get_current_election()
    if curr_election:
        c = Campaign.objects.create(election=curr_election, campaigner=campaign.email,
                                job=campaign.job, pitch=campaign.pitch)
        return json.dumps({'code': 200, 'message': 'OK'})
    else:
        return json.dumps({'code': 400, 'message': 'There is no current election for this period!'})

def get_campaign(email, job):
    """
        Get the member's campaign
    :param email:
    :return: campaign information if campaign exists
    """

    try:
        campaign = Campaign.objects.get(campaigner=email, job=job)
        return json.dumps({'code': 200, 'election': str(campaign.election), 'job': campaign.job,
                       'pitch': campaign.pitch, 'message': 'OK'})
    except Campaign.DoesNotExist:
        return json.dumps({'code': 400, 'message': 'There is no campaign.'})

def edit_campaign(campaign):
    """
        Given campaign information (email, job, pitch), edit the campaign pitch if it exists
    :param campaign:
    :return: 200 if successful, 400 if not
    """
    result = Campaign.objects.filter(campaigner=campaign.email, job=campaign.job)

    if result:
        result.pitch = campaign.pitch
        return json.dumps({'code': 200, 'message': 'OK'})
    else:
        # make a more helpful message later
        return json.dumps({'code': 400, 'message': 'There is no campaign'})

def get__current_campaigns():

    results = Campaign.objects.filter(election=get_current_election())
    if results:
        string = '{"code": 200, "message": "OK", "campaigns": {'
        for c in results:
            string += '"email": ' + '"' + str(c.campaigner) + '",' + '"job": ' + '"' + c.job + '",' + '"pitch": ' + '"' \
                        + c.pitch + '",' + '"election": ' + '"' + str(c.election) + '"}}'
        print(string)
        return json.dumps(json.loads(string))
    else:
        return json.dumps({'code': 400, 'message': 'There are no current campaigns."'})

def get_current_election():

    today = str(datetime.now(pytz.utc).date())
    curr_election = Election.objects.get(date__lte=today, endDate__gte=today)
    return curr_election