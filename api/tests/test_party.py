import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class PartyTest(CustomTestCase):

    @run(path_name="create_party", email=MEMBER, method=POST, args={'queue_type': 'CASUAL', 'member_ids': '2,3,4,5'})
    def test_create_bad_party(self):
        """
        According to the example data, 'Member' is already on a party, so this should return a bad response
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        parties = Party.objects.all()
        number_of_parties_after = len(list(parties))
        number_of_parties_before = len(list(self.original_parties))

        self.assertEqual(number_of_parties_after, number_of_parties_before)


    @run(path_name="create_party", email=GRACE, method=POST,
         args={'queue_type': 'CASUAL', 'member_ids': '2,3,4,5'})
    def test_create_party(self):
        """
        According to the example data, 'Grace' is not yet on a party, so this should be ok
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        parties = Party.objects.all()
        number_of_parties_after = len(list(parties))

        number_of_parties_before = len(list(self.original_parties))

        self.assertEqual(number_of_parties_after, number_of_parties_before + 1)


    @run(path_name="get_party_for_member", email=MEMBER, method=GET,
         args={})
    def test_get_party(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('party_id' in json)


    @run(path_name="get_party_for_member", email=GRACE, method=GET,
         args={})
    def test_get_no_party(self):
        response = self.response

        json = response.json()
        self.assertTrue('party_id' not in json)


    @run(path_name="party_add_member", email=MEMBER, method=POST,
         args={'member_id': 6})
    def test_add_member_to_party(self):
        """
        According to the example data, member_id 6 is Grace who is not yet in a party. So this is valid
        :return:
        """


    @run(path_name="party_add_member", email=MEMBER, method=POST,
         args={'member_id': 3})
    def test_add_bad_member_to_party(self):
        """
        According to the example data, member_id 3 is Eddie who is already in a party. So this is not valid
        :return:
        """


    @run(path_name="party_remove_member", email=DAN, method=POST,
         args={'member_id': 4})
    def test_remove_member_from_party(self):
        """
        According to the example data, member_id 4 is Bhuvan who is in a party with Dan. So this is not valid
        :return:
        """


    @run(path_name="delete_party", email=MEMBER, method=POST,
         args={})
    def test_delete_party(self):
        """
        According to the example data, member_id 4 is Bhuvan who is in a party with Dan. So this is not valid
        :return:
        """
        


