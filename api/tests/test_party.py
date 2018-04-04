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
        response = self.client.get(reverse('api:get_party_for_member'), {'member_id': eddie.id})
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('party_id' in json)

    def test_get_no_party(self):
        some_guy = Member(first_name='some', last_name='guy', dateJoined=datetime.date.today(), email='someguy@gmail.com')
        some_guy.save()

        response = self.client.get(reverse('api:get_party_for_member'), {'member_id': some_guy.id})

        json = response.json()
        self.assertTrue('party_id' not in json)

    def test_add_member_to_party(self):
        self.create_example_data()

        parties = Party.objects.all()

        self.assertGreaterEqual(len(list(parties)), 2)

        some_guy = Member(first_name='some', last_name='guy', dateJoined=datetime.date.today(),
                         email='someguy@gmail.com')
        some_guy.save()

        first_party = parties[0]
        second_party = parties[1]

        response = self.client.post(reverse('api:party_add_member'), {'party_id': first_party.id, 'member_id': some_guy.id})
        self.assertGoodResponse(response)

        guys_in_first_party = Member.objects.filter(party_id=first_party.id)
        self.assertEqual(len(list(guys_in_first_party)), 2)

    def test_remove_member_from_party(self):
        self.create_example_data()

        parties = Party.objects.all()

        self.assertGreaterEqual(len(list(parties)), 2)

        number_of_parties_before_removal = len(list(parties))

        first_party = parties[0] # This party only has one member (Eddie). Removing Eddie from the party should remove the party
        second_party = parties[1] # This party has two members(Bhuvan and Dan). Removing Bhuvan should just leave Dan in the party

        eddie = Member.objects.get(email='ezhuang2@illinois.edu')
        bhuvan = Member.objects.get(email='bhuvan2@illinois.edu')

        response = self.client.post(reverse('api:party_remove_member'), {'party_id': first_party.id, 'member_id': eddie.id})
        self.assertGoodResponse(response)

        parties = Party.objects.all()
        self.assertEqual(len(list(parties)), number_of_parties_before_removal - 1)

        response = self.client.post(reverse('api:party_remove_member'), {'party_id': second_party.id, 'member_id': bhuvan.id})
        self.assertGoodResponse(response)
        parties = Party.objects.all()
        self.assertEqual(len(list(parties)), number_of_parties_before_removal - 1)

        members_of_second_party = Member.objects.filter(party=second_party)
        self.assertEqual(len(list(members_of_second_party)), 1)
        self.assertEqual(members_of_second_party[0].first_name, 'Dan')




