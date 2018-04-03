import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class PartyTest(CustomTestCase):
    def test_get_party(self):
        self.create_example_data()
        eddie = Member.objects.get(first_name='Eddie')
        response = self.client.get(reverse('api:get_party_for_member', args=(eddie.id, )))
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('party' in json)

    def test_get_no_party(self):
        someGuy = Member(first_name='some', last_name='guy', dateJoined=datetime.date.today(), email='someguy@gmail.com')
        someGuy.save()

        response = self.client.get(reverse('api:get_party_for_member', args=(someGuy.id, )))

        json = response.json()
        self.assertTrue('party' not in json)






