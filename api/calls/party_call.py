from api.calls.queue_call import get_parties_by_playtime, get_queues as call_get_queues
from api.routers.router import restrictRouter, validate_keys, run_connection
from api.models import Party, Member, Court, Match
from api.cursor_api import *


def get_party(party_id):
    parties = Party.objects.raw("SELECT * FROM api_party WHERE id = %s", [party_id])
    if len(list(parties)) == 0:
        return http_response({}, message="no parties found", code=400)

    party = parties[0]
    members = Member.objects.raw("SELECT * FROM api_member WHERE party_id = %s", [party.id])
    party_dict = serializeModel(party)
    party_dict['members'] = serializeSetOfModels(members)
    context = {
        'party': party_dict
    }

    return http_response(context)


def create_party(queue_id, member_ids):

    parties_with_max_id = Party.objects.raw("SELECT * FROM api_party WHERE id = (SELECT MAX(id) FROM api_party)")
    if len(list(parties_with_max_id)) == 0:
        new_id = 0
    else:
        party_with_max_id = parties_with_max_id[0]
        new_id = party_with_max_id.id + 1

    response = run_connection("INSERT INTO api_party(id, queue_id) VALUES (%s, %s)", new_id, queue_id)
    if response.status_code != 200:
        return response
    for member_id in member_ids:
        response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", new_id, member_id)
        if response.status_code != 200:
            return response

    return response





def edit_party(party_id, queue_id=None, add_members=None, remove_members=None):
    if queue_id is not None:
        response = run_connection("UPDATE api_party SET queue_id = %s WHERE id = %s", queue_id, party_id)
        if response.status_code != 200:
            return response

    if add_members is not None:
        for member_id in add_members:
            response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", party_id, member_id)
            if response.status_code != 200:
                return response

    if remove_members is not None:
        for member_id in remove_members:
            response = run_connection("UPDATE api_member SET party_id = NULL WHERE interested_ptr_id = %s", member_id)
            if response.status_code != 200:
                return response

    return http_response({},message="OK")


def get_member_party(member_id):
    query_set = (Party.objects.raw("SELECT * FROM api_party WHERE id = (SELECT party_id FROM api_member WHERE interested_ptr_id=%s)", [member_id]))
    if len(list(query_set)) == 0:
        return http_response({'status': 'partyless'}, message="This member is not part of a party")
    party = query_set[0]
    context = {
        "party_id": party.id,
        "queue_id": party.queue.type
    }
    return http_response(dict=context)

def party_remove_member(party_id, member_id):
    members = Member.objects.raw(
        "SELECT * FROM api_member WHERE party_id NOT NULL AND party_id = %s AND interested_ptr_id = %s",
        [party_id, member_id])
    if len(list(members)) == 0:
        return http_response(message="Member is not part of party")

    # Remove the party_id from this member
    response = run_connection("UPDATE api_member SET party_id = NULL WHERE interested_ptr_id = %s", member_id)
    # Remove the party from the database if the removed member was the last member on the party
    members_in_same_party = Member.objects.raw("SELECT * FROM api_member WHERE party_id NOT NULL AND party_id = %s", [party_id])
    if len(list(members_in_same_party)) == 0:
        # Nobody else is in this party
        # response = run_connection("DELETE FROM api_party WHERE id=%s", [party_id])
        Party.objects.get(id=party_id).delete()
        return http_response(message="OK")
    return response

def add_members_to_party(party_id, member_ids):
    """
    Add a list of members to a specified party
    :param member_ids: list of members to add to the party
    :return:
    """
    for member_id in member_ids:
        run_connection("UPDATE api_member SET party_id=%s WHERE interested_ptr_id=%s", party_id, member_id)
    return http_response(message="OK")

def queue_is_empty_with_open_court(queue_id):
    """
    # Check if there are other parties on this queue. If not, for each court associated with
    # this queue, check if there are matches with NULL endDateTime with the court id. If for a court_id, there
    # are NO matches with a NULL endDateTime, that means there is no ongoing match on that court. In that case,
    # return the open court_id. In any other case, return None.
    :param queue_id:
    :return: court_id of the open court or None
    """
    raw_query = Party.objects.raw("SELECT * FROM api_party WHERE queue_id=%s", [queue_id])
    queue_is_empty = len(list(raw_query)) == 0

    if queue_is_empty:
        raw_query = Court.objects.raw("SELECT * FROM api_court WHERE queue_id=%s", [queue_id])
        courts = list(raw_query)
        for court in courts:
            raw_query = Match.objects.raw("SELECT * FROM api_match WHERE court_id=%s AND endDateTime IS NULL", [court.id])
            court_is_free = len(list(raw_query)) == 0
            if court_is_free:
                return court.id
        return None

    else:
        return None


def get_free_members_call(member_id):
    """
    GET -- "free members" in this context mean members who are not currently in a party or an ongoing match.
        This will represent the members who are available to invite to a party.
        The returned members will exclude the logged in user who made the request.
    :param: member_id -- The id of the member making the request
    :return:
    """
    with connection.cursor() as cursor:
        query = """
        SELECT id, first_name, last_name
        FROM api_member 
        JOIN api_interested ON interested_ptr_id = id
        WHERE party_id IS NULL AND interested_ptr_id <> %s AND interested_ptr_id NOT IN 
            (SELECT m.interested_ptr_id
            FROM api_member AS m, api_playedin AS plin, api_match AS match
            WHERE m.interested_ptr_id=plin.member_id AND plin.match_id=match.id AND match.endDateTime IS NULL)
        """
        cursor.execute(query, [member_id])
        results = dictfetchall(cursor)
        return HttpResponse(json.dumps(results), content_type='application/json', status=200)
