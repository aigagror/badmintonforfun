from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .home_api import *

def index(request):
    return render(request, 'index.html')

def home(request):
    announcements = get_announcements()

    profile = get_member('ezhuang2@illinois.edu')

    context = {
        'announcements': announcements,
        'profile': profile,
        'stats': None,
        'matches': None,
    }
    return render(request, 'home.html', context)

def elections(request):

    return render(request, 'elections.html')

def settings(request):
    return render(request, 'settings.html')
