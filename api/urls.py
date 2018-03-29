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
from django.urls import re_path, path

import api.routers.announcement_router
import api.routers.campaign_router
import api.routers.election_router
import api.routers.match_router
import api.routers.settings_router
import api.routers.votes_router
from api.routers import router
import api.routers.demo

app_name = 'api'
urlpatterns = [

    re_path(r'demo/matches/?$', api.routers.demo.matches, name='demo_matches'),
    re_path(r'demo/matches/create/?$', api.routers.demo.create_match, name='demo_matches_create'),
    re_path(r'demo/matches/delete/?$', api.routers.demo.delete_match, name='demo_matches_delete'),
    path('demo/matches/<int:match_id>/edit/', api.routers.demo.edit_match, name='demo_matches_edit'),
    re_path(r'demo/players/top/?$', api.routers.demo.top_players, name='demo_top_players'),

    re_path(r'demo/election/?$', api.routers.demo.index, name='demo_election'),
    re_path(r'demo/election/vote/?$', api.routers.demo.vote, name='demo_vote'),

    # Gets the 3 latest announcements | Edits an announcement
    re_path(r'announcements/?$', api.routers.announcement_router.announcements, name='announcement'),
    re_path(r'announcements/create/?$', api.routers.announcement_router.create_announcement, name='create_announcement'),
    re_path(r'members/top_players?$', api.routers.match_router.top_players, name='top_players'),

    # Gets all votes
    re_path(r'election/all_votes/?$', api.routers.votes_router.all_votes, name='all_votes'),
    # Create/edit/delete votes
    re_path(r'election/vote/?$', api.routers.votes_router.vote, name='vote'),
    # Createss a campaign
    re_path(r'election/create/?$', api.routers.election_router.electionCreateRouter, name='create_election'),
    # Gets current election and all of its campaigns
    re_path(r'election/?$', api.routers.election_router.electionRouter, name='election'),

    # Edits campaign
    re_path(r'campaign/?$', api.routers.campaign_router.campaignRouter, name='campaign'),
    # Creates a campaign
    re_path(r'campaign/create/?$', api.routers.campaign_router.campaignCreateRouter, name='create_campaign'),

    re_path(r'settings/member/?$', api.routers.settings_router.settingsRouter, name='member_settings'),
    re_path(r'settings/boardmembers/?$', api.routers.settings_router.settingsBoardMemberRouter, name='boardmembers'),
    re_path(r'settings/members/all?$', api.routers.settings_router.settingsAllMembersRouter, name='all_members'),
    re_path(r'settings/interested/add/?$', api.routers.settings_router.settingsInterestedCreateRouter, name='add_interested'),
    re_path(r'settings/schedule/?$', api.routers.settings_router.settingsSchedulesRouter, name='schedule'),
    re_path(r'settings/courts/?$', api.routers.settings_router.settingsCourtRouter, name='courts'),
    re_path(r'settings/queue/?$', api.routers.settings_router.settingsQueueRouter, name='queue'),

    re_path(r'queue/party/next?$', api.routers.settings_router.settingsQueueRouter, name='queue_next_party')

]

