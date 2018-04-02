from django.test import TestCase
from django.urls import reverse

from api.models import Interested


# class SettingsTest(TestCase):
#     def test_promote(self):
#         interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
#                            'email': 'ezhuang2@illinois.edu'}
#         response = self.client.post(reverse('api:add_interested'), interested_dict)
#         j = response.json()
#         self.assertEqual(j['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         member_dict = {'id': 1}
#         response = self.client.post(reverse('api:promote'), member_dict)
#         j = response.json()
#         self.assertEqual(j['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         boardmember_dict = {'id': 1, 'job': 'PRESIDENT'}
#         response = self.client.post(reverse('api:promote'), boardmember_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_member_info(self):
#         interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False, 'email': 'ezhuang2@illinois.edu'}
#         response = self.client.post(reverse('api:add_interested'), interested_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         member_dict = {'id': 1}
#         response = self.client.post(reverse('api:promote'), member_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.get(reverse('api:member_info'), {'id': 1})
#         j = response.json()
#         self.assertEqual(j['status'], 'up')
#         self.assertEqual(j['bio'], '')
#         self.assertEqual(j['email'], 'ezhuang2@illinois.edu')
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_board_member_info(self):
#         interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
#                            'email': 'ezhuang2@illinois.edu'}
#         response = self.client.post(reverse('api:add_interested'), interested_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         member_dict = {'id': 1}
#         response = self.client.post(reverse('api:promote'), member_dict)
#         j = response.json()
#         self.assertEqual(j['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         boardmember_dict = {'id': 1, 'job': 'PRESIDENT'}
#         response = self.client.post(reverse('api:promote'), boardmember_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.get(reverse('api:boardmember_info'), {'id': 1})
#         j = response.json()
#         self.assertEqual(j['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#
#     def test_delete_member(self):
#         # Get a member in the db
#         interested = Interested(first_name='Eddie', last_name='Huang', email='ezhuang2@illinois.edu')
#         interested.save()
#
#         member_dict = {'id': interested.id}
#         response = self.client.post(reverse('api:promote'), member_dict)
#         self.assertEqual(response.json()['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         response = self.client.get(reverse('api:member_info'), {'id': interested.id})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Delete member
#         response = self.client.delete(reverse('api:edit_member'), {'email': 'ezhuang2@illinois.edu'})
#         self.assertEqual(response.status_code, 200)
#
#         # Check if member is gone from db
#         response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
#         self.assertEqual(response.json()['status'], 'down')
#         self.assertEqual(response.status_code, 200)
#
#     def test_add_to_schedule(self):
#         response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#     def test_schedule(self):
#         # Try to get schedule when there's nothing in the schedule, should receive nothing
#         response = self.client.get(reverse('api:schedule'), {})
#         self.assertEqual(response.json()['status'], 'down')
#         self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
#         self.assertEqual(response.status_code, 200)
#
#         # Add to schedule
#         response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Get schedule again, should work
#         response = self.client.get(reverse('api:schedule'), {})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.json()['schedule'][0].__getitem__('date'), '2018-03-25T00:00:00Z')
#         self.assertEqual(response.json()['schedule'][0].__getitem__('number_of_courts'), 4)
#
#         self.assertEqual(response.status_code, 200)
#
#         # Delete that entry
#         response = self.client.delete(reverse('api:schedule'), {'date': '2018-03-25'})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Check again. Should receive nothing
#         response = self.client.get(reverse('api:schedule'), {})
#         self.assertEqual(response.json()['status'], 'down')
#         self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
#         self.assertEqual(response.status_code, 200)
#
#     def test_queue(self):
#         # Get all the queues. Should get nothing
#         response = self.client.get(reverse('api:queues'), {})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.json()['message'], 'There are no queues.')
#         self.assertEqual(response.status_code, 200)
#
#         # Add a CASUAL queue
#         response = self.client.post(reverse('api:create_queue'), {'queue_type': 'CASUAL'})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Get all queues. Should have CASUAL as type now
#         response = self.client.get(reverse('api:queues'), {})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.json()['queues'][0].__getitem__('type'), 'CASUAL')
#         self.assertEqual(response.status_code, 200)
#
#     def test_court(self):
#         # Get all courts. Should get nothing
#         response = self.client.get(reverse('api:courts'), {})
#         self.assertEqual(response.json()['status'], 'down')
#         self.assertEqual(response.json()['message'], 'There are no courts stored in the database.')
#         self.assertEqual(response.status_code, 200)
#
#         # Add a CASUAL queue
#         response = self.client.post(reverse('api:queue'), {'queue_type': 'CASUAL'})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Add a court with a CASUAL queue
#         response = self.client.post(reverse('api:courts'), {'court_id': '1', 'queue': 'CASUAL'})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.status_code, 200)
#
#         # Get all courts. Should get a court with id=1, number=2, queue_id='CASUAL'
#         response = self.client.get(reverse('api:courts'), {})
#         self.assertEqual(response.json()['status'], 'up')
#         self.assertEqual(response.json()['courts'][0].__getitem__('id'), 1)
#         self.assertEqual(response.json()['courts'][0].__getitem__('queue_id'), 'CASUAL')
#         self.assertEqual(response.status_code, 200)