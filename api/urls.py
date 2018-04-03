"""badminton_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see
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

import api.routers.party_router
from api.routers import demo, router, votes_router, \
    settings_router, match_router, election_router, \
    campaign_router, announcement_router, queue_router

app_name = 'api'
urlpatterns = [

    # Front-end demonstrations of backend functions
    re_path(r'demo/?$', demo.index, name='demo_index'),
    re_path(r'demo/matches/?$', demo.matches, name='demo_matches'),
    re_path(r'demo/matches/create/?$', demo.create_match, name='demo_matches_create'),
    re_path(r'demo/matches/delete/?$', demo.delete_match, name='demo_matches_delete'),
    path('demo/matches/<int:match_id>/edit/', demo.edit_match, name='demo_matches_edit'),
    re_path(r'demo/players/top/?$', demo.top_players, name='demo_top_players'),

    re_path(r'demo/election/?$', demo.index, name='demo_election'),
    re_path(r'demo/election/vote/?$', demo.vote, name='demo_vote'),

    re_path(r'demo/queue/?$', demo.queue, name='demo_queue'),
    path('demo/queue/party/<int:party_id>/', demo.edit_party, name='demo_edit_party'),

    # Gets the 3 latest announcements | Edits an announcement
    re_path(r'announcements/?$', announcement_router.announcements, name='announcement'),
    # Creates an announcement
    re_path(r'announcements/create/?$', announcement_router.create_announcement, name='create_announcement'),

    # Gets the top players
    re_path(r'members/top_players?$', match_router.top_players, name='top_players'),

    # Gets all votes
    path('election/vote/get/<int:voter_id>/', votes_router.get_votes_from_member, name='get_votes_from_member'),
    re_path(r'election/all_votes/?$', votes_router.all_votes, name='get_all_votes'),
    # Create/edit/delete votes
    re_path(r'election/vote/?$', votes_router.cast_vote, name='cast_vote'),
    # Creates an election
    re_path(r'election/create/?$', election_router.electionCreateRouter, name='create_election'),
    # Gets current election and all of its campaigns
    re_path(r'election/get/?$', election_router.get_election, name='get_election'),
    re_path(r'election/edit/?$', election_router.edit_election, name='edit_election'),

    re_path(r'campaign/create/?$', campaign_router.create_campaign, name='create_campaign'),
    path('campaign/get/<int:campaigner_id>/', campaign_router.get_campaign_from_campaigner, name='get_campaign_from_campaigner'),
    re_path(r'campaign/get_all/?$', campaign_router.get_all_campaigns, name='get_all_campaigns'),
    # Edits campaign
    re_path(r'campaign/?$', campaign_router.campaignRouter, name='campaign'),

    re_path(r'settings/member/?$', settings_router.settingsRouter, name='member_settings'),
    re_path(r'settings/boardmembers/?$', settings_router.settingsBoardMemberRouter, name='boardmembers'),
    re_path(r'settings/members/all/?$', settings_router.settingsAllMembersRouter, name='all_members'),
    re_path(r'settings/interested/add/?$', settings_router.settingsInterestedCreateRouter, name='add_interested'),
    re_path(r'settings/schedule/?$', settings_router.settingsSchedulesRouter, name='schedule'),
    re_path(r'settings/courts/?$', settings_router.settingsCourtRouter, name='court_settings'),
    re_path(r'settings/queues/?$', settings_router.settingsQueueRouter, name='queue_settings'),

    # Gets the queues with all the parties on them
    re_path(r'queue/?$', queue_router.get_queues, name='get_queues'),

    #Create a queue
    re_path(r'queue/create/?', queue_router.create_queue, name='create_queue'),
    # Creates a party
    re_path(r'queue/party/create/?$', api.routers.party_router.create_party, name='create_party'),
    # Edits/deletes a party
    re_path(r'queue/party/edit/?$', api.routers.party_router.edit_party, name='edit_party'),
    # Gets the next part on the queue
    re_path(r'queue/party/next/?$', queue_router.next_on_queue, name='queue_next_party'),
    re_path(r'queue/party/dequeue/?$', queue_router.dequeue_next_party_to_court, name='dequeue_next_party_to_court'),

]


