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

