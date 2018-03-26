import datetime
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from api import cursor_api

class ElectionTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_get_election(self):
        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'down') # No current election

        self.test_create_election()

        response = self.client.get(reverse('api:election'))
        json = response.json()
        self.assertEqual(json['date'], '2018-03-24')
        self.assertIsNone(json['endDate'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json['status'], 'up')  # Now there is an election


    def test_edit_election(self):
        self.test_create_election()
        date = self.test_date
        endDate = datetime.date(2018, 5, 2)
        response = self.client.post(reverse('api:election'), {'id': 1, 'startDate': cursor_api.serializeDate(date), 'endDate': cursor_api.serializeDate(endDate)})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:election'))
        self.assertEqual(response.json()['endDate'], '2018-05-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'up')  # Now there is an election

    def test_delete_election(self):
        self.test_create_election()

        voter_email = 'ezhuang2@illinois.edu'
        votee_email = 'obama@gmail.com'
        election_date = self.test_date
        response = self.client.post(reverse('api:vote'),
                                    {'voter': voter_email, 'electionDate': cursor_api.serializeDate(election_date),
                                     'votee': votee_email})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Vote successfully cast')

        position = 'OFFICER'
        pitch = 'Hello I am a test case'
        email_id = 'donghao2@illinois.edu'
        response = self.client.post(reverse('api:create_campaign'),
                                    {'id': 1, 'job': position, 'pitch': pitch, 'email': email_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'OK')

        response = self.client.delete(reverse('api:election'), {'id': 1})
        self.assertEqual(response.status_code, 200)

class CampaignTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_get_campaign(self):
        self.test_create_campaign()
        response = self.client.post(reverse('api:find_campaign'), {'id': 1, 'email': 'donghao2@illinois.edu', 'job': 'OFFICER'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['pitch'], 'Hello I am a test case')

    def test_create_campaign(self):
        self.test_create_election()
        position = 'OFFICER'
        pitch = 'Hello I am a test case'
        email_id= 'donghao2@illinois.edu'
        response = self.client.post(reverse('api:create_campaign'), {'id': 1, 'job': position, 'pitch': pitch, 'email': email_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'OK')

    def test_edit_campaign(self):
        self.test_create_election()
        position = 'PRESIDENT'
        pitch = 'Hello I am a modification to the PRESIDENT pitch'
        email_id='ezhuang2@illinois.edu'
        response = self.client.post(reverse('api:campaign'), {'id': 1, 'job': position, 'pitch': pitch, 'email': email_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'OK')

    def test_delete_campaign(self):
        self.test_create_election()
        position = 'PRESIDENT'
        email_id='donghao2@illinois.edu'
        response = self.client.post(reverse('api:create_campaign'), {'id': 1, 'job': position, 'pitch': "Hi",
                                                                     'email': email_id})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(reverse('api:campaign'), {'id': 1, 'job': position, 'email': email_id})
        self.assertEqual(response.status_code, 200)

    def test_get_all_campaigns(self):
        self.test_create_campaign()
        position = 'OFFICER'
        email_id = 'harryr2@illinois.edu'
        response = self.client.post(reverse('api:create_campaign'), {'job': position, 'pitch': "Hello I am Harry",
                                                                     'email': email_id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('api:campaign'))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()["campaigns"], [{'email': 'donghao2@illinois.edu', 'name': 'donghao2@illinois.edu', 'id': 1, 'job': 'OFFICER',
        #   'pitch': 'Hello I am a test case'}, {'email': 'harryr2@illinois.edu', 'name': 'harryr2@illinois.edu',
        #                                        'id': 2, 'job': 'OFFICER', 'pitch': 'Hello I am Harry'}])


class VotesTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

    def test_cast_votes(self):
        self.test_create_election()
        voter_email = 'ezhuang2@illinois.edu'
        votee_email = 'obama@gmail.com'
        election_date = self.test_date
        response = self.client.post(reverse('api:vote'), {'voter': voter_email, 'electionDate': cursor_api.serializeDate(election_date), 'votee': votee_email})
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
        response = self.client.post(reverse('api:add_interested'), interested_dict)
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
        response = self.client.post(reverse('api:add_interested'), interested_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        member_dict = {'email': 'ezhuang2@illinois.edu', 'level': 0, 'private': False, 'dateJoined': '2018-03-19', 'bio':'Hello, my name is Eddie.'}
        response = self.client.post(reverse('api:promote'), member_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.json()['my_info'][0].__getitem__('bio'), 'Hello, my name is Eddie.')
        self.assertEqual(response.json()['my_info'][0].__getitem__('email'), 'ezhuang2@illinois.edu')
        self.assertEqual(response.status_code, 200)

    def test_get_board_member_info(self):
        interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
                           'email': 'ezhuang2@illinois.edu'}
        response = self.client.post(reverse('api:add_interested'), interested_dict)
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

        response = self.client.get(reverse('api:boardmember_info'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)


    def test_delete_member(self):
        # Get a member in the db
        interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
                           'email': 'ezhuang2@illinois.edu'}
        response = self.client.post(reverse('api:add_interested'), interested_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        member_dict = {'email': 'ezhuang2@illinois.edu', 'level': 0, 'private': False, 'dateJoined': '2018-03-19',
                       'bio': 'Hello, my name is Eddie.'}
        response = self.client.post(reverse('api:promote'), member_dict)
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Delete member
        response = self.client.delete(reverse('api:edit_member'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.status_code, 200)

        # Check if member is gone from db
        response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
        self.assertEqual(response.json()['status'], 'down')
        self.assertEqual(response.status_code, 200)

    def test_add_to_schedule(self):
        response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

    def test_schedule(self):
        # Try to get schedule when there's nothing in the schedule, should receive nothing
        response = self.client.get(reverse('api:schedule'), {})
        self.assertEqual(response.json()['status'], 'down')
        self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
        self.assertEqual(response.status_code, 200)

        # Add to schedule
        response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Get schedule again, should work
        response = self.client.get(reverse('api:schedule'), {})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.json()['schedule'][0].__getitem__('date'), '2018-03-25T00:00:00Z')
        self.assertEqual(response.json()['schedule'][0].__getitem__('number_of_courts'), 4)

        self.assertEqual(response.status_code, 200)

        # Delete that entry
        response = self.client.delete(reverse('api:schedule'), {'date': '2018-03-25'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Check again. Should receive nothing
        response = self.client.get(reverse('api:schedule'), {})
        self.assertEqual(response.json()['status'], 'down')
        self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
        self.assertEqual(response.status_code, 200)

    def test_queue(self):
        # Get all the queues. Should get nothing
        response = self.client.get(reverse('api:queue'), {})
        self.assertEqual(response.json()['status'], 'down')
        self.assertEqual(response.json()['message'], 'There are no queues.')
        self.assertEqual(response.status_code, 200)

        # Add a CASUAL queue
        response = self.client.post(reverse('api:queue'), {'queue_type': 'CASUAL'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Get all queues. Should have CASUAL as type now
        response = self.client.get(reverse('api:queue'), {})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.json()['queues'][0].__getitem__('type'), 'CASUAL')
        self.assertEqual(response.status_code, 200)

    def test_court(self):
        # Get all courts. Should get nothing
        response = self.client.get(reverse('api:courts'), {})
        self.assertEqual(response.json()['status'], 'down')
        self.assertEqual(response.json()['message'], 'There are no courts stored in the database.')
        self.assertEqual(response.status_code, 200)

        # Add a CASUAL queue
        response = self.client.post(reverse('api:queue'), {'queue_type': 'CASUAL'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Add a court with a CASUAL queue
        response = self.client.post(reverse('api:courts'), {'court_id': '1', 'number': '2', 'queue': 'CASUAL'})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.status_code, 200)

        # Get all courts. Should get a court with id=1, number=2, queue_id='CASUAL'
        response = self.client.get(reverse('api:courts'), {})
        self.assertEqual(response.json()['status'], 'up')
        self.assertEqual(response.json()['courts'][0].__getitem__('id'), 1)
        self.assertEqual(response.json()['courts'][0].__getitem__('number'), 2)
        self.assertEqual(response.json()['courts'][0].__getitem__('queue_id'), 'CASUAL')
        self.assertEqual(response.status_code, 200)

