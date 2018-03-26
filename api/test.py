import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from api import cursor

class ElectionTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_get_election(self):
        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'down') # No current election

        self.test_create_election()

        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.json()['date'], '2018-03-24')
        self.assertIsNone(response.json()['endDate'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'up')  # Now there is an election


    def test_edit_election(self):
        self.test_create_election()
        date = self.test_date
        endDate = datetime.date(2018, 5, 2)
        response = self.client.post(reverse('api:election'), {'startDate': cursor.serializeDate(date), 'endDate': cursor.serializeDate(endDate)})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.json()['endDate'], '2018-05-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'up')  # Now there is an election

class VotesTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_cast_votes(self):
        self.test_create_election()
        voter_email = 'ezhuang2@illinois.edu'
        votee_email = 'obama@gmail.com'
        election_date = self.test_date
        response = self.client.post(reverse('api:vote'), {'voter': voter_email, 'electionDate': cursor.serializeDate(election_date), 'votee': votee_email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Vote successfully cast')


    def test_get_all_votes(self):
        response = self.client.get(reverse('api:all_votes'))
        self.assertEqual(len(response.json()), 0)

        self.test_cast_votes()

        response = self.client.get(reverse('api:all_votes'))
        self.assertEqual(len(response.json()), 1)



class SettingsTest(TestCase):
    def test_promote(self):
        interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
                           'email': 'ezhuang2@illinois.edu'}
        response = self.client.post(reverse('api:add_member'), interested_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        member_dict = {'email': 'ezhuang2@illinois.edu', 'level': 0, 'private': False, 'dateJoined': '2018-03-19',
                       'bio': 'Hello, my name is Eddie.'}
        response = self.client.post(reverse('api:promote'), member_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        boardmember_dict = {'email': 'ezhuang2@illinois.edu', 'job': 'PRESIDENT'}
        response = self.client.post(reverse('api:promote'), boardmember_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

    def test_get_member_info(self):
        interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False, 'email': 'ezhuang2@illinois.edu'}
        response = self.client.post(reverse('api:add_member'), interested_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        member_dict = {'email': 'ezhuang2@illinois.edu', 'level': 0, 'private': False, 'dateJoined': '2018-03-19', 'bio': 'Hello, my name is Eddie.'}
        response = self.client.post(reverse('api:promote'), member_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

    def test_get_board_member_info(self):
        foo = 0