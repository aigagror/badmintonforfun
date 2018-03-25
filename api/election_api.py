from .models import *
import pytz
from django.db import connection, DatabaseError, IntegrityError
from django.http import HttpResponse
from .cursor import *
from datetime import datetime
import json


def get_all_votes():
    """
    Returns all of the votes from the current election if there are any
    :return:
    """

    with connection.cursor() as cursor:
        query = """
        SELECT *
        FROM api_votes, api_election
        WHERE api_election.endDate = NULL AND api_votes.election_id = api_election.date;
        """
        cursor.execute(query)

        results = dictfetchall(cursor)
    return HttpResponse(json.dumps(results), content_type='application/json')

def get_votes_from_member(email):
    """
    Returns all of the votes for the given member in the current election
    :param email:
    :return:
    """

    with connection.cursor() as cursor:
        query = """
        SELECT *
        FROM api_votes, api_election, api_member
        WHERE api_election.endDate = NULL AND api_votes.election_id = api_election.date AND api_votes.voter_id = %s;
        """
        cursor.execute(query, [email])

        results = dictfetchall(cursor)
    return HttpResponse(json.dumps(results), content_type='application/json')

def cast_vote(voter_email, election_date, votee_email):
    """
    Inserts/updates a vote
    :param voter_email:
    :param election_date:
    :param votee_email:
    :return:
    """

    # Check if vote exists
    with connection.cursor() as cursor:
        query = """
        SELECT COUNT(*)
        FROM api_votes
        WHERE voter_id = %s AND election_id = %s AND votee_id = %s
        """
        cursor.execute(query, [voter_email, election_date, votee_email])
        if cursor.fetchone()[0] <= 0:
            # Insert
            query = """
            INSERT INTO api_votes VALUES(%s, %s, %s)
            """
            cursor.execute(query, [voter_email, election_date, votee_email])
        else:
            # Update
            query="""
            UPDATE api_votes
            SET votee_id = %s
            WHERE voter_id = %s AND election_id = %s
            """
            cursor.execute(query, [votee_email, voter_email, election_date])
    return HttpResponse(json.dumps({"message": "Vote successfully cast"}), content_type='application/json')


def start_campaign(campaign_dict):
    """

    :param campaign_dict: an object containing the email, pitch, and job for the campaign
    :return: 200 if successful, 400 if not
    """

    curr_election = get_current_election()
    if curr_election is not None:
        return run_connection("INSERT INTO api_campaign (job, pitch, election_id, campaigner_id) VALUES\
                                (%s, %s, %s, %s)", campaign_dict["job"], campaign_dict["pitch"], curr_election["date"], campaign_dict["email"])
    else:
        return HttpResponse(json.dumps({"message": "There is no election to campaign for!"}),
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
        return HttpResponse(json.dumps({"message": "OK", "campaigns": []}), content_type='application/json')

    results = Campaign.objects.raw("SELECT * FROM api_campaign WHERE api_campaign.election_id = %s",
                                   [curr_election.date])

    if results:
        campaign_list = []
        for c in results:
            campaign_dict = {}
            campaign_dict["email"] = c.campaigner_id
            campaign_dict["name"] = str(c.campaigner)
            campaign_dict["id"] = c.id
            campaign_dict["job"] = c.job
            campaign_dict["pitch"] = c.pitch
            campaign_list.append(campaign_dict)

        alphaOrder = sorted(list(set([i["job"] for i in campaign_list])))
        dict = {"order": alphaOrder, "campaigns": campaign_list}
        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There are no current campaigns."'}),
                            content_type='application/json', status=400)


def get_current_election():
    """
        Returns the one current election going on
    :return:
    """

    curr_election = Election.objects.raw("SELECT * FROM api_election \
        WHERE date is not null AND date <= date('now')\
        ORDER BY date DESC LIMIT 1;")

    if len(list(curr_election)) == 0:
        return None
    else:
        return curr_election[0]

def current_election():
    """
    Returns the one current election going on
    :return:
    """

    election = get_current_election()
    if election == None:
        return HttpResponse(json.dumps({"status": "down", "message": "Sorry there is no election!"}), content_type='application/json')
    else:
        serialize = serializeModel(election)
        serialize["status"] = "up"
        return HttpResponse(json.dumps(serialize), content_type='application/json')


def get_all_elections():
    """
        Returns all elections in the database
    :return: JSON in format
        {"message": "OK", "elections": [{"date": "2018-02-03", "endDate": "None"},
        {"date": "2018-09-09", "endDate": "2018-09-28"}]} if successful
        {"message": "There are no current elections."} if not
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

        return HttpResponse(json.dumps(election_list), content_type='application/json')
    else:
        return HttpResponse('There are no current elections.', status=400)


def start_election(startDate, endDate=None):
    """
        Starts an election with optional endDate
    """

    if endDate is None:
        return run_connection("INSERT INTO api_election (date, endDate) VALUES (%s, NULL);", serializeDate(startDate))
    else:
        return run_connection("INSERT INTO api_election (date, endDate) VALUES\
                                 (%s, %s)", startDate, endDate)


def get_election(startDate, endDate=None):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_election WHERE date=%s", [serializeDate(startDate)])
        election = dictfetchone(cursor)

    if election:
        return HttpResponse(json.dumps({'code': 200, 'message': 'OK',
                                        'election': {'date': serializeDate(election['date']),
                                                     'endDate': serializeDate(election['endDate']) if election['endDate'] is not None else 'TBA'}}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There is no election that starts on this date!'}),
                            content_type='application/json', status=400)


def edit_election(startDate, endDate=None):
    if get_election(startDate).status_code == 400:
        return start_election(startDate, endDate)

    if endDate is not None:
        return run_connection("UPDATE api_election SET endDate = %s WHERE date = %s", endDate, startDate)
    else:
        return run_connection("UPDATE api_election SET endDate = NULL WHERE date = %s", startDate)


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
        except IntegrityError:
            return HttpResponse(json.dumps({'code': 400, 'message': 'IntegrityError!'}),
                                content_type='application/json', status=400)
        except DatabaseError as e:
            print(e)
            return HttpResponse(json.dumps({'code': 400, 'message': 'DatabaseError!'}), content_type='application/json',
                                status=400)
        else:
            return HttpResponse(json.dumps({'code': 200, 'message': 'OK'}), content_type='application/json')
