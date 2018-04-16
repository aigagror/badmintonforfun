import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from api.calls.match_call import *
from .custom_test_case import *
import json

class MatchTest(CustomTestCase):

    def test_create_match_call(self):
        matches = len(list(Match.objects.all()))
        playedin = len(list(PlayedIn.objects.all()))
        create_match(a_players=[1, 2], b_players=[3, 4], court_id=5)
        self.assertEqual(matches + 1, len(list(Match.objects.all())))
        self.assertEqual(playedin + 4, len(list(PlayedIn.objects.all())))

    # @run(path_name='start_match', email=JARED, method=POST, args={'court_id': 6})
    # def test_start_match(self):
    #     """
    #     Can start a match on a court with no queue
    #     :return:
    #     """
    #     response = self.response
    #     self.assertGoodResponse(response)
    #
    #     self.assertEqual(self.original_number_of_matches + 1, self.number_of_matches_now)
    #
    #     jared = Member.objects.get(first_name='Jared')
    #     playedin = PlayedIn.objects.get(member=jared)
    #     self.assertIsNotNone(playedin)
    #     match = playedin.match
    #
    #     # Should be an ongoing match
    #     self.assertIsNone(match.endDateTime)
    #
    #     # Should be on this court
    #     self.assertEqual(6, match.court_id)
    #
    # @run(path_name='start_match', email=JARED, method=POST, args={'court_id': 5})
    # def test_start_bad_match(self):
    #     """
    #     Cannot start a match on a court that's associated with a queue
    #     :return:
    #     """
    #     response = self.response
    #     self.assertBadResponse(response)
    #
    #     self.assertEqual(self.original_number_of_matches, self.number_of_matches_now)
    #
    #     jared = Member.objects.get(first_name='Jared')
    #     playedin = PlayedIn.objects.get(member=jared)
    #     self.assertIsNone(playedin)
    #
    #     match_on_court = Match.objects.filter(court_id=5).exists()
    #     self.assertFalse(match_on_court)

    @run(path_name='join_match', email=JARED, method=POST, args={'match_id': 9, 'team': 'B'})
    def test_join_match_team_B(self):
        """
        Jared has not played in this match before
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        match = Match.objects.get(id=9)
        jared = Member.objects.get(first_name='Jared')
        playedin = PlayedIn.objects.get(member=jared, match=match)
        self.assertIsNotNone(playedin)
        self.assertEqual(playedin.team, 'B')

    @run(path_name='join_match', email=JARED, method=POST, args={'match_id': 9, 'team': 'A'})
    def test_join_match_team_A(self):
        """
        Jared has not played in this match before
        :return:
        """
        response = self.response
        self.assertGoodResponse(response)

        match = Match.objects.get(id=9)
        jared = Member.objects.get(first_name='Jared')
        playedin = PlayedIn.objects.get(member=jared, match=match)
        self.assertIsNotNone(playedin)
        self.assertEqual(playedin.team, 'A')

    @run(path_name='join_match', email=JARED, method=POST, args={'match_id': 1, 'team': 'A'})
    def test_bad_join_finished_match(self):
        """
        Cannot join a finished match
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        json = response.json()
        self.assertEqual('Cannot join a finished match', json['message'])

        match = Match.objects.get(id=1)
        jared = Member.objects.get(first_name='Jared')
        playedin = PlayedIn.objects.filter(member=jared, match=match)
        playedin = list(playedin)
        self.assertEquals(playedin, [])

    @run(path_name='join_match', email=GRACE, method=POST, args={'match_id': 13, 'team': 'B'})
    def test_bad_join_match(self):
        """
        Grace is already in an ongoing match
        :return:
        """
        response = self.response
        self.assertBadResponse(response)

        json = response.json()
        self.assertEqual(json['message'], 'Member is already in a match')

        match = Match.objects.get(id=13)
        grace = Member.objects.get(first_name='Grace')
        playedin = PlayedIn.objects.filter(member=grace, match=match)
        playedin = list(playedin)
        self.assertEquals(playedin, [])

    @run(path_name='leave_match', email=GRACE, method=POST, args={'match_id': 9})
    def test_leave_match_that_deletes_match(self):
        response = self.response
        self.assertGoodResponse(response)

        self.assertEqual(self.number_of_matches_now, self.original_number_of_matches - 1)

        grace = Member.objects.get(first_name='Grace')
        playedin = PlayedIn.objects.filter(member=grace)
        playedin = list(playedin)
        self.assertEquals(playedin, [])


    @run(path_name='leave_match', email=EDDIE, method=POST, args={'match_id': 1})
    def test_bad_leave_match(self):
        response = self.response
        self.assertBadResponse(response)

        json = response.json()
        self.assertEqual(json['message'], 'Cannot leave a finished match')

        self.assertEqual(self.number_of_matches_now, self.original_number_of_matches)

        # Eddie should still be in that match
        match = Match.objects.get(id=1)
        eddie = Member.objects.get(first_name='Eddie')
        playedin = PlayedIn.objects.get(member=eddie, match=match)
        self.assertIsNotNone(playedin)

    @run(path_name='leave_match', email=EDDIE, method=POST, args={'match_id': 9})
    def test_bad_leave_match_not_in_match(self):
        response = self.response
        self.assertBadResponse(response)

        json = response.json()
        self.assertEqual(json['message'], "Cannot leave a match you're not part of!")


    @run(path_name='leave_match', email=DAN, method=POST, args={'match_id': 10})
    def test_leave_match(self):
        response = self.response
        self.assertGoodResponse(response)

        playedin = len(list(PlayedIn.objects.all()))
        self.assertEqual(playedin, self.original_number_of_playedins - 1)
        self.assertEqual(len(list(Match.objects.all())), self.original_number_of_matches)


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

    @run(path_name='finish_match', email=GRACE, method=POST, args={'scoreA': 21, 'scoreB': 19})
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

        court_query = Court.objects.filter(match=match_of_grace)

        self.assertFalse(court_query.exists())
        self.assertIsNotNone(match_of_grace.endDateTime)

        # One of these courts must should now contain a match involving Member
        successfully_dequeued = 0
        member_dan = Member.objects.get(first_name='Daniel')
        member_bhuvan = Member.objects.get(first_name='Bhuvan')
        for court in casual_courts:
            match_on_court = court.match
            playedin = PlayedIn.objects.filter(match=match_on_court)
            playedin = list(playedin)
            for played in playedin:
                if played.member == member_dan:
                    successfully_dequeued += 1
                elif played.member == member_bhuvan:
                    successfully_dequeued += 1

        self.assertTrue(successfully_dequeued, 2)

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




