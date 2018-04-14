from .custom_test_case import *


class SettingsTest(CustomTestCase):
    @run(path_name="all_members", email=MEMBER, method=GET, args={})
    def test_board_member_settings_bad(self):
        # Non-boardmember trying to get info on all members. Should fail
        response = self.response
        self.assertBadResponse(response)

    @run(path_name="all_members", email=BOARD_MEMBER, method=GET, args={})
    def test_board_member_settings(self):
        # Boardmember trying to get info on all members. Should be valid
        response = self.response
        self.assertGoodResponse(response)
        json = response.json()

        self.assertTrue("members" in json)
        members = json["members"]
        if members is not None:
            first_member = members[0]
            self.assertTrue("member_id" in first_member)
            self.assertTrue("first_name" in first_member)
            self.assertTrue("last_name" in first_member)
            self.assertTrue("email" in first_member)
            self.assertTrue("status" in first_member)

    @run(path_name="all_members", email=BOARD_MEMBER, method=POST,
         args={"member_id": 5, "status": "Interested"})
    def test_demote_member_status(self):
        # Have a boardmember change the the Daniel from a Member to an Interested
        response = self.response
        self.assertGoodResponse(response)

        # Assert Daniel is not a member anymore, but is still an interested
        daniel_member_count = Member.objects.filter(pk=5).count()
        self.assertEqual(daniel_member_count, 0)
        daniel_interested_count = Interested.objects.filter(pk=5).count()
        self.assertEqual(daniel_interested_count, 1)

        # One less member
        self.assertEqual(self.number_of_members_now, self.original_number_of_members - 1)
        # Number of interesteds stays the same
        self.assertEqual(self.number_of_interesteds_now, self.original_number_of_interesteds)

    @run(path_name="all_members", email=BOARD_MEMBER, method=POST,
         args={"member_id": 5, "status": "Boardmember"})
    def test_promote_member_status(self):
        # Have a boardmember change the the Daniel from a Member to an Boardmember
        response = self.response
        self.assertGoodResponse(response)

        # Assert Daniel is still a member, but is also a boardmember
        daniel_member_count = Member.objects.filter(pk=5).count()
        self.assertEqual(daniel_member_count, 1)
        daniel_boardmember_count = BoardMember.objects.filter(pk=5).count()
        self.assertEqual(daniel_boardmember_count, 1)

        # One more boardmember
        self.assertEqual(self.number_of_boards_now, self.original_number_of_boards + 1)
        # Number of members stays the same
        self.assertEqual(self.number_of_members_now, self.original_number_of_members)

    @run(path_name="delete_member", email=BOARD_MEMBER, method=POST,
         args={"member_id": 6})
    def test_delete_member(self):
        # Delete Jared (a member) from the club
        response = self.response
        self.assertGoodResponse(response)

        # Assert Jared isn't an Interested or a Member or a Boardmember
        jared_member_count = Member.objects.filter(pk=6).count()
        self.assertEqual(jared_member_count, 0)
        jared_interested_count = Interested.objects.filter(pk=6).count()
        self.assertEqual(jared_interested_count, 0)
        jared_boardmember_count = BoardMember.objects.filter(pk=6).count()
        self.assertEqual(jared_boardmember_count, 0)

        # One less member
        self.assertEqual(self.number_of_members_now, self.original_number_of_members - 1)
        # One less interested
        self.assertEqual(self.number_of_interesteds_now, self.original_number_of_interesteds - 1)
#
#     @run(path_name="member_settings", email=MEMBER, method=GET, args={})
#     def test_board_member_setting(self):
#         response = self.response
#         json = response.json()
#         self.assertEqual(len(json), 3)
#         self.assertFalse(json[0]['value']) # Privacy setting
#
#     @run(path_name="add_interested", email=NO_ONE, method=GET, args=
#                             {'first_name': 'Eddie', 'last_name': 'Huang',
#                              'formerBoardMember': False,
#                              'email': 'ezhuang2@illinois.edu'})
#     def test_add_interested(self):
#         response = self.response
#         j = response.json()
#         self.assertEqual(j['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#
#     @run(path_name="promote", email=BOARD_MEMBER, method=POST, args={'id': 1})
#     def test_promote_interested(self):
#         response = self.response
#         j = response.json()
#         self.assertEqual(j['message'], 'OK')
#         self.assertEqual(response.status_code, 200)
#
#         members = Member.objects.all()
#         self.assertEqual(len(list(members)), len(list(self.original_members)) + 1)
#
#
#     @run(path_name="promote", email=BOARD_MEMBER, method=POST, args={'id': 2, 'job': 'PRESIDENT'})
#     def test_promote_member(self):
#         response = self.response
#         self.assertGoodResponse(response)
#
#         boards = BoardMember.objects.all()
#         self.assertEqual(len(list(boards)), len(list(self.original_boards)) + 1)
#
#
#     # TODO: Fix the test cases
#     #
#     # def test_get_member_info(self):
#     #     interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False, 'email': 'ezhuang2@illinois.edu'}
#     #     response = self.client.post(reverse('api:add_interested'), interested_dict)
#     #     self.assertEqual(response.json()['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     member_dict = {'id': 1}
#     #     response = self.client.post(reverse('api:promote'), member_dict)
#     #     self.assertEqual(response.json()['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     response = self.client.get(reverse('api:member_info'), {'id': 1})
#     #     j = response.json()
#     #     self.assertEqual(j['status'], 'up')
#     #     self.assertEqual(j['bio'], '')
#     #     self.assertEqual(j['email'], 'ezhuang2@illinois.edu')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_get_board_member_info(self):
#     #     interested_dict = {'first_name': 'Eddie', 'last_name': 'Huang', 'formerBoardMember': False,
#     #                        'email': 'ezhuang2@illinois.edu'}
#     #     response = self.client.post(reverse('api:add_interested'), interested_dict)
#     #     self.assertEqual(response.json()['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     member_dict = {'id': 1}
#     #     response = self.client.post(reverse('api:promote'), member_dict)
#     #     j = response.json()
#     #     self.assertEqual(j['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     boardmember_dict = {'id': 1, 'job': 'PRESIDENT'}
#     #     response = self.client.post(reverse('api:promote'), boardmember_dict)
#     #     self.assertEqual(response.json()['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     response = self.client.get(reverse('api:boardmember_info'), {'id': 1})
#     #     j = response.json()
#     #     self.assertEqual(j['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #
#     # def test_delete_member(self):
#     #     # Get a member in the db
#     #     interested = Interested(first_name='Eddie', last_name='Huang', email='ezhuang2@illinois.edu')
#     #     interested.save()
#     #
#     #     member_dict = {'id': interested.id}
#     #     response = self.client.post(reverse('api:promote'), member_dict)
#     #     self.assertEqual(response.json()['message'], 'OK')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     response = self.client.get(reverse('api:member_info'), {'id': interested.id})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Delete member
#     #     response = self.client.delete(reverse('api:edit_member'), {'email': 'ezhuang2@illinois.edu'})
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Check if member is gone from db
#     #     response = self.client.get(reverse('api:member_info'), {'email': 'ezhuang2@illinois.edu'})
#     #     self.assertEqual(response.json()['status'], 'down')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_add_to_schedule(self):
#     #     response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_schedule(self):
#     #     # Try to get schedule when there's nothing in the schedule, should receive nothing
#     #     response = self.client.get(reverse('api:schedule'), {})
#     #     self.assertEqual(response.json()['status'], 'down')
#     #     self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Add to schedule
#     #     response = self.client.post(reverse('api:schedule'), {'date': '2018-03-25', 'number_of_courts': 4})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Get schedule again, should work
#     #     response = self.client.get(reverse('api:schedule'), {})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.json()['schedule'][0].__getitem__('date'), '2018-03-25T00:00:00Z')
#     #     self.assertEqual(response.json()['schedule'][0].__getitem__('number_of_courts'), 4)
#     #
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Delete that entry
#     #     response = self.client.delete(reverse('api:schedule'), {'date': '2018-03-25'})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Check again. Should receive nothing
#     #     response = self.client.get(reverse('api:schedule'), {})
#     #     self.assertEqual(response.json()['status'], 'down')
#     #     self.assertEqual(response.json()['message'], 'There is nothing in the schedule.')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_queue(self):
#     #     # Get all the queues. Should get nothing
#     #     response = self.client.get(reverse('api:queues'), {})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.json()['message'], 'There are no queues.')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Add a CASUAL queue
#     #     response = self.client.post(reverse('api:create_queue'), {'queue_type': 'CASUAL'})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Get all queues. Should have CASUAL as type now
#     #     response = self.client.get(reverse('api:queues'), {})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.json()['queues'][0].__getitem__('type'), 'CASUAL')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_court(self):
#     #     # Get all courts. Should get nothing
#     #     response = self.client.get(reverse('api:courts'), {})
#     #     self.assertEqual(response.json()['status'], 'down')
#     #     self.assertEqual(response.json()['message'], 'There are no courts stored in the database.')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Add a CASUAL queue
#     #     response = self.client.post(reverse('api:queue'), {'queue_type': 'CASUAL'})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Add a court with a CASUAL queue
#     #     response = self.client.post(reverse('api:courts'), {'court_id': '1', 'queue': 'CASUAL'})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.status_code, 200)
#     #
#     #     # Get all courts. Should get a court with id=1, number=2, queue_id='CASUAL'
#     #     response = self.client.get(reverse('api:courts'), {})
#     #     self.assertEqual(response.json()['status'], 'up')
#     #     self.assertEqual(response.json()['courts'][0].__getitem__('id'), 1)
#     #     self.assertEqual(response.json()['courts'][0].__getitem__('queue_id'), 'CASUAL')
#     #     self.assertEqual(response.status_code, 200)