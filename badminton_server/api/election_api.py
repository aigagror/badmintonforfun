from .models import *
import pytz
from datetime import datetime
from django.db import connection, transaction, DatabaseError, IntegrityError
from .cursor import *
import json

def start_campaign(campaign):
    """

    :param campaign: an object containing the email, pitch, and job for the campaign
    :return: 200 if successful, 400 if not
    """

    curr_election = get_current_election()
    if curr_election:
        #c = Campaign.objects.raw(election=curr_election, campaigner=campaign.email,
        #                        job=campaign.job, pitch=campaign.pitch)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO api_campaign (id, job, pitch, election_id, campaigner_id) VALUES\
                                (NULL, %s, %s, %s, %s)", [campaign.job, campaign.pitch, curr_election.date, campaign.email])

            try:
                 connection.commit()
            except DatabaseError:
                 return json.dumps({'code': 400, 'message': 'There is no current election for this period!'})
            except IntegrityError:
                 return json.dumps({'code': 400, 'message': 'There is no current election for this period!'})
            else:
                 return json.dumps({'code': 200, 'message': 'OK'})

def get_campaign(email, job):
    """
        Get the member's campaign
    :param email:
    :return: campaign information if campaign exists
    """

    curr_election = get_current_election()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_campaign, api_election WHERE api_campaign.job=%s AND api_campaign.election_id=%s \
                       AND api_campaign.campaigner_id=%s", [job, curr_election.date, email])
        result = dictfetchone(cursor)
        if result:
            return json.dumps({'code': 200, 'election': str(result['date']) + " to " + str(result['endDate']), 'job': result['job'],
                       'pitch': result['pitch'], 'message': 'OK'})
        else:
            # be more helpful later
            return json.dumps({'code': 400, 'message': 'There is no campaign.'})

def edit_campaign(campaign):
    """
        Given campaign information (email, job, pitch), edit the campaign pitch if it exists
    :param campaign:
    :return: 200 if successful, 400 if not
    """
    #result = Campaign.objects.filter(campaigner=campaign.email, job=campaign.job)
    with connection.cursor() as cursor:
        cursor.execute("UPDATE api_campaign SET pitch=%s WHERE campaigner_id=%s AND job=%s",
                       [campaign.pitch, campaign.email, campaign.job])

        try:
            connection.commit()
        except DatabaseError:
            return json.dumps({'code': 400, 'message': 'Database Error!'})
        except IntegrityError:
            return json.dumps({'code': 400, 'message': 'Integrity Error!'})
        else:
            return json.dumps({'code': 200, 'message': 'OK'})

def get__current_campaigns():

    curr_election = get_current_election()
    #results = Campaign.objects.filter(election=get_current_election())
    results = Campaign.objects.raw("SELECT * FROM api_campaign WHERE api_campaign.election_id = %s",
                                   [curr_election.date])

    if results:
        campaign_list = []
        for c in results:
            campaign_dict = {}
            campaign_dict["email"] = c.campaigner_id
            campaign_dict["job"] = c.job
            campaign_dict["pitch"] = c.pitch
            campaign_list.append(campaign_dict)

        dict = {"code": 200, "message": "OK", "campaigns": campaign_list}
        print(dict)
        return json.dumps(dict)
    else:
        return json.dumps({'code': 400, 'message': 'There are no current campaigns."'})

def get_current_election():
    """
        Returns the one current election going on
    :return:
    """

    today = str(datetime.now(pytz.utc).date())
    curr_election = Election.objects.raw("SELECT * FROM api_election WHERE date <= %s AND endDate >= %s", [today, today])
    #curr_election = Election.objects.get(date__lte=today, endDate__gte=today)
    return curr_election[0]