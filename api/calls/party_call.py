from api.calls.queue_call import get_parties_by_playtime, get_queues as call_get_queues
from api.routers.router import restrictRouter, validate_keys, run_connection
from api.models import Party, Member
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
        return http_response({}, message="This member is not part of a party", status=400)
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