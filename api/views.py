from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from api.api.home import *
from api.api.election import *
from api.api.settings import *
from api.api.match import *
from django.views.decorators.csrf import csrf_exempt


def restrictRouter(allowed=list(), incomplete=list()):
    def _restrictRouter(func):
        def _func(request, *args, **kwargs):
            if request.method in incomplete:
                return HttpResponse("Coming soon!", status=501)
            elif request.method not in allowed:
                return HttpResponse("Invalid request verb {}".format(request.method), status=400)
            else:
                return func(request, *args, **kwargs)

        return _func
    return _restrictRouter

@restrictRouter(incomplete=["GET", "POST"])
def announcements(request):
    """
    GET - Get the 3 latest announcements
    POST - Edit an announcement
    :param request:
    :return:
    """
    foo = 0

@restrictRouter(incomplete=["POST"])
def create_announcement(request):
    """
    POST - Creates an announcement
    :param request:
    :return:
    """
    foo = 0

@restrictRouter(allowed=["GET"])
def top_players(request):
    """
    GET -- Gets the top 5 players
    :param request:
    :return:
    """
    return get_top_players()


@restrictRouter(allowed=["GET", "POST"])
def vote(request):
    """
    GET -- Gets votes of given member
    POST -- Casts/updates a vote for the current election
    :param request:
    :param job:
    :return:
    """

    if request.method == "GET":
        dict_get = dict(request.GET.items())
        emailKey = "email"
        if emailKey not in dict_get:
            return HttpResponse("Missing required param {}".format(emailKey), status=400)
        email = dict_get[emailKey]
        return get_votes_from_member(email)
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        voterKey = "voter"
        electionKey = "electionDate"
        voteeKey = "votee"
        keys = [voterKey, electionKey, voteeKey]
        for key in keys:
            if key not in dict_post:
                return HttpResponse("Missing required param {}".format(key), status=400)

        voterEmail = dict_post[voterKey]
        voteeEmail = dict_post[voteeKey]
        electionDate = deserializeDate(dict_post[electionKey])
        return cast_vote(voterEmail, electionDate, voteeEmail)

@restrictRouter(allowed=["GET"])
def all_votes(request):
    return get_all_votes()

@restrictRouter(allowed=["GET", "POST", "DELETE"])
def campaignRouter(request):
    """
    GET -- Gets all campaigns of current election
    POST -- Edits a campaign
    :param request:
    :return:
    """
    if request.method == "GET":
        return get_current_campaigns()
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        validate_keys(["job", "pitch", "email"], dict_post)
        return edit_campaign(dict_post)
    elif request.method == "DELETE":
        # django doesn't have anything that handles delete so...
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        validate_keys(["job", "email"], dict_delete)
        return delete_campaign(dict_delete["email"], dict_delete["job"])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignFindRouter(request):
    dict_post = dict(request.POST.items())
    validate_keys(["job", "email"], dict_post)
    return get_campaign(dict_post["email"], dict_post["job"])


@csrf_exempt
@restrictRouter(allowed=["POST"])
def campaignCreateRouter(request):
    """
    POST -- Creates an campaign
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    jobKey = "job"
    pitchKey = "pitch"
    email = "email"

    keys = [jobKey, pitchKey, email]

    validate_keys(keys, dict_post)

    campaign_dict = {
        "job": dict_post[jobKey],
        "pitch": dict_post[pitchKey],
        "email": dict_post[email],
    }
    return start_campaign(campaign_dict)


def validate_keys(keys, validate_dict):
    for key in keys:
        if key not in validate_dict:
            return HttpResponse("Missing required param {}".format(key), status=400)

@restrictRouter(allowed=["GET", "POST"])
def settingsRouter(request):
    """
    Allow members to get and edit their own settings.
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    if request.method == "GET":
        dict_get = dict(request.GET.items())
        email = dict_get.get('email', '')
        return member_config(email)
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        email = dict_post.get('email', '')
        return member_config_edit(email, dict_post)


@restrictRouter(allowed=["GET"])
def settingsBoardMemberRouter(request):
    """
    Allow board members to get boardmember-exclusive-info in settings
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    dict_get = dict(request.GET.items())
    email = dict_get.get('email', '')
    if not is_board_member(email):
        return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
                            content_type="application/json")

    if request.method == "GET":
        return board_member_config()


@restrictRouter(allowed=["POST"])
def settingsPromoteMemberRouter(request):
    """
    Allow board members to promote interested->member, member->board member (Removed board member check for testing)
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")
    if request.method == "POST":
        dict_post = dict(request.POST.items())
        p_email = dict_post.get('email', '')
        # Member info
        p_level = dict_post.get('level', 0)
        p_private = dict_post.get('private', False)
        p_dateJoined = dict_post.get('dateJoined', '')
        p_bio = dict_post.get('bio', '')
        # Board member info
        p_job = dict_post.get('job', '')
        if p_email == '':
            return HttpResponse("Missing required param email", status=400)
        if not p_dateJoined:
            if not p_job:
                return HttpResponse("Missing required param member info or boardmember info", status=400)
            else:
                board_member = BoardMember(p_job)
                return promote_to_board_member(p_email, board_member)
        else:
            member = Member(p_level, p_private, p_dateJoined, p_bio)
            return promote_to_member(p_email, member)


@restrictRouter(allowed=["POST", "DELETE"])
def settingsEditMemberRouter(request):
    """
    Allow board members to edit information of a member OR remove them from the club
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")

    if request.method == "POST":
        dict_post = dict(request.POST.items())
        p_email = dict_post.get('email', '')
        if p_email == '':
            return HttpResponse("Missing required param email", status=400)

        p_attr_to_change = dict_post.get('attr_to_change', '')
        p_new_value = dict_post.get('new_value', '')
        if p_attr_to_change == '' or p_new_value == '' or p_email:
            return HttpResponse("Missing required param attr_to_change or new_value", status=400)

        if is_board_member(p_email):
            return edit_boardmember_info(p_email, p_new_value)  # only attribute to edit is 'job'
        else:
            return edit_member_info(p_email, p_attr_to_change, p_new_value)

    elif request.method == "DELETE":
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        validate_keys(["email"], dict_delete)
        return remove_member(dict_delete['email'])

    dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
    validate_keys(["job", "email"], dict_delete)
    return delete_campaign(dict_delete["email"], dict_delete["job"])


@restrictRouter(allowed=["POST"])
def settingsInterestedCreateRouter(request):
    """
    Allows board members to add people to the club. (Removed the board member check for testing)
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")

    dict_post = dict(request.POST.items())
    if request.method == "POST":
        p_first_name = dict_post.get('first_name', '')
        p_last_name = dict_post.get('last_name', '')
        p_formerBoardMember= dict_post.get('formerBoardMember', False)
        p_email = dict_post.get('email', '')
        if not p_email:
            return HttpResponse("Missing required param interested_info", status=400)
        interested = Interested(p_first_name, p_last_name,
                                p_formerBoardMember, p_email)
        return add_interested(interested)


@restrictRouter(allowed=["GET", "POST", "DELETE"])
def settingsSchedulesRouter(request):
    """
    Allows board members to get the whole schedule and add to/edit/delete from schedule
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")
    dict_post = dict(request.POST.items())
    if request.method == "GET":
        schedule = get_schedule()
        if schedule:
            # Convert date format to be JSON serializable
            for s in schedule:
                s.__setitem__('date', s.get('date').strftime('%Y-%m-%dT%H:%M:%SZ'))
            context = {'status': 'up', 'schedule': schedule}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "down", "message": "There is nothing in the schedule."}),
                                content_type="application/json")
    elif request.method == "POST":
        # INSERT or UPDATE
        p_date = dict_post.get('date', '')
        p_number_of_courts = dict_post.get('number_of_courts', 0)

        if p_date == '':
            return HttpResponse("Missing required param date", status=400)

        if schedule_date_exists(p_date):
            return edit_schedule(p_date, p_number_of_courts)
        else:
            return add_to_schedule(p_date, p_number_of_courts)
    elif request.method == "DELETE":
        dict_delete = json.loads(request.body.decode('utf8').replace("'", '"'))
        validate_keys(["date"], dict_delete)
        return delete_from_schedule(dict_delete["date"])


@restrictRouter(allowed=["GET", "POST"])
def settingsCourtRouter(request):
    """
    Allows board members to get the info on all courts and add/edit courts
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")
    if request.method == "GET":
        courts = get_all_courts()
        if courts:
            context = {'status': 'up', 'courts': courts}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "down", "message": "There are no courts stored in the database."}),
                                content_type="application/json")
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        p_court_id = dict_post.get('court_id', '')
        validate_keys('court_id', dict_post)
        if court_id_exists(p_court_id):
            p_attr_to_change = dict_post.get('attr_to_change', '')  # 'queue_id', 'number', or 'id'
            p_new_value = dict_post.get('new_value', '')
            validate_keys({'attr_to_change', 'new_value'}, dict_post)
            return edit_court_info(p_court_id, p_attr_to_change, p_new_value)
        else:
            p_number = dict_post.get('number', 0)
            p_queue_type = dict_post.get('queue', '')
            validate_keys({'number', 'queue'}, dict_post)
            return add_court(Court(p_court_id, p_number, p_queue_type))

@restrictRouter(allowed=["GET"])
def settingsAvailableCourtsRouter(request):
    """
    Allows board members to get the available courts on a certain day from the schedule
    :param request:
    :return:
    """
    # email = request.session.get('email', '')
    email = 'ezhuang2@illinois.edu'
    if not is_board_member(email):
        return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
                            content_type="application/json")
    if request.method == "GET":
        dict_post = dict(request.GET.items())
        g_date = dict_post.get('date', '')
        if g_date == '':
            return HttpResponse("Missing required param date", status=400)
        return get_available_courts(g_date)


@restrictRouter(allowed=["GET", "POST"])
def settingsQueueRouter(request):
    # email = request.session.get('email', '')
    # email = 'ezhuang2@illinois.edu'
    # if not is_board_member(email):
    #     return HttpResponse(json.dumps({"status": "down", "message": "You are not a board member."}),
    #                         content_type="application/json")
    if request.method == "GET":
        queues = get_all_queues()
        if queues:
            context = {'status': 'up', 'queues': queues}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "down", "message": "There are no queues."}),
                                content_type="application/json")
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        p_queue_type = dict_post.get('queue_type', '')
        validate_keys('queue_type', dict_post)
        return add_queue(p_queue_type)


@csrf_exempt
@restrictRouter(allowed=["GET", "POST"], incomplete=["DELETE"])
def electionRouter(request):
    """
    GET -- Gets the current election
    POST -- Edits an election
    :param request:
    :return:
    """
    if request.method == "GET":
        return current_election()
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        startKey = "startDate"
        endKey = "endDate"
        if startKey not in dict_post:
            return HttpResponse("Missing required param {}".format(startKey), status=400)
        startDate = deserializeDate(dict_post[startKey])
        endDate = dict_post.get(endKey, None)
        if endDate != None:
            endDate = deserializeDate(endDate)
        return edit_election(startDate, endDate)

@csrf_exempt
@restrictRouter(allowed=["POST"])
def electionCreateRouter(request):
    """
    POST -- Creates an election
    :param request:
    :return:
    """
    dict_post = dict(request.POST.items())
    startKey = "startDate"
    if startKey not in dict_post:
        return HttpResponse("Missing required param {}".format(startKey), status=400)
    startDate = deserializeDate(dict_post[startKey])
    return start_election(startDate)


class Interested(object):
    first_name = ''
    last_name = ''
    formerBoardMember = False
    email = ''

    def __init__(self, first_name, last_name, formerBoardMember, email):
        self.first_name = first_name
        self.last_name = last_name
        self.formerBoardMember = formerBoardMember
        self.email = email


class Member(object):
    level = ''
    private = False
    dateJoined = ''
    # queue = ''
    bio = ''

    def __init__(self, level, private, dateJoined, bio):
        self.level = level
        self.private = private
        self.dateJoined = dateJoined
        # self.queue = queue
        self.bio = bio


class BoardMember(object):
    job = ''

    def __init__(self, job):
        self.job = job


class Court(object):
    id = ''
    number = ''
    queue = ''

    def __init__(self, id, number, queue):
        self.id = id
        self.number = number
        self.queue = queue


def settings(request):
    #remove_member('johndoe@email.com')
    add_interested(Interested('John', 'Doe', False, 'johndoe@email.com'))
    new_member_info = Member(0, False, '2018-03-20', 'My name is John Doe and I like badminton')
    promote_to_member('johndoe@email.com', new_member_info)
    #promote_to_board_member('johndoe@email.com', BoardMember('Test Job'))

    #edit_member_info('johndoe@email.com', 'private', True)
    #edit_bio('johndoe@email.com', 'edit 2')
    #edit_privacy('johndoe@email.com', False)

    #remove_member('johndoe@email.com')

    board_members = get_board_members()
    members = get_members()
    interested = get_interested()
    member_info = get_member_info('ezhuang2@illinois.edu')
    print(member_info[0].__getitem__('dateJoined'))
    member_info[0].__setitem__('dateJoined', member_info[0].__getitem__('dateJoined').strftime('%Y-%m-%dT%H:%M:%SZ'))

    #add_to_schedule('2018-03-21', 8)
    #edit_schedule('2018-03-21', 2)
    #delete_from_schedule('2018-03-21')
    schedule = get_schedule()

    add_queue('CASUAL')
    add_queue('RANKED')
    add_queue('KOTH')

    add_court(Court(1, 4, 'CASUAL'))
    add_court(Court(2, 2, 'RANKED'))
    add_court(Court(3, 8, 'CASUAL'))
    add_court(Court(4, 4, 'KOTH'))
    add_court(Court(5, 2, 'RANKED'))
    add_court(Court(6, 2, 'RANKED'))
    add_court(Court(7, 2, 'RANKED'))
    add_court(Court(8, 2, 'RANKED'))

    check_court_date = '2018-03-31'
    available_courts = {'date': check_court_date, 'courts': get_available_courts(check_court_date)}

    edit_court_info(1, 'queue_id', 'KOTH')
    all_courts = get_all_courts()

    is_bm = is_board_member('apoddar3@illinois.edu')

    context = {
        'board_members': board_members,
        'members': members,
        'interested': interested,
        'member_info': member_info,
        'schedule': schedule,
        'available_courts': available_courts,
        'all_courts': all_courts,
        'is_bm': is_bm
    }

    return render(request, 'api_settings.html', context)
