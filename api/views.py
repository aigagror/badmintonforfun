from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .home_api import *
from .election_api import *

def index(request):
    return render(request, 'api_index.html')

def home(request):
    email = 'ezhuang2@illinois.edu'

    announcements = get_announcements()
    profile = get_member(email)

    stats = get_stats(email)

    matches = get_matches(email)

    context = {
        'announcements': announcements,
        'profile': profile,
        'stats': stats,
        'matches': matches,
    }

    return render(request, 'api_home.html', context)

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

    insert_one = start_campaign(Mini("ezhuang2@illinois.edu", "Hello I'm Eddie", "Treasurer"))
    after_insert = get__current_campaigns()

    edit_one = edit_campaign(Mini("ezhuang2@illinois.edu", "I've been edited - twice", "Treasurer"))
    after_edit = get__current_campaigns()
    context = {
        'campaigns': curr_campaigns,
        'foundCampaign': campaign_json,
        'noCampaign': no_campaign_json,
        'insertResult': insert_one,
        'afterInserting': after_insert,
        'edit': edit_one,
        'afterEditing': after_edit
    }

    return render(request, 'api_elections.html', context)

def settings(request):
    return render(request, 'api_settings.html')
