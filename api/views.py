from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from .home_api import *
from .election_api import *
from .settings_api import *

def index(request):
    return render(request, 'index.html')

def home(request):
    email = 'ezhuang2@illinois.edu'

    announcements = get_announcements()
    profile = get_member(email)

    stats = get_stats(email)

    matches = get_matches(email)

    schedule = get_schedule()

    context = {
        # 'announcements': announcements,
        'profile': profile,
        'stats': stats,
        # 'matches': matches,
        # 'schedule': schedule
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

class Mini(object):
    email = ""
    pitch = ""
    job = ""
    def __init__(self, email, pitch, job):
        self.email = email
        self.pitch = pitch
        self.job = job

def elections(request):
    curr_campaigns = get_current_campaigns()
    campaign_json = get_campaign("apoddar3@illinois.edu", "Treasurer")
    no_campaign_json = get_campaign("apoddar3@illinois.edu", "President")

    insert_one = edit_campaign(Mini("ezhuang2@illinois.edu", "Hello I'm Eddie", "Treasurer"))
    after_insert = get_current_campaigns()

    edit_one = edit_campaign(Mini("ezhuang2@illinois.edu", "I've been edited again!", "Treasurer"))
    after_edit = get_current_campaigns()

    #delete_election = delete_current_election()
    new_election = edit_election("2018-10-03")
    new_election_w_end = edit_election("2019-03-05", "2019-03-20")

    election_list = get_all_elections()

    context = {
        'campaigns': curr_campaigns,
        'foundCampaign': campaign_json,
        'noCampaign': no_campaign_json,
        'insertResult': insert_one,
        'afterInserting': after_insert,
        'edit': edit_one,
        'afterEditing': after_edit,
        'deleted': delete_election,
        'oneElection': new_election,
        'twoElections': new_election_w_end,
        'elections': election_list
    }

    if request.method == "POST":
        dict_post = dict(request.POST.items())
        return edit_campaign(Mini(dict_post["email"], dict_post["pitch"], dict_post["job"]))


    else:
        return render(request, 'api_elections.html', context)


def campaignView(request):
    if request.method == "GET":
        return get_current_campaigns()

    # create a new campaign or edit a current campaign
    if request.method == "POST":
        dict_post = dict(request.POST.items())
        return edit_campaign(Mini(dict_post["email"], dict_post["pitch"], dict_post["job"]))

def electionView(request):
    if request.method == "GET":
        return get_all_elections()

    if request.method == "POST":
        dict_post = dict(request.POST.items())
        return edit_election(dict_post["date"], dict_post["endDate"])

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


class Queue(object):
    type = ''

    def __init__(self, type):
        self.type = type

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

    add_queue(Queue('CASUAL'))
    add_queue(Queue('RANKED'))
    add_queue(Queue('KOTH'))

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


def settings_view(request):
    # email = request.session['email']
    email = 'ezhuang2@illinois.edu'
    if request.method == 'GET':
        context = ''

        # Get this member's info
        my_info = get_member_info(email)
        # Convert 'dateJoined' attribute to be JSON serializable
        # datetime.datetime.utcnow().strftime(“ % Y - % m - % dT % H: % M: % SZ”)
        my_info[0].__setitem__('dateJoined', my_info[0].__getitem__('dateJoined').strftime('%Y-%m-%dT%H:%M:%SZ'))

        if is_board_member(email):
            # Get list of everybody (interested, members, boardmembers)
            board_members = get_board_members()
            members = get_members()
            for m in members:
                m.__setitem__('dateJoined', m.get('dateJoined').strftime('%Y-%m-%dT%H:%M:%SZ'))

            interested = get_interested()

            # Get schedule
            schedule = get_schedule()
            for s in schedule:
                s.__setitem__('date', s.get('date').strftime('%Y-%m-%dT%H:%M:%SZ'))
            all_courts = get_all_courts()
            all_queues = get_all_queues()

            context = {
                'board_members': board_members,
                'members': members,
                'interested': interested,
                'schedule': schedule,
                'all_courts': all_courts,
                'all_queues': all_queues
            }

        context['my_info'] = my_info
        return HttpResponse(json.dumps(context, indent=4, sort_keys=True), content_type="application/json")

    if request.method == 'POST':
        if is_board_member(email):
            dict_post = dict(request.POST.items())





def settings_available_courts(request):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    # If the date isn't specified, use today's date
    available_courts = get_available_courts(request.GET.get('date', today))
    context = {'available_courts': available_courts}

    return HttpResponse(json.dumps(context), content_type="application/json")
