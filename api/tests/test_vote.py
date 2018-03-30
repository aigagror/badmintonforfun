import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.tests.utils import create_election


class VotesTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_cast_votes(self):
        election, campaign, voter = create_election()

        response = self.client.post(reverse('api:vote'), {'voter': voter.id, 'campaign': campaign.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Vote successfully cast')

    def test_get_all_votes(self):
        response = self.client.get(reverse('api:all_votes'))
        self.assertEqual(len(response.json()), 0)

        self.test_cast_votes()

        response = self.client.get(reverse('api:all_votes'))
        self.assertEqual(len(response.json()), 1)