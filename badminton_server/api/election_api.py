from .models import *
import pytz
from datetime import datetime
import json

def start_campaign(campaign):
    """

    :param campaign: an object containing the email, pitch, and job for the campaign
    :return: 200 if successful, 400 if not
    """

    today = str(datetime.now(pytz.utc).date())
    curr_election = Election.objects.get(date__lte=today, endDate__gte=today)
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

    campaign = Campaign.objects.filter(campaigner=email, job=job)

    if not campaign:
        return json.dumps({'code': 400, 'message': 'There is no campaign.'})
    return json.dumps({'code': 200, 'election': campaign.election, 'job': campaign.job,
                       'pitch': campaign.pitch, 'message': 'OK'})

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

def get_all_campaigns():
    