import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api


class CampaignTest(TestCase):
    test_date = datetime.date(2018, 3, 24)

    def test_create_election(self):
        date = self.test_date
        response = self.client.post(reverse('api:create_election'), {'startDate': cursor_api.serializeDate(date)})
        self.assertEqual(response.status_code, 200)

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