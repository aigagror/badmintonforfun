import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *

class AnnouncementTest(CustomTestCase):
    def test_get_announcements(self):
        self.create_example_data()

        response = self.client.get(reverse('api:get_announcements'))
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('announcements' in json)

        self.assertEqual(len(json['announcements']), 3)

    def test_create_announcement(self):

        announcements = Announcement.objects.all()
        number_of_announcements_before = len(list(announcements))

        response = self.client.post(reverse('api:create_announcement'), {'title': 'Hello', 'entry': 'World'})
        self.assertGoodResponse(response)

        announcements = Announcement.objects.all()
        number_of_announcements_after = len(list(announcements))

        self.assertEqual(number_of_announcements_after, number_of_announcements_before + 1)

        announcement = Announcement.objects.get(title='Hello', entry='World')

    def test_edit_announcement(self):

        announcements = Announcement.objects.all()
        announcement = announcements[0]

        response = self.client.post(reverse('api:edit_announcement'), {'id': announcement.id, 'title': 'Hello', 'entry': 'World'})
        self.assertGoodResponse(response)

        announcement = Announcement.objects.get(title='Hello', entry='World')


