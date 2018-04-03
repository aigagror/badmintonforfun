import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class QueueTest(CustomTestCase):
    def test_get_queues(self):
        response = self.client.get(reverse('api:get_queues'))
        json = response.json()
        self.assertEqual(json['message'], 'There are no queues.')

        # Create a queue
        self.create_example_data()

        response = self.client.get(reverse('api:get_queues'))
        self.assertGoodResponse(response)
        json = response.json()
        self.assertEqual(json['queues'][0]['type'], 'CASUAL')

    def test_create_queue(self):
        response = self.client.post(reverse('api:create_queue'), {'queue_type': 'CASUAL'})
        self.assertGoodResponse(response)

        queues = Queue.objects.all()
        self.assertEqual(len(list(queues)), 1)
        queue = queues[0]
        self.assertEqual(queue.type, 'CASUAL')

        # Cannot create another queue of the same type
        response = self.client.post(reverse('api:create_queue'), {'queue_type': 'CASUAL'})
        self.assertBadResponse(response)

    def test_next_party(self):
        self.create_example_data()
        response = self.client.get(reverse('api:queue_next_party'), {'type': 'CASUAL'})
        json = response.json()
        self.assertEqual(len(json['parties']), 2)

        # Test empty queue
        queue = Queue(type="KOTH")
        queue.save()
        response = self.client.get(reverse('api:queue_next_party'), {'type': 'KOTH'})
        json = response.json()
        self.assertEqual(len(json['parties']), 0)

    def test_dequeue_party(self):
        self.create_example_data()
        response = self.client.post(reverse('api:dequeue_next_party_to_court'), {'type': 'CASUAL'})




