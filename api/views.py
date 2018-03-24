from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from .home_api import *
from .election_api import *
from .settings_api import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
    email = 'ezhuang2@illinois.edu'

    announcements = get_announcements()
    profile = get_member(email)

    stats = get_stats(email)
    
    matches = get_matches(email)
    
    schedule = get_schedule()

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


def campaignRouter(request):
    if request.method == "GET":
        return get_current_campaigns()
    # create a new campaign or edit a current campaign
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        return edit_campaign(Mini(dict_post["email"], dict_post["pitch"], dict_post["job"]))
    elif request.method == "DELETE":
        pass
    else:
        return HttpResponse("Invalid request verb {}".format(request.method), status=400)

@csrf_exempt
def electionRouter(request):
    if request.method == "GET":
        return current_election()
    elif request.method == "POST":
        dict_post = dict(request.POST.items())
        startKey = "startDate"
        endKey = "endDate"
        if startKey not in dict_post:
            return HttpResponse("Missing required param {}".format(startKey), status=400)
        startDate = deserializeDateTime(dict_post[startKey])
        endDate = dict_post.get(endKey, None)
        if endDate != None:
            endDate = deserializeDateTime(endDate)
        return edit_election(startDate, endDate)
    elif request.method == "DELETE":
        return HttpResponse("Coming soon!", status=501)
    else:
        return HttpResponse("Invalid request verb {}".format(request.method), status=400)

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
    john_doe_attr = get_member_attr('johndoe@email.com', 'private')

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

    context = {
        'board_members': board_members,
        'members': members,
        'interested': interested,
        'john_doe_attr': john_doe_attr,
        'schedule': schedule,
        'available_courts': available_courts,
        'all_courts': all_courts
    }

    return render(request, 'api_settings.html', context)
