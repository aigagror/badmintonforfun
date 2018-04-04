import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class TournamentTest(CustomTestCase):
    def test_get_tournament(self):
        response = self.client.get(reverse('api:get_tournament'))
        self.assertBadResponse(response)

        json = response.json()
        self.assertEqual(json['message'], 'No tournament going on')

        self.create_example_data()