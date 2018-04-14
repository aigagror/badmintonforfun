import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from .custom_test_case import *
from api.models import *


class VotesTest(CustomTestCase):

    @run(path_name='cast_vote', email=MEMBER, method=POST, args={'campaign': 1})
    def test_cast_votes(self):
        response = self.response
        self.assertGoodResponse(response)

    # def test_get_all_votes(self):
    #     response = self.client.get(reverse('api:get_all_votes'))
    #     json = response.json()
    #     self.assertEqual(json['message'], 'No current election available')
    #
    #     self.test_cast_votes()
    #
    #     response = self.client.get(reverse('api:get_all_votes'))
    #     json = response.json()
    #     votes = json['all_votes']
    #     self.assertEqual(len(votes), 1)