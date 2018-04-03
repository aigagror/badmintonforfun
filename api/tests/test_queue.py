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
        self.assertGoodResponse(response)

        # There should now only be one party on CASUAL queue(bhuvan)
        # There should be a match with just Eddie on it on some court

        queue = Queue.objects.get(type='CASUAL')

        parties = Party.objects.filter(queue=queue)

        self.assertEqual(len(list(parties)), 1)

        matches = Match.objects.raw("SELECT * FROM api_match WHERE court_id NOT NULL")
        self.assertEqual(len(list(matches)), 1)

        expected_new_match = matches[0]

        playedins = PlayedIn.objects.filter(match=expected_new_match)
        self.assertEqual(len(list(playedins)), 1)






