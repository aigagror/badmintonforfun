import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *
import api.datetime_extension

class TournamentTest(CustomTestCase):

    @run(path_name='get_tournament', email=MEMBER, method=GET, args={})
    def test_get_tournament(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('tournament' in json)
        tournament = json['tournament']
        self.assertTrue('bracket_nodes' in tournament)
        bracket_nodes = tournament['bracket_nodes']
        for node in bracket_nodes:
            self.assertTrue('matches' in node)
            matches = node['matches']
            for match in matches:
                self.assertTrue('team_A' in match)
                self.assertTrue('team_B' in match)

    @run(path_name='create_tournament', email=BOARD_MEMBER, method=POST, args={'num_players': 4,
                                                                               'tournament_type': 'DOUBLES',
                                                                               'elimination_type': 'SINGLE'})
    def test_create_tournament(self):
        today = datetime.date.today()
        response = self.response
        self.assertGoodResponse(response)

        tournament = Tournament.objects.get(id=2)

        # make sure tournament was added
        self.assertEqual(tournament.date, today)
        self.assertEqual(tournament.match_type, "DOUBLES")
        self.assertEqual(len(list(Tournament.objects.all())), self.original_number_of_tournaments + 1)

        # make sure bracket nodes were added
        self.assertEqual(len(list(BracketNode.objects.all())), self.original_number_of_bracket_nodes + 1)

    @run(path_name='finish_tournament', email=BOARD_MEMBER, method=POST, args={"tournament_id": 1})
    def test_finish_tournament(self):
        today = datetime.date.today()
        response = self.response
        self.assertGoodResponse(response)

        tournament = Tournament.objects.get()
        self.assertEqual(tournament.endDate, today)

    @run(path_name='get_tournament_bracket_node', email=MEMBER, method=GET, args={'tournament_id': 1, 'level': 3, 'index': 0})
    def test_get_bracket_node(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('bracket_node' in json)
        self.assertTrue('matches' in json['bracket_node'])


    @run(path_name='get_tournament_bracket_node', email=MEMBER, method=GET,
         args={'tournament_id': 1, 'level': 5, 'index': 0})
    def test_get_bad_bracket_node(self):
        response = self.response
        self.assertBadResponse(response)

    @run(path_name='get_tournament_bracket_node', email=MEMBER, method=GET,
         args={'tournament_id': 1, 'level': 2, 'index': 9})
    def test_get_bad_bracket_node_2(self):
        response = self.response
        self.assertBadResponse(response)


    @run(path_name='add_match_to_bracket_node', email=BOARD_MEMBER, method=POST,
         args={'bracket_node_id': 5, 'team_A': '1,2', 'team_B': '3,4'})
    def test_add_match_to_bracket_node(self):
        """
        Start a new match on bracket node with given players
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)
        all_matches = Match.objects.all()
        self.assertEqual(self.original_number_of_matches + 1, len(list(all_matches)))

    @run(path_name='add_member_to_tournament', email=BOARD_MEMBER, method=POST,
         args={'member_id': 2})
    def test_add_member_to_tournament(self):
        response = self.response
        self.assertGoodResponse(response)

        member = Member.objects.get(id=2)
        self.assertTrue(member.in_tournament)

    @run(path_name='add_member_to_tournament', email=BOARD_MEMBER, method=POST,
         args={'member_id': 3})
    def test_add_bad_member_to_tournament(self):
        """
        Eddie is already in a tournament
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        member = Member.objects.get(id=3)
        self.assertTrue(member.in_tournament)

        json = response.json()
        self.assertEqual(json['message'], 'Member is already in a tournament')

    @run(path_name='remove_member_from_tournament', email=BOARD_MEMBER, method=POST,
         args={'member_id': 3})
    def test_remove_member_from_tournament(self):
        response = self.response
        self.assertGoodResponse(response)

        member = Member.objects.get(id=3)
        self.assertFalse(member.in_tournament)

    @run(path_name='remove_member_from_tournament', email=BOARD_MEMBER, method=POST,
         args={'member_id': 2})
    def test_remove_bad_member_from_tournament(self):
        """
        Member (2) was never in a tournament
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        member = Member.objects.get(id=2)
        self.assertFalse(member.in_tournament)

        json = response.json()
        self.assertEqual(json['message'], 'Member was not in a tournament to begin with')


    @run(path_name='get_tournament_members', email=MEMBER, method=GET, args={})
    def test_get_tournament_members(self):
        response = self.response

        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('tournament_members' in json)
        tournament_members = json['tournament_members']
        self.assertGreaterEqual(len(tournament_members), 0)

        first_tournament_member = tournament_members[0]

        self.assertTrue('member_id' in first_tournament_member)
        self.assertTrue('first_name' in first_tournament_member)
        self.assertTrue('last_name' in first_tournament_member)