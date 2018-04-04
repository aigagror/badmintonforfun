from django.views.decorators.csrf import csrf_exempt

from api.calls.party_call import *
from api.routers.router import restrictRouter, validate_keys
from api.cursor_api import http_response, run_connection
from api.models import *

@csrf_exempt
@restrictRouter(allowed=["POST"])
def create_party(request):
    """
    POST -- Creates a party
        Required Keys: queue_id, member_ids
            NOTE: member_ids is a comma separated list of ids to add to the party
    :param request:
    :return:
    """

    post_dict = dict(request.POST.items())
    if not validate_keys(['queue_id', 'member_ids'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    queue_id = int(post_dict['queue_id'])
    member_ids = post_dict['member_ids']
    member_ids = [int(i) for i in member_ids.split(',')]

    response = call_create_party(queue_id, member_ids)
    return response

@csrf_exempt
@restrictRouter(allowed=["POST"])
def add_member(request):
    """
        POST -- Removes members from a party
            Required Keys: id, delete
            Optional Keys: queue_id, add_members, remove_members
                NOTE: `add_members` and `remove_members` are comma separated lists of
                    member id's to add or remove from the party respectively

        :param request:
        :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(['party_id', 'member_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    party_id = int(post_dict['party_id'])
    member_id = int(post_dict['member_id'])

    members = Member.objects.raw(
        "SELECT * FROM api_member WHERE party_id NOT NULL AND party_id = %s AND interested_ptr_id = %s",
        [party_id, member_id])
    if len(list(members)) > 0:
        return http_response(message="Member is already part of party")

    response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", party_id, member_id)
    return response

@csrf_exempt
@restrictRouter(allowed=["POST"])
def remove_member(request):
    """
        POST -- Removes members from a party
            Required Keys: id, delete
            Optional Keys: queue_id, add_members, remove_members
                NOTE: `add_members` and `remove_members` are comma separated lists of
                    member id's to add or remove from the party respectively

        :param request:
        :return:
    """
    post_dict = dict(request.POST.items())
    if not validate_keys(['party_id', 'member_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)


    party_id = int(post_dict['party_id'])
    member_id = int(post_dict['member_id'])
    return party_remove_member(party_id, member_id)

@restrictRouter(allowed=["DELETE"])
def delete_party(request):
    delete_dict = dict(request.DELETE.items())
    party_id = delete_dict.get('party_id')
    if party_id is None:
        return http_response(message='No party passed in', code=400)
    return run_connection("DELETE FROM api_party WHERE id = %s", party_id)


@restrictRouter(allowed=["GET"])
def member_party(request):
    get_dict = dict(request.GET.items())
    member_id = get_dict.get('member_id')
    if member_id is None:
        return http_response(message='No member id passed in', code=400)
    return get_member_party(member_id)