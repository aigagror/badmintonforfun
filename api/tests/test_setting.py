from .custom_test_case import *


class SettingsTest(CustomTestCase):
    @run(path_name="all_members", email=MEMBER, method=GET, args={})
    def test_board_member_settings_bad(self):
        # Non-boardmember trying to get info on all members. Should fail
        response = self.response
        self.assertBadResponse(response)

    @run(path_name="all_members", email=BOARD_MEMBER, method=GET, args={})
    def test_board_member_settings(self):
        # BoardMember trying to get info on all members. Should be valid
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
         args={"member_id": 5, "status": str("Interested")})
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

        # TODO: Make sure any entry in PlayedIn, Vote, and Campaign associated with Daniel is also gone
        played_in = PlayedIn.objects.filter(member_id=5).count()
        self.assertEqual(played_in, 0)

    @run(path_name="all_members", email=BOARD_MEMBER, method=POST,
         args={"member_id": 5, "status": str("BoardMember")})
    def test_promote_member_status(self):
        # Have a boardmember change the the Daniel from a Member to an BoardMember
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

        # Assert Jared isn't an Interested or a Member or a BoardMember
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

