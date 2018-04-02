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


def delete_party(party_id):
    return run_connection("DELETE FROM api_party WHERE id = %s", party_id)


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

