from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
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

    context = {
        'announcements': announcements,
        'profile': profile,
        'stats': stats,
        'matches': None,
    }

    return render(request, 'home.html', context)

class Mini(object):
    email = ""
    pitch = ""
    job = ""
    def __init__(self, email, pitch, job):
        self.email = email
        self.pitch = pitch
        self.job = job

def elections(request):
    curr_campaigns = get__current_campaigns()
    campaign_json = get_campaign("apoddar3@illinois.edu", "Treasurer")
    no_campaign_json = get_campaign("apoddar3@illinois.edu", "President")

    insert_one = edit_campaign(Mini("ezhuang2@illinois.edu", "Hello I'm Eddie", "Treasurer"))
    after_insert = get__current_campaigns()

    edit_one = edit_campaign(Mini("ezhuang2@illinois.edu", "I've been edited again!", "Treasurer"))
    after_edit = get__current_campaigns()

    delete_election = delete_current_election()
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

    return render(request, 'elections.html', context)

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
    date_joined = ''
    queue = None
    bio = ''

    def __init__(self, level, private, date_joined, queue, bio):
        self.level = level
        self.private = private
        self.date_joined = date_joined
        self.queue = queue
        self.bio = bio


class BoardMember(object):
    job = ''

    def __init__(self, job):
        self.job = job


def settings(request):
    board_members = get_board_members()
    members = get_members()
    interested = get_interested()
    context = {
        'board_members': board_members,
        'members': members,
        'interested': interested
    }

    return render(request, 'api_settings.html', context)

