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

        self.assertEqual(self.original_number_of_parties, self.number_of_parties_now)


    @run(path_name="create_party", email=JARED, method=POST,
         args={'queue_type': 'CASUAL', 'member_ids': '8,9'})
    def test_create_party(self):
        """
        According to the example data, 'Grace' is not yet on a party, so this should be ok
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties + 1)


    @run(path_name='create_party', email=JARED, method=POST,
         args={'queue_type': 'RANKED', 'member_ids': '8,9'})
    def test_create_party_that_creates_a_match(self):
        """
        According to the example data, 'Jared' is not yet on a party and there is a free court associated with the ranked queue
        Therefore, there should be no new party and instead there should be a new match on one of the courts associated with the
        ranked queue
        :return:
        """

        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties)

        self.assertEqual(self.number_of_matches_now, self.original_number_of_matches + 1)

        ranked_queue = Queue.objects.get(type="RANKED")
        ranked_courts = Court.objects.filter(queue=ranked_queue)

        ongoing_ranked_match_exists = False
        for court in ranked_courts:
            match = Match.objects.get(court=court)
            if match is not None:
                ongoing_ranked_match_exists = True
                break


        self.assertTrue(ongoing_ranked_match_exists)


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
        response = self.response

        self.assertGoodResponse(response)

        grace = Member.objects.get(first_name='Grace')
        self.assertIsNotNone(grace.party)



    @run(path_name="party_add_member", email=MEMBER, method=POST,
         args={'member_id': 3})
    def test_add_bad_member_to_party(self):
        """
        According to the example data, member_id 3 is Eddie who is already in a party. So this is not valid
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

    @run(path_name='join_party', email=JARED, method=POST, args={'party_id': 3})
    def test_join_party(self):
        """
        Jared joined Member's party (id = 3)
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        member = Member.objects.get(first_name='Member')
        party = member.party

        jared = Member.objects.get(first_name='Jared')
        self.assertEqual(jared.party_id, party.id)

    @run(path_name='join_party', email=MEMBER, method=POST, args={'party_id': 2})
    def test_bad_join_party(self):
        """
        Member is already party of some party, so should fail and Member should remain in party 3
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties)

        # No party should be empty
        all_parties = Party.objects.all()
        for party in all_parties:
            party_members = Member.objects.filter(party=party)
            if len(list(party_members)) == 0:
                print(party.id)
            self.assertGreater(len(list(party_members)), 0)

        # Member should still be a part of some party
        member = Member.objects.get(first_name='Member')
        self.assertIsNotNone(member.party)

    @run(path_name='leave_party', email=MEMBER, method=POST, args={})
    def test_leave_party_that_removes_party(self):
        """
        Member has left his party. Since he was the only one in the party, this also deletes the party
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties - 1)

        member = Member.objects.get(first_name='Member')

        self.assertIsNone(member.party)

    @run(path_name='leave_party', email=BHUVAN, method=POST, args={})
    def test_leave_party(self):
        """
        Bhuvan has left the party which included Dan, which leaves Dan as a one man band
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties)

        bhuvan = Member.objects.get(first_name='Bhuvan')
        dan = Member.objects.get(first_name='Daniel')

        self.assertIsNone(bhuvan.party)

        self.assertIsNotNone(dan.party)



    @run(path_name="party_remove_member", email=DAN, method=POST,
         args={'member_id': 4})
    def test_remove_member_from_party(self):
        """
        According to the example data, member_id 4 is Bhuvan who is in a party with Dan. Dan removes Bhuvan from party
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        bhuvan = Member.objects.get(first_name='Bhuvan')
        self.assertIsNone(bhuvan.party_id)


    @run(path_name="delete_party", email=DAN, method=POST,
         args={})
    def test_delete_party(self):
        """
        Delete the party of 'Dan'. Bhuvan should then not be associated with a party because CASCADE
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_parties_now, self.original_number_of_parties - 1)

        bhuvan = Member.objects.get(first_name='Bhuvan')
        self.assertIsNone(bhuvan.party_id)

    @run(path_name="get_free_members", email=JARED, method=POST, args={})
    def test_get_free_members(self):
        """
        Gets the members who are not in a party and are not in an ongoing match and are not himself
        :return:
        """

        jared = Member.objects.get(first_name='Jared') # Should not see himself

        # These guys are in a party
        member = Member.objects.get(first_name='Member')
        eddie = Member.objects.get(first_name='Eddie')
        bhuvan = Member.objects.get(first_name='Bhuvan')
        dan = Member.objects.get(first_name='Daniel')

        # Grace is in an ongoing match
        grace = Member.objects.get(first_name='Grace')

        people_who_should_not_be_included = [jared, member, eddie, bhuvan, dan, grace]

        response = self.response
        self.assertGoodResponse(response)

        json = response.json()

        self.assertTrue('free_members' in json)

        free_members = json['free_members']

        # Obama and 'BoardMember' should at least be in here
        self.assertGreaterEqual(len(free_members), 2)

        for free_member in free_members:
            self.assertTrue('id' in free_member)
            self.assertTrue('first_name' in free_member)
            self.assertTrue('last_name' in free_member)

            first_names_of_people_who_should_not_be_included = [m.first_name for m in people_who_should_not_be_included]

            self.assertFalse(free_member['first_name'] in first_names_of_people_who_should_not_be_included)

        # Check that Barack is in here
        barack_is_free = False
        for free_member in free_members:
            first_name = free_member['first_name']
            if first_name == 'Barack':
                barack_is_free = True

        self.assertTrue(barack_is_free)






