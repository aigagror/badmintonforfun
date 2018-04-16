import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from api.calls.election_call import delete_campaign
from api.calls.home_call import get_schedule
from api.calls.settings_call import *
from api.routers.router import restrictRouter, validate_keys, auth_decorator
from api.cursor_api import *
from django.contrib.auth.decorators import login_required
from api.utils import MemberClass, get_member_class, id_for_member


@restrictRouter(allowed=["GET", "POST"])
@auth_decorator(allowed=MemberClass.MEMBER)
def settingsRouter(request):
    """
    Allow members to get and edit their own settings.
    Expect input/output dictionary to be of the form
    {
        'private': _,
        'bio': _
    }
    :param request:
    :return:
    """

    session_id = id_for_member(request.user.email)
    if request.method == "GET":
        if session_id is None:
            return HttpResponse(json.dumps({"message": "No such member"}),
                                content_type="application/json")
        return member_config(session_id)
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        if not validate_keys(["private", "bio"], dict_post):
            HttpResponse(json.dumps({'message': 'Missing parameters private or bio'}),
                         content_type='application/json', status=400)
        if session_id is None:
            return HttpResponse(json.dumps({"message": "No such member"}),
                                content_type="application/json")
        return member_config_edit(session_id, dict_post)


@restrictRouter(allowed=["GET", "POST"])
@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
def settingsBoardMemberRouter(request):
    """
    Allow board members to get/edit list of boardmembers.
    Expect input/output dictionary to be of the form
    {
        'boardmembers': [
            {
                'member_id': _
                'first_name': _
                'last_name': _
                'email': _
                'job': _
            },
            ...
        ]
    }
    :param request:
    :return:
    """

    session_id = id_for_member(request.user.email)

    if request.method == "GET":
        return boardmembers_config()
    elif request.method == "POST":
        # Can only change their jobs
        json_post_data = json.loads(request.body)
        if not validate_keys(["boardmembers"], json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameters member_id or job'}),
                         content_type='application/json', status=400)
        return boardmembers_config_edit(json_post_data)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["GET", "POST"])
def settingsAllMembersRouter(request):
    """
    Allows boardmembers to get information on all the people in the club (interested, members, boardmembers)
    AND promote/demote people
    Expect GET OUTPUT dictionary to be of the form
    {
        'members': [
            {
                'member_id': _, (Used for promoting/demoting/deletion)
                'first_name': _,
                'last_name': _,
                'email': _,
                'status': _ (Interested, Member, BoardMember)
            },
            ...
        ]
    }
    Expect POST INPUT dictionary
        Example: {"member_id": 39, "status": "Interested"}

    Look at POST branch below for specific input dictionaries
    :param request:
    :return:
    """

    if request.method == "GET":
        return get_all_club_members()
    elif request.method == "POST":
        # Promote/demote ONE member (Interested, Member, BoardMember)
        # {"member_id": _, "status": _}
        # Going to BoardMember, the default 'job'='OFFICER'
        post_dict = dict(request.POST)
        print(post_dict)
        if not validate_keys(["member_id", "status"], post_dict):
            return http_response({}, message="Keys not found", code=400)
        return update_club_member_status(post_dict)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def delete_member(request):
    """
    DELETE -- (labeled as POST because Django doesn't handle DELETE)
        Delete ONE member from the db completely
        Example: {"member_id": 39}
    :param request:
    :return:
    """
    # Here, the dictionary should be {"member_id": _}
    post_dict = dict(request.POST.items())
    if not validate_keys(["member_id"], post_dict):
        HttpResponse(json.dumps({'message': 'Missing parameter member_id'}),
                     content_type='application/json', status=400)
    return delete_club_member(post_dict)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["POST"])
def settingsInterestedCreateRouter(request):
    """
    Allows board members to add people to the club.
    Expect input dictionary to be of the form
    {
        'first_name': _,
        'last_name': _,
        'formerBoardMember': _,
        'email': _
    }
    :param request:
    :return:
    """
    session_id = id_for_member(request.user.email)
    json_post_data = json.loads(request.body)
    p_first_name = json_post_data.get('first_name', '')
    p_last_name = json_post_data.get('last_name', '')
    p_formerBoardMember = json_post_data.get('formerBoardMember', False)
    p_email = json_post_data.get('email', None)
    if p_email is None:
        return HttpResponse(json.dumps({"message": "Missing required param email"}), status=400,
                            content_type='application/json')
    interested = Interested(p_first_name, p_last_name,
                            p_formerBoardMember, p_email)
    return add_interested(interested)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def settingsSchedulesRouter(request):
    """
    Allows board members to get the whole schedule and add to/edit/delete from schedule
    Expect input/output dictionary to be of the form
    {
        'schedule': [
            {
                'date': _,
                'number_of_courts': _
            },
            ...
        ]
    }
    :param request:
    :return:
    """
    session_id = id_for_member(request.user.email)
    if not is_board_member(session_id):
        return HttpResponse(json.dumps({"message": "You are not a board member."}),
                            content_type="application/json")
    if request.method == "GET":
        return schedule_to_dict()
    elif request.method == "POST":
        # INSERT or UPDATE
        # dict_post = dict(request.POST.items())
        print(request.body)
        json_post_data = json.loads(request.body.decode('utf8'))
        if not validate_keys(["schedule"], json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameter schedule'}),
                         content_type='application/json', status=400)
        return addto_edit_schedule(json_post_data)
    elif request.method == "DELETE":
        # The provided dictionary should ONLY contain information on the entries that are
        # intended to be deleted.
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        if not validate_keys(["schedule"], dict_delete):
            HttpResponse(json.dumps({'message': 'Missing parameter schedule'}),
                         content_type='application/json', status=400)
        return delete_multiple_from_schedule(dict_delete)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def settingsCourtRouter(request):
    """
    Allows board members to get the info on all courts and add/edit courts.
    Expect the input/output dictionary to be of the form
    {
        'courts': [
            {
                'court_id': _,
                'queue_id': _
            },
            ...
        ]
        'court_types': [str, ...]
    }
    :param request:
    :return:
    """
    session_id = id_for_member(request.user.email)
    if request.method == "GET":
        return get_all_courts_formmated()
    elif request.method == "POST":
        # Used to add new courts OR change the queue types for the courts
        json_post_data = request.POST
        if not validate_keys('courts', json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameter courts'}),
                         content_type='application/json', status=400)
        return addto_edit_courts_formatted(json_post_data)
    elif request.method == "DELETE":
        # The input dictionary should hold information ONLY for the courts to be deleted
        json_delete_data = json.loads(request.body.decode('utf8'))
        if not validate_keys('courts', json_delete_data):
            HttpResponse(json.dumps({'message': 'Missing parameter courts'}),
                         content_type='application/json', status=400)
        return delete_courts_formatted(json_delete_data)


@auth_decorator(allowed=MemberClass.BOARD_MEMBER)
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def settingsQueueRouter(request):
    """
    Allows boardmembers to get all the current queues in db or add more queue types
    Expect the input/output dictionary to be of the form
    {
        'queues': [
            {
                'queue_id': _,
                'queue_type': _
            },
            ...
        ]
    }
    :param request:
    :return:
    """
    session_id = id_for_member(request.user.email)
    if not is_board_member(session_id):
        return HttpResponse(json.dumps({"message": "You are not a board member."}),
                            content_type="application/json")
    if request.method == "GET":
        return get_all_queues_formatted()
    elif request.method == "POST":
        # Used to add more queue types to the db
        # dict_post = dict(request.POST.items()) <- For some reason, can't read POST dictionary from PostMan like this
        json_post_data = json.loads(request.body)
        if not validate_keys('queues', json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameter queues'}),
                         content_type='application/json', status=400)
        return add_queues_formatted(json_post_data)
    elif request.method == "DELETE":
        # The input dictionary should hold information ONLY for the queues to be deleted
        json_delete_data = json.loads(request.body)
        if not validate_keys('queues', json_delete_data):
            HttpResponse(json.dumps({'message': 'Missing parameter queues'}),
                         content_type='application/json', status=400)
        return delete_queues_formatted(json_delete_data)