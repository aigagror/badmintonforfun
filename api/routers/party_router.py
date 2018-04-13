from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.calls.party_call import *
from api.routers.router import restrictRouter, validate_keys
from api.cursor_api import http_response, run_connection
from api.models import *

@csrf_exempt
@login_required
@restrictRouter(allowed=["POST"])
def create_party(request):
    """
    POST -- Creates a party. Anyone with Member permission or above can do this.
        Required Keys: queue_type, member_ids
            NOTE: member_ids is a comma separated list of ids to add to the party
    :param request:
    :return:
    """

    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    post_dict = dict(request.POST.items())
    if not validate_keys(['queue_type', 'member_ids'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    queue_type = post_dict['queue_type']
    queues = Queue.objects.raw("SELECT * FROM api_queue WHERE type = %s", [queue_type])
    if len(list(queues)) <= 0:
        return http_response(message='Queue does not exist', code=400)

    queue = queues[0]

    queue_id = queue.id
    user_id = user.id
    member_ids = post_dict['member_ids']
    member_ids = member_ids.split(",")  # list of ids to add to the party

    # Check if the user is already in a party
    rawquery = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s AND party_id NOT NULL", [user_id])
    member_is_in_party = len(list(rawquery)) > 0
    if member_is_in_party:
        return http_response(message="User is already in a party", code=400)

    parties_with_max_id = Party.objects.raw("SELECT * FROM api_party WHERE id = (SELECT MAX(id) FROM api_party)")
    if len(list(parties_with_max_id)) == 0:
        new_id = 0
    else:
        party_with_max_id = parties_with_max_id[0]
        new_id = party_with_max_id.id + 1

    response = run_connection("INSERT INTO api_party(id, queue_id) VALUES (%s, %s)", new_id, queue_id)
    if response.status_code != 200:
        return response

    # response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", new_id, member_id)
    # if response.status_code != 200:
    #     return response
    add_members_to_party(new_id, member_ids)

    return response

@csrf_exempt
@login_required()
@restrictRouter(allowed=["POST"])
def add_member(request):
    """
        POST -- Adds a member to the logged in user's party
            Required Keys: id, delete
            Optional Keys: queue_id, add_members, remove_members
                NOTE: `add_members` and `remove_members` are comma separated lists of
                    member id's to add or remove from the party respectively

        :param request:
        :return:
    """
    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    post_dict = dict(request.POST.items())
    if not validate_keys(['member_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    member_id = int(post_dict['member_id'])
    party_id = user.party_id

    rawquery = Member.objects.raw("SELECT * FROM api_member WHERE interested_ptr_id=%s AND party_id NOT NULL", [member_id])
    member_is_in_party = len(list(rawquery)) > 0
    if member_is_in_party:
        return http_response(message="Member is already in a party", code=400)

    members = Member.objects.raw(
        "SELECT * FROM api_member WHERE party_id NOT NULL AND party_id = %s AND interested_ptr_id = %s",
        [party_id, member_id])
    if len(list(members)) > 0:
        return http_response(message="Member is already part of party")

    response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", party_id, member_id)
    return response

@csrf_exempt
@login_required()
@restrictRouter(allowed=["POST"])
def remove_member(request):
    """
        POST -- Removes a member from the logged in user's party
            Required Keys: member_id
            Optional Keys: queue_id, add_members, remove_members
                NOTE: `add_members` and `remove_members` are comma separated lists of
                    member id's to add or remove from the party respectively

        :param request:
        :return:
    """
    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    party_id = user.party_id

    if party_id is None:
        return http_response(message='You are not part of a party', code=400)

    post_dict = dict(request.POST.items())
    if not validate_keys(['member_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    member_id = int(post_dict['member_id'])
    member = Member.objects.get(id=member_id)
    if member.party_id != party_id:
        return http_response(message='The specified member is not in your party!', code=400)
    return party_remove_member(party_id, member_id)

@login_required()
@restrictRouter(allowed=["POST"])
def delete_party(request):
    """
    DELETE -- Deletes the party that the member is in, if any.
            We are allowing "POST" here because django tests don't allow DELETE
    :param request:
    :return:
    """
    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    party_id = user.party_id

    if party_id is None:
        return http_response(message='You are not in a party', code=400)
    run_connection("DELETE FROM api_party WHERE id = %s", party_id)

    # Make sure any members associated with this party are updated
    return run_connection("UPDATE api_member SET party_id=NULL WHERE party_id=%s", party_id)


@restrictRouter(allowed=["GET"])
def member_party(request):
    """
    GET -- The logged in user's party
    :param request:
    :return:
    """
    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    member_id = user.id
    # if member_id is None:
    #     return http_response(message='No member id passed in', code=400)
    return get_member_party(member_id)