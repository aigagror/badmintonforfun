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
from api.calls.interested_call import get_member_class, id_for_member, MemberClass

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


@auth_decorator(allowed=MemberClass.MEMBER)
@restrictRouter(allowed=["GET", "POST", "DELETE"])
def settingsAllMembersRouter(request):
    """
    Allows boardmembers to get/edit/delete information on all the people in the club (interested, members, boardmembers)
    Expect input/output dictionary to be of the form
    {
        'members': [
            {
                'member_id': _, (Used for promoting/demoting/deletion)
                'first_name': _,
                'last_name': _,
                'email': _,
                'status': _ (Interested, Member, Boardmember)
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
        return get_all_club_members()
    elif request.method == "POST":
        # Promote/demote members (Interested, Member, Boardmember)
        # Going to Boardmember, the default 'job'='OFFICER'
        json_post_data = json.loads(request.body.decode('utf8').replace("'", '"'))
        if not validate_keys(["members"], json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameters members'}),
                         content_type='application/json', status=400)
        return update_all_club_members_status(json_post_data)
    elif request.method == "DELETE":
        # Here, the dictionary should ONLY contain the information for members that should be deleted
        # Remove people from the db completely
        # dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        json_delete_data = json.loads(request.body.decode('utf8').replace("'", '"'))
        if not validate_keys(["members"], json_delete_data):
            HttpResponse(json.dumps({'message': 'Missing parameter members'}),
                         content_type='application/json', status=400)
        return delete_multiple_club_members(json_delete_data)


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
    # session_id = request.session.get('session_id', None)
    session_id = id_for_member(request.user.email)
    if not is_board_member(session_id):
        return http_response({}, message="You are not a board member.")

    # dict_post = dict(request.POST.items())
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
    # session_id = request.session.get('session_id', None)
    session_id = id_for_member(request.user.email)
    if not is_board_member(session_id):
        return HttpResponse(json.dumps({"message": "You are not a board member."}),
                            content_type="application/json")
    if request.method == "GET":
        return schedule_to_dict()
    elif request.method == "POST":
        # INSERT or UPDATE
        # dict_post = dict(request.POST.items())
        json_post_data = json.loads(request.body)
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
    # session_id = request.session.get('session_id', None)
    session_id = id_for_member(request.user.email)
    if not is_board_member(session_id):
        return HttpResponse(json.dumps({"message": "You are not a board member."}),
                            content_type="application/json")
    if request.method == "GET":
        return get_all_courts_formmated()
    elif request.method == "POST":
        # Used to add new courts OR change the queue types for the courts
        json_post_data = json.loads(request.body)
        if not validate_keys('courts', json_post_data):
            HttpResponse(json.dumps({'message': 'Missing parameter courts'}),
                         content_type='application/json', status=400)
        return addto_edit_courts_formatted(json_post_data)
    elif request.method == "DELETE":
        # The input dictionary should hold information ONLY for the courts to be deleted
        json_delete_data = json.loads(request.body)
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
    # session_id = request.session.get('session_id', None)
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