# import datetime
#
# from django.test import TestCase
# from django.urls import reverse
#
# from api import cursor_api
# from api.models import *
# from .custom_test_case import *
# import api.datetime_extension
#
# class TournamentTest(CustomTestCase):
#     def test_get_tournament(self):
#         response = self.client.get(reverse('api:get_tournament'))
#         self.assertBadResponse(response)
#
#         json = response.json()
#         self.assertEqual(json['message'], 'No tournaments exist')
#
#         self.create_example_data()
#
#         response = self.client.get(reverse('api:get_tournament'))
#         self.assertGoodResponse(response)
#
#         json = response.json()
#         self.assertTrue('tournament' in json)
#         print(json['tournament'])
#
#     def test_create_tournament(self):
#         today = datetime.date.today()
#         response = self.client.post(reverse('api:create_tournament'), {'num_players': 4, 'tournament_type': 'Doubles'})
#         self.assertGoodResponse(response)
#
#         tournament = Tournament.objects.get(date=today)
#         self.assertEqual(tournament.date, today)
#
#     def test_finish_tournament(self):
#         today = datetime.date.today()
#         response = self.client.post(reverse('api:create_tournament'), {'num_players': 4, 'tournament_type': 'Doubles'})
#         self.assertGoodResponse(response)
#         tournament = Tournament.objects.get(id=0)
#         self.assertEqual(tournament.endDate, None)
#
#         response = self.client.post(reverse("api:finish_tournament"), {"tournament_id": 0})
#         self.assertGoodResponse(response)
#         tournament = Tournament.objects.get(id=0)
#         self.assertEqual(tournament.endDate, today)
#
#     def test_get_match_in_bracket_node(self):
#         self.create_example_data()
#
#         today = datetime.date.today()
#         tournament = Tournament.objects.get(date=today)
#
#         response = self.client.get(reverse('api:get_tournament_bracket_node'), {'tournament_id': tournament.id, 'level': 3, 'index': 0})
#         self.assertGoodResponse(response)
#
#         json = response.json()
#         self.assertTrue('bracket_node' in json)
#         self.assertTrue('match' in json['bracket_node'])
#
#     def test_get_no_match_in_bracket_node(self):
#         self.create_example_data()
#
#         today = datetime.date.today()
#         tournament = Tournament.objects.get(date=today)
#
#         response = self.client.get(reverse('api:get_tournament_bracket_node'),
#                                    {'tournament_id': tournament.id, 'level': 2, 'index': 0})
#         self.assertGoodResponse(response)
#
#         json = response.json()
#         self.assertTrue('bracket_node' in json)
#         self.assertTrue('match' in json['bracket_node'])
#         self.assertIsNone(json['bracket_node']['match'])
#
#     def test_get_bad_bracket_node(self):
#         self.create_example_data()
#
#         today = datetime.date.today()
#         tournament = Tournament.objects.get(date=today)
#
#         response = self.client.get(reverse('api:get_tournament_bracket_node'),
#                                    {'tournament_id': tournament.id, 'level': 5, 'index': 0})
#         self.assertBadResponse(response)
#
#         response = self.client.get(reverse('api:get_tournament_bracket_node'),
#                                    {'tournament_id': tournament.id, 'level': 2, 'index': 9})
#         self.assertBadResponse(response)
#
#     def test_add_match_to_tournament_bracket(self):
#         self.create_example_data()
#
#         today = datetime.date.today()
#         tournament = Tournament.objects.get(date=today)
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=2, sibling_index=0)
#         self.assertIsNone(bracket_node.match)
#
#         now = datetime.datetime.now(tz=api.datetime_extension.utc)
#         new_tournament_match = Match(startDateTime=now + datetime.timedelta(minutes=-10), scoreB=0, scoreA=0)
#         new_tournament_match.save()
#
#         response = self.client.post(reverse('api:add_match_to_tournament'), {'tournament_id': tournament.id,
#                                                                              'match_id': new_tournament_match.id,
#                                                                              'level': 2, 'index': 0})
#         self.assertGoodResponse(response)
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=2, sibling_index=0)
#
#         self.assertIsNotNone(bracket_node.match)
#
#     def test_finish_tournament_match(self):
#         """
#         If a match that is finished is associated with a tournament. There should be a check to see if we can add a new match up the bracket.
#         For example consider the case where there is a tournament bracket shaped as a perfect tree of height 1
#         with the left and right child having ongoing matches. If the left child's match was finished first, nothing should happen.
#         However, when the right child's match finishes, the tournament should automatically have added a match to the root node
#         where the members involved are those who have won the matches from that of the left and right childs' matches respectively
#         :return:
#         """
#
#         self.create_example_data()
#
#         today = datetime.date.today()
#         tournament = Tournament.objects.get(date=today)
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=3, sibling_index=0)
#         self.assertIsNotNone(bracket_node.match)
#         matchA = bracket_node.match
#
#         matchA.scoreA = 21
#         matchA.scoreB = 19
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=3, sibling_index=1)
#         self.assertIsNotNone(bracket_node.match)
#         matchB = bracket_node.match
#
#         matchB.scoreA = 21
#         matchB.scoreB = 19
#
#         matchA.save()
#         matchB.save()
#
#         response = self.client.post(reverse('api:finish_match'), {'id': matchA.id})
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=2, sibling_index=0)
#         self.assertIsNone(bracket_node.match)
#
#         response = self.client.post(reverse('api:finish_match'), {'id': matchB.id})
#
#         bracket_node = BracketNode.objects.get(tournament=tournament, level=2, sibling_index=0)
#         self.assertIsNotNone(bracket_node.match)