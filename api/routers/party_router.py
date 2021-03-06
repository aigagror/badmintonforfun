import random

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from api.utils import MemberClass, id_for_member
from api.calls.party_call import *
from api.calls.match_call import *
from api.routers.router import restrictRouter, validate_keys, auth_decorator
from api.cursor_api import http_response, run_connection
from api.models import *

@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def create_party(request):
    """
    POST -- Creates a party. Anyone with Member permission or above can do this.
        Required Keys: queue_type, member_ids
            NOTE: member_ids is a comma separated list of ids to add to the party (EXCLUDES the user themselves)
    :param request:
    :return:
    """
    post_dict = dict(request.POST.items())
    print(post_dict)
    if not validate_keys(['queue_id', 'member_ids'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    queue_id = post_dict['queue_id']
    queues = Queue.objects.raw("SELECT * FROM api_queue WHERE id = %s", [queue_id])
    if len(list(queues)) <= 0:
        return http_response(message='Queue does not exist', code=400)

    queue = queues[0]

    queue_id = queue.id
    user_id = id_for_member(request.user.email)
    member_ids = post_dict['member_ids']
    member_ids = member_ids.split(",")  # list of ids to add to the party
    if user_id not in member_ids:
        member_ids.append(str(user_id)) # add self to the party, if not already specified

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

    # Check if there are other parties on this queue. If not, for each court associated with
    # this queue, check if there are matches with NULL endDateTime with the court id. If for a court_id, there
    # are no matches with a NULL endDateTime, that means there is no ongoing match on that court. In that case,
    # skip creating a party and just throw this group into a match on that empty court.
    open_court_id = queue_is_empty_with_open_court(queue_id)
    if open_court_id:
        # Create match
        # Randomize the member_id's into two teams (preferably equal numbers on each team)
        a_players = []
        b_players = []
        num_players = len(member_ids)
        for member_id in member_ids:
            choice = random.choice([True, False])
            if choice and len(a_players) < num_players/2:
                # Add to a_players, if half of players aren't already on there
                a_players.append(member_id)
            else:
                if len(b_players) < num_players/2:
                    b_players.append(member_id)
                else:
                    a_players.append(member_id)

        create_match(a_players=a_players, b_players=b_players, court_id=open_court_id)
        return http_response(message="OK", code=200)
    else:
        # Create party on the queue
        response = run_connection("INSERT INTO api_party(id, queue_id) VALUES (%s, %s)", new_id, queue_id)
        if response.status_code != 200:
            return response

        # response = run_connection("UPDATE api_member SET party_id = %s WHERE interested_ptr_id = %s", new_id, member_id)
        # if response.status_code != 200:
        #     return response
        add_members_to_party(new_id, member_ids)

        return response

@auth_decorator(allowed=MemberClass.MEMBER)
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

    post_dict = dict(request.POST.items())
    if not validate_keys(['member_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)

    member_id = post_dict['member_id']
    my_id = id_for_member(request.user.email)
    party = party_for_member(my_id)
    party_id = party.id

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

@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def remove_member(request):
    """
        POST -- Removes a member from the logged in user's party
            Required Keys: member_id
        :param request:
        :return:
    """
    post_dict = dict(request.POST.items())

    my_id = id_for_member(request.user.email)
    party = party_for_member(my_id)

    if party is None:
        return http_response(message='You are not part of a party', code=400)

    party_id = party.id
    member_id = int(post_dict['member_id'])
    member = Member.objects.get(id=member_id)
    if member.party_id != party_id:
        return http_response(message='The specified member is not in your party!', code=400)
    return party_remove_member(party_id, member_id)

@auth_decorator(allowed=MemberClass.MEMBER)
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


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def member_party(request):
    """
    GET -- The logged in user's party
    :param request:
    :return:
    """
    member_id = id_for_member(request.user.email)
    return get_member_party(member_id)


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def join_party(request):
    session_email = request.user.username
    if not request.user.is_authenticated:
        return http_response({}, message="You are not logged in", code=302)

    try:
        user = Member.objects.get(email=session_email)
    except Member.DoesNotExist:
        return http_response({}, message="You do not have the required permissions", code=403)

    member_id = user.id
    curr_party_id = user.party_id
    if curr_party_id is not None:
        return http_response(message="You are already in a party", code=400)

    post_dict = dict(request.POST.items())
    if not validate_keys(['party_id'], post_dict):
        return http_response({}, message="Keys not found", code=400)
    party_id = post_dict["party_id"]

    return run_connection("UPDATE api_member SET party_id=%s WHERE interested_ptr_id=%s", party_id, member_id)


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["POST"])
def leave_party(request):
    session_email = request.user.username

    member_id = id_for_member(request.user.email)
    party = party_for_member(member_id)
    party_id = party.id

    return party_remove_member(party_id, member_id)


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET"])
def get_free_members(request):
    """
    GET -- "free members" in this context mean members who are not currently in a party or an ongoing match.
        This will represent the members who are available to invite to a party.
        The returned members will exclude the logged in user who made the request.
    :param request:
    :return:
    """
    member_id = id_for_member(request.user.email)
    return get_free_members_call(member_id)
