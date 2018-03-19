from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .home_api import *

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
    return render(request, 'elections.html')

def settings(request):
    return render(request, 'settings.html')
