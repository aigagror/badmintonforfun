from ..cursor_api import *
import json
from ..models import *

jobs_list = [x[0] for x in JOBS]

#votes
def get_all_votes():
    """
    Returns all of the votes from the current election if there are any
    :return:
    """

    with connection.cursor() as cursor:
        query = """
        SELECT voter.first_name, voter.last_name, votee.first_name, votee.last_name
        FROM api_vote AS vote, api_election AS election, api_campaign AS campaign, api_interested AS voter, api_interested AS votee
        WHERE (election.endDate IS NULL OR election.endDate >= date('now')) 
        AND vote.campaign_id = campaign.id AND campaign.election_id = election.id
        AND votee.id = campaign.campaigner_id AND voter.id = vote.voter_id;
        """
        cursor.execute(query)

        results = dictfetchall(cursor)

    return HttpResponse(json.dumps(results), content_type='application/json')


def get_votes_from_member(id):
    """
    Returns all of the votes for the given member in the current election
    :param id:
    :return:
    """

    with connection.cursor() as cursor:
        query = """
        SELECT *
        FROM api_vote, api_election, api_member
        WHERE api_election.endDate = NULL AND api_vote.election_id = api_election.date AND api_vote.voter_id = %s;
        """
        cursor.execute(query, [id])

        results = dictfetchall(cursor)
    return HttpResponse(json.dumps(results), content_type='application/json')



def get_campaign(id, email, job):
    """
        Get the member's campaign
    :param email:
    :return: campaign information if campaign exists
    """

    curr_election_dict = get_current_election()
    curr_election = curr_election_dict['election']
    if curr_election is None:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There is no election.'}), content_type='application/json',
                            status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_campaign, api_election WHERE api_campaign.job=%s AND api_campaign.election_id=%s\
                       AND api_campaign.campaigner_id=%s", [job, curr_election.id, email])
        result = dictfetchone(cursor)
        if result:
            if result['endDate'] is None:
                return HttpResponse(json.dumps({'code': 200, 'election start date': serializeDate(result['date']),
                                            'election end date': result['endDate'], 'job': result['job'],
                                            'pitch': result['pitch'], 'message': 'OK'}),
                                content_type='application/json')
            else:
                return HttpResponse(json.dumps({'code': 200, 'election start date': serializeDate(result['date']),
                                            'election end date': serializeDate(result['endDate']),
                                            'job': result['job'], 'pitch': result['pitch'], 'message': 'OK'}),
                                content_type='application/json')
        else:
            # be more helpful later
            return HttpResponse(json.dumps({'code': 400, 'message': 'There is no campaign.'}),
                                content_type='application/json', status=400)


def edit_campaign(campaign_dict):
    """
        Given campaign information (email, job, pitch), edit the campaign pitch if it exists
    :param campaign:
    :return: 200 if successful, 400 if not
    """

    if get_campaign(campaign_dict["id"], campaign_dict["email"], campaign_dict["job"]).status_code == 400:
        return start_campaign(campaign_dict)

    return run_connection("UPDATE api_campaign SET pitch=%s WHERE campaigner_id=%s AND job=%s",
                          campaign_dict["pitch"], campaign_dict["email"], campaign_dict["job"])


def delete_campaign(id, email, job):
    if get_campaign(id, email, job).status_code == 400:
        return HttpResponse(json.dumps({'message': 'No campaign exists.'}), content_type='application/json',
                            status=400)

    return run_connection("DELETE FROM api_campaign WHERE id=%s", id)


def get_current_campaigns():
    print(1)
    curr_election_dict = get_current_election()
    curr_election = curr_election_dict["election"]
    if curr_election is None:
        return HttpResponse(json.dumps({"message": "OK", "campaigns": []}), content_type='application/json')

    results = Campaign.objects.raw("SELECT * FROM api_campaign WHERE api_campaign.election_id = %s",
                                   [curr_election.date])


    if results:
        campaign_list = []
        for c in results:
            campaign_dict = serializeModel(c)
            campaign_list.append(campaign_dict)

        alphaOrder = sorted(list(set([i["job"] for i in campaign_list])))
        dict = {"order": alphaOrder, "campaigns": campaign_list}
        return HttpResponse(json.dumps(dict), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'code': 400, 'message': 'There are no current campaigns."'}),
                            content_type='application/json', status=400)


#elections
def get_current_election():
    """
    Returns the one current election and all of its campaigns
    :return:
    """
    print(2)
    curr_election = Election.objects.raw("SELECT * FROM api_election AS election\
        WHERE endDate IS NULL OR endDate >= date('now')\
        ORDER BY election.date DESC LIMIT 1;")

    if len(list(curr_election)) == 0:
        return None
    else:
        election = curr_election[0]
        with connection.cursor() as cursor:
            query = """
                SELECT * FROM api_campaign WHERE election_id = %s
                JOIN api_interested ON api_campaign.campaigner = api_interested.id
            """
            cursor.execute(query, [election.id])

            results = dictfetchall(cursor)
            print(hello)
            print(results)
        campaigns = Campaign.objects.raw("SELECT * FROM api_campaign WHERE election_id = %s", [election.id])
        return {'election': election, 'campaigns': campaigns}

def current_election():
    """
    Returns the one current election going on
    :return:
    """
    election_dict = get_current_election()
    if election_dict is None:
        return HttpResponse(json.dumps({"status": "down", "message": "Sorry there is no election!"}), content_type='application/json')
    else:
        serialize = serializeModel(election_dict['election'])
        serialize["status"] = "up"
        campaigns = election_dict['campaigns']
        serialize["campaigns"] = []
        serialize['order'] = jobs_list
        for campaign in campaigns:
            campaign_json = serializeModel(campaign)
            campaign_json["name"] = str(campaign.campaigner)
            serialize["campaigns"].append(campaign_json)
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
            election_dict["date"] = serializeDate(e.date)
            if e.endDate is None:
                election_dict["endDate"] = e.endDate
            else:
                election_dict["endDate"] = serializeDate(e.endDate)
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


def get_election(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM api_election WHERE id=%s", [id])
        election = dictfetchone(cursor)
    if election:
        return HttpResponse(json.dumps({'code': 200, 'message': 'OK',
                                        'election': {'date': serializeDate(election['date']),
                                                     'endDate': serializeDate(election['endDate']) if election['endDate'] is not None else 'TBA'}}),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'message': 'There is no election that starts on this date!'}),
                            content_type='application/json', status=400)


def edit_election(id, startDate, endDate):
    if get_election(id).status_code == 400:
        return start_election(startDate, endDate)

    ret = HttpResponse(json.dumps({"message": "Nothing edited"}), content_type='application/json', status=400)
    if startDate is not None:
        ret =  run_connection("UPDATE api_election SET date = %s WHERE id = %s", serializeDate(startDate), id)
    if endDate is not None:
        ret =  run_connection("UPDATE api_election SET endDate = %s WHERE id = %s", serializeDate(endDate), id)
    return ret

def delete_election(id):

    elections = Election.objects.raw("SELECT * FROM api_election WHERE id = %s", [id])

    if len(list(elections)) == 0:
        return HttpResponse(json.dumps({'message': 'No election found'}),
                     content_type='application/json', status=400)

    election = elections[0]
    campaigns = Campaign.objects.raw("SELECT * FROM api_campaign WHERE election_id = %s", [election.id])
    with connection.cursor() as cursor:
        for campaign in campaigns:
            # TODO: Check these responses
            response = run_connection("DELETE FROM api_vote WHERE campaign_id = %s", campaign.id)
            response = run_connection("DELETE FROM api_campaign WHERE id=%s", campaign.id)

    response = run_connection("DELETE FROM api_election WHERE id=%s", id)
    return response
