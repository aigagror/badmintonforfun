import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class QueueTest(CustomTestCase):

    @run(path_name="get_queues", email=MEMBER, method=GET, args={})
    def test_get_queues(self):
        response = self.response
        self.assertGoodResponse(response)
        json = response.json()

        self.assertTrue('queues' in json)

        self.assertGreaterEqual(len(json['queues']), 2)

        first_queue = json['queues'][0]
        self.assertTrue('type' in first_queue)
        self.assertTrue('parties' in first_queue)
        self.assertTrue(first_queue["type"] == "CASUAL")

        party_in_first_queue = first_queue['parties'][0]

        self.assertTrue('average_play_time' in party_in_first_queue)
        self.assertTrue('members' in party_in_first_queue)

        second_queue = json['queues'][1]
        self.assertTrue('type' in second_queue)
        self.assertTrue('parties' in second_queue)
        self.assertTrue(second_queue["type"] == "RANKED")


