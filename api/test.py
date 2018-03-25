import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from api import cursor

class ElectionTest(TestCase):

    def test_create_election(self):
        date = datetime.date(2018, 3, 24)
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_get_election(self):
        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'down') # No current election

        self.test_create_election()

        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.json()['date'], '2018-03-24')
        self.assertIsNone(response.json()['endDate'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'up')  # Now there is an election


    def test_edit_election(self):
        self.test_create_election()
        date = datetime.date(2018, 3, 24)
        endDate = datetime.date(2018, 5, 2)
        response = self.client.post(reverse('api:election'), {'startDate': cursor.serializeDate(date), 'endDate': cursor.serializeDate(endDate)})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.json()['endDate'], '2018-05-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'up')  # Now there is an election

class VotesTest(TestCase):

    def test_get_all_votes(self):
        response = self.client.get(reverse('api:all_votes'))
        self.assertEqual(len(response.json()), 0)
