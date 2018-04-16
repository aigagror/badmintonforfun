import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from .custom_test_case import *
from api.models import *
from api.calls.election_call import delete_election


class VotesTest(CustomTestCase):

    @run(path_name='cast_vote', email=MEMBER, method=POST, args={'campaign_id': 1})
    def test_cast_votes(self):
        """
        Changing vote from Bhuvan to Eddie since they're both running for president
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        vote = Vote.objects.get(voter_id=2)
        self.assertEqual(vote.campaign_id, 1)

        self.assertEqual(self.original_number_of_votes, len(list(Vote.objects.all())))

    @run(path_name='cast_vote', email=MEMBER, method=POST, args={'campaign_id': 2})
    def test_update_cast_vote(self):
        response = self.response
        self.assertGoodResponse(response)

        # ensure that nothing changed from the first vote cast except the campaign id
        vote = Vote.objects.get(voter_id=2)
        self.assertEqual(vote.campaign_id, 2)
        self.assertEqual(self.original_number_of_votes, len(list(Vote.objects.all())))

    @run(path_name='cast_vote', email=MEMBER, method=POST, args={'campaign_id': 4})
    def test_cast_vote_on_treasurer(self):
        # already cast a vote on a president, you can still cast one vote on a treasurer
        response = self.response
        self.assertGoodResponse(response)

        votes = Vote.objects.filter(voter_id=2)
        self.assertEqual(votes[0].campaign_id, 2)

        # Casted a new vote
        self.assertEqual(self.original_number_of_votes + 1, len(list(Vote.objects.all())))

    @run(path_name='get_all_votes', email=MEMBER, method=GET, args={})
    def test_fail_get_all_votes_not_board_member(self):
        # response = self.client.get(reverse('api:get_all_votes'))
        # json = response.json()
        # self.assertEqual(json['message'], 'No current election available')
        #
        # self.test_cast_votes()
        #
        # response = self.client.get(reverse('api:get_all_votes'))
        # json = response.json()
        # votes = json['all_votes']
        # self.assertEqual(len(votes), 1)

        response = self.response
        self.assertEquals(response.status_code, 403)

    # @run(path_name='get_all_votes', email=BOARD_MEMBER, method=GET, args={})
    # def test_fail_get_all_votes_no_current_election(self):
    #     response = delete_election(0)
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.response
    #     self.assertBadResponse(response)


