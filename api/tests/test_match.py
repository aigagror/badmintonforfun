import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *
from api.calls.match_call import *


class ElectionTest(CustomTestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_match(self):
        response = self.client.post(reverse('api:create_match'), {"score_A": 21, "score_B": 23, "a_players": [6, 2],
                                                                  "b_players": [4, 5]})
