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
from django.urls import re_path, path, include

from api.routers import demo, router, votes_router, \
    settings_router, match_router, election_router, \
    campaign_router, announcement_router, queue_router, \
    party_router, tournament_router, member_router, rankings_router, \
    courts_router

announcements_paths = [
    # Gets the 3 latest announcements | Edits an announcement
    re_path(r'get/?$', announcement_router.get_announcements, name='get_announcements'),
    # Creates an announcement
    re_path(r'create/?$', announcement_router.create_announcement, name='create_announcement'),
    re_path(r'edit/?$', announcement_router.edit_announcement, name='edit_announcement'),
    re_path(r'delete/?$', announcement_router.delete_announcement, name='delete_announcement'),
]

members_paths = [
    re_path(r'all/?$', member_router.get_members, name='get_members'),
    re_path(r'profile/?$', member_router.get_profile, name='get_profile'),
    re_path(r'view_member_profile/?$', member_router.view_member_profile, name='view_member_profile'),
]

election_paths = [
    path('vote/get/<int:voter_id>/', votes_router.get_votes_from_member, name='get_votes_from_member'),
    re_path(r'vote/?$', votes_router.cast_vote, name='cast_vote'),
    re_path(r'all_votes/?$', votes_router.all_votes, name='get_all_votes'),

    re_path(r'create/?$', election_router.electionCreateRouter, name='create_election'),
    re_path(r'get/?$', election_router.get_election, name='get_election'),
    re_path(r'edit/?$', election_router.edit_election, name='edit_election'),
]

settings_paths = [
    re_path(r'member/?$', settings_router.settingsRouter, name='member_settings'),
    re_path(r'boardmembers/?$', settings_router.settingsBoardMemberRouter, name='boardmembers'),
    re_path(r'members/all/?$', settings_router.settingsAllMembersRouter, name='all_members'),
    re_path(r'members/all/delete/?$', settings_router.delete_member, name='delete_member'),
    re_path(r'interested/add/?$', settings_router.settingsInterestedCreateRouter, name='add_interested'),
    re_path(r'schedule/?$', settings_router.settingsSchedulesRouter, name='schedule'),
    re_path(r'courts/?$', settings_router.settingsCourtRouter, name='court_settings'),
    re_path(r'queues/?$', settings_router.settingsQueueRouter, name='queue_settings'),
]

campaign_paths = [
    re_path(r'create/?$', campaign_router.create_campaign, name='create_campaign'),
    path('get/<int:campaigner_id>/', campaign_router.get_campaign_from_campaigner, name='get_campaign_from_campaigner'),
    re_path(r'get_all/?$', campaign_router.get_all_campaigns, name='get_all_campaigns'),
    # Edits campaign
    path('', campaign_router.campaignRouter, name='campaign'),
]

match_paths = [
    re_path(r'edit/?$', match_router.edit_match, name='edit_match'),
    re_path(r'finish/?$', match_router.finish_match, name='finish_match'),
    re_path(r'join/?$', match_router.join_match, name='join_match'),
    re_path(r'leave/?$', match_router.leave_match, name='leave_match'),
    re_path(r'create/?$', match_router.start_match, name='start_match'),
    re_path(r'delete/?$', match_router.delete_match, name='delete_match'),
    re_path(r'get/?$', match_router.current_match, name='current_match'),
    re_path(r'all_matches_from_member/?$', match_router.all_matches_from_member, name='all_matches_from_member'),
    re_path(r'all/?$', match_router.all_matches, name='all_matches'),
]

queue_paths = [

    # Gets all the queues with all the parties sorted by priority
    path('', queue_router.get_queues, name='get_queues'),

    re_path(r'create/?', queue_router.create_queue, name='create_queue'),
    re_path(r'refresh/?', queue_router.refresh_queues, name='refresh_queues'),
]

party_paths = [
    re_path(r'get/?$', party_router.member_party, name='get_party_for_member'),
    # Creates a party
    re_path(r'create/?$', party_router.create_party, name='create_party'),
    # Edits/deletes a party
    re_path(r'delete/?$', party_router.delete_party, name='delete_party'),
    re_path(r'join/?$', party_router.join_party, name='join_party'),
    re_path(r'leave/?$', party_router.leave_party, name='leave_party'),
    re_path(r'remove_member/?$', party_router.remove_member, name='party_remove_member'),
    re_path(r'add_member/?$', party_router.add_member, name='party_add_member'),
    re_path(r'free_members/?$', party_router.get_free_members, name='get_free_members'),
]

tournament_paths = [
    re_path(r'create/?$', tournament_router.create_tournament_router, name='create_tournament'),
    re_path(r'bracket_node/?$', tournament_router.get_bracket_node, name='get_tournament_bracket_node'),
    
    re_path(r'add/match/?$', tournament_router.add_match, name='add_match_to_bracket_node'),
    re_path(r'finish/?$', tournament_router.finish_tournament_router, name='finish_tournament'),
    re_path(r'^$', tournament_router.get_tournament, name='get_tournament'),
]

rankings_paths = [
    re_path(r'level/?$', rankings_router.get_rankings_by_level, name='get_rankings_by_level'),
    re_path(r'winratio/?$', rankings_router.get_rankings_by_win_ratio, name='get_rankings_by_win_ratio'),
]

courts_paths = [
    re_path(r'^$', courts_router.get_courts, name='get_courts'),
]

"""
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
"""
import api.views as views

from django.conf.urls import url, include
from django.contrib import admin

app_name = 'api'
urlpatterns = [
    path('announcements/', include(announcements_paths)),
    path('members/', include(members_paths)),
    path('election/', include(election_paths)),
    path('queue/', include(queue_paths)),
    path('settings/', include(settings_paths)),
    path('campaign/', include(campaign_paths)),
    path('match/', include(match_paths)),
    path('party/', include(party_paths)),
    path('tournament/', include(tournament_paths)),
    path('mail/', views.mail),
    path('rankings/', include(rankings_paths)),
    path('courts/', include(courts_paths))
]
