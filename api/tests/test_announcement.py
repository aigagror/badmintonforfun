import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class AnnouncementTest(CustomTestCase):

    @run(path_name='get_announcements', method=GET, email=INTERESTED, args={'title': 'Hello', 'entry': 'World'})
    def test_get_announcements(self):
        response = self.response
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('announcements' in json)



    @run(path_name='create_announcement', method=POST, email=BOARD_MEMBER, args={'title': 'Hello', 'entry': 'World'})
    def test_create_announcement(self):
        response = self.response
        self.assertGoodResponse(response)


        announcement = Announcement.objects.get(title='Hello', entry='World')
        self.assertIsNotNone(announcement)


        all_announcements = Announcement.objects.all()
        self.assertEqual(self.original_number_of_announcements + 1, len(list(all_announcements)))

    @run(path_name='edit_announcement', method=POST, email=BOARD_MEMBER, args={'id': 0, 'title': 'Hello', 'entry': 'World'})
    def test_edit_announcement(self):
        response = self.response
        self.assertGoodResponse(response)

        all_announcements = Announcement.objects.all()
        self.assertEqual(self.original_number_of_announcements, len(list(all_announcements)))


