import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from api.calls.match_call import *
from .custom_test_case import *
import json

class CourtTest(CustomTestCase):

    @run(path_name='get_courts', email=JARED, method=GET, args={})
    def test_get_courts(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()

        self.assertTrue('courts' in json)

        courts = json['courts']

        self.assertGreater(len(courts), 0)


        some_courts_have_matches = False
        some_courts_are_empty = False
        for court in courts:
            self.assertTrue('queue_type' in court)
            self.assertTrue('match' in court)
            self.assertTrue('court_id' in court)
            match = court['match']

            if match is not None:
                some_courts_have_matches = True
                self.assertTrue('match_id' in match)
                self.assertTrue('teamA' in match)
                self.assertTrue('teamB' in match)
            else:
                some_courts_are_empty = True


        self.assertTrue(some_courts_have_matches)
        self.assertTrue(some_courts_are_empty)