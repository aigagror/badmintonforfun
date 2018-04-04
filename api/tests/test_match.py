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
        response = self.client.post(reverse('api:create_match'), {"score_A": 21, "score_B": 23, "a_players": [6, 2], "b_players": [4, 5]},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(matches + 1, len(list(Match.objects.all())))
        self.assertEqual(playedin + 4, len(list(PlayedIn.objects.all())))

    def test_edit_match(self):
        self.test_create_match()
        self.assertEqual(len(list(Match.objects.all())), 1)
        m = Match.objects.get(id=0)
        response = self.client.post(reverse('api:edit_match'), {"id": 0, "score_A": 20, "score_B": 2})
        self.assertEqual(response.status_code, 200)
