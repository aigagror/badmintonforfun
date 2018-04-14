import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from api.calls.match_call import *
from .custom_test_case import *
import json

class MatchTest(CustomTestCase):

    def test_create_match(self):
        matches = len(list(Match.objects.all()))
        playedin = len(list(PlayedIn.objects.all()))
        create_match(score_a=21, score_b=23, a_players=[1, 2], b_players=[3, 4], court_id=5)
        self.assertEqual(matches + 1, len(list(Match.objects.all())))
        self.assertEqual(playedin + 4, len(list(PlayedIn.objects.all())))

    @run(path_name='join_match', email=JARED, method=POST, args={'match_id': 1})
    def test_join_match(self):
        """
        Jared never played in a match before
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        jared = Member.objects.get(first_name='Jared')
        playedin = PlayedIn.objects.get(member=jared)
        self.assertIsNotNone(playedin)

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

    @run(path_name='finish_match', email=GRACE, method=POST, args={'scoreA': 21, 'scoreB': 23})
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

        # Grace's level should still be 0, since she's team A
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
            matches = Match.objects.filter(court=court)  # Match.objects.get(court=court) was throwing errors
            self.assertTrue(len(list(matches)) == 0)

        # Assert that the number of matches remain the same (finishing a match just sets the endDateTime of an
        # existing match.
        self.assertEqual(self.number_of_matches_now, self.original_number_of_matches)

        # Assert that the match that joshua was a part of is finished
        joshua = Member.objects.get(first_name='Joshua')
        playedin = PlayedIn.objects.get(member=joshua)
        match = playedin.match

        self.assertIsNotNone(match.endDateTime)


        # Assert that Joshua's level increased by some constant, since he's team A
        # Joshua's original level is 10.
        # (Let's say for now that every win increases your level by 10)
        self.assertEqual(joshua.level, 20)




