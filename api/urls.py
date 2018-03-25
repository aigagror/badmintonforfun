"""badminton_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path, re_path
from . import views

app_name = 'api'
urlpatterns = [
    re_path(r'election/all_votes/?$', views.all_votes, name='all_votes'),
    re_path(r'election/create/?$', views.electionCreateRouter, name='create_election'),
    re_path(r'election/?$', views.electionRouter, name='election'),

    re_path(r'vote/?$', views.vote, name='vote'),

    re_path(r'campaign/?$', views.campaignRouter),
    re_path(r'campaign/create/?$', views.campaignCreateRouter),

    re_path(r'settings/member/?$', views.settingsRouter),
    re_path(r'settings/boardmember/?$', views.settingsBoardMemberRouter),
    re_path(r'settings/promote/?$', views.settingsPromoteMemberRouter),
    re_path(r'settings/member/edit/?$', views.settingsEditMemberRouter),
    re_path(r'settings/member/add/?$', views.settingsInterestedCreateRouter),
    re_path(r'settings/schedule/?$', views.settingsSchedulesRouter),
    re_path(r'settings/courts/?$', views.settingsCourtRouter),
    re_path(r'settings/courts/available/?$', views.settingsAvailableCourtsRouter),
    re_path(r'settings/queue/?$', views.settingsQueueRouter)
]

