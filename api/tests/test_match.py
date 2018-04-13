import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *
import json

class MatchTest(CustomTestCase):
    @run(path_name='current_match', email=GRACE, method=GET, args={})
    def test_get_current_match(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('match' in json)
        match = json['match']

        self.assertTrue('scoreA' in match)
        self.assertTrue('scoreB' in match)

        self.assertTrue('teamA' in match)
        self.assertTrue('teamB' in match)

    @run(path_name='finish_match', email=GRACE, method=POST, args={'id': 9, 'scoreA': 21, 'scoreB': 19})
    def test_finish_match(self):
        """
        Grace is associated with one unfinished match,
        which is on a court which is associated with the casual queue
        Since this was a casual match, Grace's level should not increase
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        casual_queue = Queue.objects.get(type='CASUAL')
        casual_courts = Court.objects.filter(queue=casual_queue)

        # The one match that Grace is a part of should be taken off the court and finished
        grace = Member.objects.get(first_name='Grace')
        member_playedin = PlayedIn.objects.get(member=grace)
        match_of_grace = member_playedin.match
        print("Grace's match ID: " + str(match_of_grace.id))

        self.assertIsNone(match_of_grace.court)
        self.assertIsNotNone(match_of_grace.endDateTime)

        # One of these courts must should now contain a match involving Member
        successfully_dequeued = False
        member = Member.objects.get(first_name='Member')
        for court in casual_courts:
            match_on_court = Match.objects.get(court=court)
            playedin = PlayedIn.objects.get(match=match_on_court)
            if playedin.member == member:
                successfully_dequeued = True
                break

        self.assertTrue(successfully_dequeued)

        # Grace's level should still be 0
        self.assertEqual(grace.level, 0)


    @run(path_name='finish_match', email=JOSHUA, method=POST, args={'scoreA': 21, 'scoreB': 19})
    def test_finish_ranked_match(self):
        """
        Joshua was on an ongoing ranked match. Since he won, his level should increase by some constant
        :return:
        """

        response = self.response
        self.assertGoodResponse(response)

        # Assert that all the courts for the ranked queue are empty now
        ranked_queue = Queue.objects.get(type='RANKED')
        ranked_courts = Court.objects.filter(queue=ranked_queue)
        for court in ranked_courts:
            match = Match.objects.get(court=court)
            self.assertIsNone(match)

        # Assert that a new match was added
        self.assertEqual(self.number_of_matches_now, self.original_number_of_matches + 1)

        # Assert that the match that joshua was a part of is finished
        joshua = Member.objects.get(first_name='Joshua')
        playedin = PlayedIn.objects.get(member=joshua)
        match = playedin.match

        self.assertIsNotNone(match.endDateTime)


        # Assert that Joshua's level increased by some constant
        # (Let's say for now that every win increases your level by 10)
        self.assertEqual(joshua.level, 10)




