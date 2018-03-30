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

from api.routers import demo, router, votes_router, \
    settings_router, match_router, election_router, \
    campaign_router, announcement_router, queue_router

app_name = 'api'
urlpatterns = [

    re_path(r'demo/matches/?$', demo.matches, name='demo_matches'),
    re_path(r'demo/matches/create/?$', demo.create_match, name='demo_matches_create'),
    re_path(r'demo/matches/delete/?$', demo.delete_match, name='demo_matches_delete'),
    path('demo/matches/<int:match_id>/edit/', demo.edit_match, name='demo_matches_edit'),
    re_path(r'demo/players/top/?$', demo.top_players, name='demo_top_players'),

    re_path(r'demo/election/?$', demo.index, name='demo_election'),
    re_path(r'demo/election/vote/?$', demo.vote, name='demo_vote'),

    # Gets the 3 latest announcements | Edits an announcement
    re_path(r'announcements/?$', announcement_router.announcements, name='announcement'),
    # Creates an announcement
    re_path(r'announcements/create/?$', announcement_router.create_announcement, name='create_announcement'),

    # Gets the top players
    re_path(r'members/top_players?$', match_router.top_players, name='top_players'),

    # Gets all votes
    re_path(r'election/all_votes/?$', votes_router.all_votes, name='all_votes'),
    # Create/edit/delete votes
    re_path(r'election/vote/?$', votes_router.vote, name='vote'),
    # Creates an election
    re_path(r'election/create/?$', election_router.electionCreateRouter, name='create_election'),
    # Gets current election and all of its campaigns
    re_path(r'election/?$', election_router.electionRouter, name='election'),

    # Creates a campaign
    re_path(r'campaign/create/?$', campaign_router.campaignCreateRouter, name='create_campaign'),
    # Edits campaign
    re_path(r'campaign/?$', campaign_router.campaignRouter, name='campaign'),

    re_path(r'settings/member/?$', settings_router.settingsRouter, name='member_settings'),
    re_path(r'settings/boardmembers/?$', settings_router.settingsBoardMemberRouter, name='boardmembers'),
    re_path(r'settings/members/all?$', settings_router.settingsAllMembersRouter, name='all_members'),
    re_path(r'settings/interested/add/?$', settings_router.settingsInterestedCreateRouter, name='add_interested'),
    re_path(r'settings/schedule/?$', settings_router.settingsSchedulesRouter, name='schedule'),
    re_path(r'settings/courts/?$', settings_router.settingsCourtRouter, name='courts'),
    re_path(r'settings/queue/?$', settings_router.settingsQueueRouter, name='queue'),

    re_path(r'queue/party/next?$', queue_router.next_on_queue, name='queue_next_party'),
    re_path(r'queue/')

]

