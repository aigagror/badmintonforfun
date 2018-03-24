from .models import *
import pytz
from datetime import datetime
from django.db import connection, DatabaseError, IntegrityError
from django.http import HttpResponse
from .cursor import *
import json


def start_campaign(campaign):
    """

    :param campaign: an object containing the email, pitch, and job for the campaign
    :return: 200 if successful, 400 if not
    """

    curr_election = get_current_election()
    if curr_election is not None:
        return run_connection("INSERT INTO api_campaign (job, pitch, election_id, campaigner_id) VALUES\
                                (%s, %s, %s, %s)", campaign.job, campaign.pitch, curr_election.date, campaign.email)
    else:
        return HttpResponse(json.dumps({"code": 400, "message": "There is no election to campaign for!"}),
                            content_type='application/json', status=400)

def get_campaign(email, job):
    """
        Get the member's campaign
    :param email:
    :return: campaign information if campaign exists
    """

    curr_election = get_current_election()
    if curr_election is None:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There is no election.'}), content_type='application/json',
                            status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_campaign, api_election WHERE api_campaign.job=%s AND api_campaign.election_id=%s \
                       AND api_campaign.campaigner_id=%s", [job, curr_election.date, email])
        result = dictfetchone(cursor)
        if result:
            if result['endDate'] is None:
                return HttpResponse(json.dumps({'code': 200, 'election start date': result['date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                                            'election end date': result['endDate'], 'job': result['job'],
                                            'pitch': result['pitch'], 'message': 'OK'}),
                                content_type='application/json')
            else:
                return HttpResponse(json.dumps({'code': 200, 'election start date': result['date'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                                            'election end date': result['endDate'].strftime("%Y-%m-%dT%H:%M:%SZ"),
                                            'job': result['job'], 'pitch': result['pitch'], 'message': 'OK'}),
                                content_type='application/json')
        else:
            # be more helpful later
            return HttpResponse(json.dumps({'code': 400, 'message': 'There is no campaign.'}),
                                content_type='application/json', status=400)


def edit_campaign(campaign):
    """
        Given campaign information (email, job, pitch), edit the campaign pitch if it exists
    :param campaign:
    :return: 200 if successful, 400 if not
    """
    #result = Campaign.objects.filter(campaigner=campaign.email, job=campaign.job)


    if get_campaign(campaign.email, campaign.job).status_code == 400:
        return start_campaign(campaign)

    return run_connection("UPDATE api_campaign SET pitch=%s WHERE campaigner_id=%s AND job=%s",
                          campaign.pitch, campaign.email, campaign.job)


def delete_campaign(email, job):
    if json.loads(get_campaign(email, job))['code'] == 400:
        return HttpResponse(json.dumps({'code': 400, 'message': 'No campaign exists.'}), content_type='application/json',
                            status=400)

    return run_connection("DELETE FROM api_campaign WHERE campaigner_id=%s AND job=%s", email, job)


def get_current_campaigns():

    curr_election = get_current_election()
    if curr_election is None:
        return HttpResponse(json.dumps({"code": 200, "message": "OK", "campaigns": []}), content_type='application/json')

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
        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There are no current campaigns."'}),
                            content_type='application/json', status=400)


def get_current_election():
    """
        Returns the one current election going on
    :return:
    """

    today = str(datetime.now(pytz.utc).date())
    curr_election = Election.objects.raw("SELECT * FROM api_election WHERE date <= %s AND endDate >= %s", [today, today])
    #curr_election = Election.objects.get(date__lte=today, endDate__gte=today)
    if len(list(curr_election)) == 0:
        return None
    else:
        return curr_election[0]


def get_all_elections():
    """
        Returns all elections in the database
    :return: JSON in format
        {"code": 200, "message": "OK", "elections": [{"date": "2018-02-03", "endDate": "None"},
        {"date": "2018-09-09", "endDate": "2018-09-28"}]} if successful
        {"code": 400, "message": "There are no current elections."} if not
    """
    elections = Election.objects.raw("SELECT * FROM api_election")
    if elections:
        election_list = []
        for e in elections:
            election_dict = {}
            election_dict["date"] = e.date.strftime("%Y-%m-%dT%H:%M:%SZ")
            if e.endDate is None:
                election_dict["endDate"] = e.endDate
            else:
                election_dict["endDate"] = e.endDate.strftime("%Y-%m-%dT%H:%M:%SZ")
            election_list.append(election_dict)

        print(election_list)
        dict = {"code": 200, "message": "OK", "elections": election_list}
        print(dict)
        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There are no current elections.'}),
                            content_type='application/json', status=400)


def start_election(startDate, endDate=None):
    """
        Starts an election with optional endDate
    """

    if endDate is None:
        return run_connection("INSERT INTO api_election (date, endDate) VALUES\
                                (%s, NULL)", startDate)
    else:
        return run_connection("INSERT INTO api_election (date, endDate) VALUES\
                                 (%s, %s)", startDate, endDate)


def get_election(startDate, endDate=None):
    with connection.cursor() as cursor:
        if endDate is None:
            cursor.execute("SELECT * FROM api_election WHERE date=%s AND endDate=NULL", [startDate])
        else:
            cursor.execute("SELECT * FROM api_election WHERE date=%s AND endDate=%s", [startDate, endDate])
        election = dictfetchone(cursor)

    if election:
        return HttpResponse(json.dumps({'code': 200, 'message': 'OK',
                                        'election': {'date': election.date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                     'endDate': election.endDate.strftime("%Y-%m-%dT%H:%M:%SZ")}}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There is no election that starts on this date!'}),
                            content_type='application/json', status=400)


def edit_election(startDate, endDate=None):
    if get_election(startDate).status_code == 400:
        return start_election(startDate, endDate)

    if endDate is None:
        return run_connection("SELECT * FROM api_election WHERE date=%s AND endDate=NULL", startDate)
    else:
        return run_connection("SELECT * FROM api_election WHERE date=%s AND endDate=%s", startDate, endDate)


def delete_current_election():
    today = str(datetime.now(pytz.utc).date())
    # delete = Election.objects.raw("DELETE FROM api_election WHERE date <= %s AND endDate >= %s", [today, today])

    return run_connection("DELETE FROM api_election WHERE date <= %s AND endDate >= %s", today, today)


def delete_election(startDate):
    return run_connection("DELETE FROM api_election WHERE date=%s", startDate)


def run_connection(execute, *args):
    with connection.cursor() as cursor:
        try:
            cursor.execute(execute, [arg for arg in args])
            connection.commit()
        except IntegrityError:
            return HttpResponse(json.dumps({'code': 400, 'message': 'IntegrityError!'}),
                                content_type='application/json', status=400)
        except DatabaseError:
            return HttpResponse(json.dumps({'code': 400, 'message': 'DatabaseError!'}), content_type='application/json',
                                status=400)
        else:
            return HttpResponse(json.dumps({'code': 200, 'message': 'OK'}), content_type='application/json')
