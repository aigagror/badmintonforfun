import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from api import cursor

class ElectionTest(TestCase):
    def test_get_election(self):
        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.status_code, 200)
        print(response.content)

    def test_create_election(self):
        date = datetime.date(2018, 4, 1)
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor.serializeDatetime(date)})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:election'))
