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

        some_queue = json['queues'][0]

        self.assertTrue('type' in some_queue)
        self.assertTrue('parties' in some_queue)
        self.assertTrue('average_play_time' in some_queue)

