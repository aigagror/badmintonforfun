from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .home_api import *
from .election_api import *

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

def elections(request):
    curr_campaigns = get__current_campaigns()
    campaign_json = get_campaign("apoddar3@illinois.edu", "Treasurer")
    no_campaign_json = get_campaign("apoddar3@illinois.edu", "President")

    context = {
        'campaigns': curr_campaigns,
        'foundCampaign': campaign_json,
        'noCampaign': no_campaign_json,

    }
    return render(request, 'elections.html', context)

def settings(request):
    return render(request, 'settings.html')
