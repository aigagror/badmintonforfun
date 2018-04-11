import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class QueueTest(CustomTestCase):

    @run(path_name="get_queues", permission=MEMBER, method=GET, args={})
    def test_get_queues(self):
        response = self.client.get(reverse('api:get_queues'))
        self.assertGoodResponse(response)
        json = response.json()
        self.assertEqual(json['queues'][0]['type'], 'CASUAL')

    @run(path_name="create_queue", permission=BOARD_MEMBER, method=POST, args={'queue_type': 'CASUAL'})
    def test_create_queue(self):
        response = self.response
        self.assertGoodResponse(response)

        queues = Queue.objects.all()
        self.assertEqual(len(list(queues)), 1)
        queue = queues[0]
        self.assertEqual(queue.type, 'CASUAL')

        # Cannot create another queue of the same type
        response = self.client.post(reverse('api:create_queue'), {'queue_type': 'CASUAL'})
        self.assertBadResponse(response)
