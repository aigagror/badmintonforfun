import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *
import json

class MatchTest(CustomTestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_match(self):
        matches = len(list(Match.objects.all()))
        playedin = len(list(PlayedIn.objects.all()))
        response = self.client.post(reverse('api:create_match'), {"score_A": 21, "score_B": 23, "a_players": [1, 2], "b_players": [3, 4]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(matches + 1, len(list(Match.objects.all())))
        self.assertEqual(playedin + 4, len(list(PlayedIn.objects.all())))

    def test_edit_match(self):
        self.test_create_match()
        self.create_example_data()
        m = Match.objects.get(id=0)
        self.assertEqual(str(m), "A['Eddie Huang', 'Bhuvan Venkatesh']-B['Daniel Rong', 'Grace Shen']:21-23")
        response = self.client.post(reverse('api:edit_match'), {"id": 0, "score_A": 19, "score_B": 21})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(Match.objects.get(id=0)), "A['Eddie Huang', 'Bhuvan Venkatesh']-B['Daniel Rong', 'Grace Shen']:19-21")

    def test_delete_match(self):
        self.test_create_match()
        self.create_example_data()
        matches = len(list(Match.objects.all()))
        playedin = len(list(PlayedIn.objects.all()))
        response = self.client.delete(reverse('api:delete_match'), {"id": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(matches - 1, len(list(Match.objects.all())))
        self.assertEqual(playedin - 4, len(list(PlayedIn.objects.all())))

    def test_find_match_by_member(self):
        self.test_create_match()
        self.create_example_data()
        response = self.client.get(reverse('api:get_match'), {"id": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["match_id"], 0)

    def test_finish_match(self):
        self.test_create_match()
        self.create_example_data()
        response = self.client.post(reverse('api:finish_match'), {"id": 0, "score_A": 23, "score_B": 21})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(Match.objects.get(id=0)), "A['Eddie Huang', 'Bhuvan Venkatesh']-B['Daniel Rong', 'Grace Shen']:23-21")