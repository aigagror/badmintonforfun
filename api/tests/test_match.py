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

    @run(path_name='current_match', email=GRACE, method=GET, args={})
    def test_get_current_match(self):
        response = self.response
        print(response.json()["message"])
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

