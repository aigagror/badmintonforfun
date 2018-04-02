import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .utils import *


class ElectionTest(CustomTestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_get_election(self):
        response = self.client.get(reverse('api:get_election'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'No current election available') # No current election

        self.test_create_election()

        response = self.client.get(reverse('api:get_election'))
        json = response.json()
        election = json['election']
        self.assertEqual(election['date'], '2018-03-24')
        self.assertIsNone(election['endDate'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['status'], 'up')  # Now there is an election


    def test_edit_election(self):
        self.test_create_election()
        date = self.test_date
        endDate = datetime.date(2018, 5, 2)
        response = self.client.post(reverse('api:edit_election'), {'id': 1, 'startDate': cursor_api.serializeDate(date), 'endDate': cursor_api.serializeDate(endDate)})
        self.assertGoodResponse(response)

    def test_delete_election(self):
        election = Election(date=datetime.date.today())
        election.save()

        response = self.client.delete(reverse('api:edit_election'), {'id': election.id})
        self.assertEqual(response.status_code, 200)