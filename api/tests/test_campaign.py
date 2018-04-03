import datetime

from django.test import TestCase
from django.urls import reverse

from api import cursor_api
from api.models import *
from .custom_test_case import *


class CampaignTest(CustomTestCase):
    election = None

    def create_election(self):
        """
        Helper function to create an election
        :return:
        """
        election = Election(date=datetime.date.today())
        election.save()
        self.election = election

    def test_get_all_campaigns(self):
        response = self.client.get(reverse('api:get_all_campaigns'))
        self.assertEqual(response.json()['message'], 'No campaigns currently')

        # Some campaigns
        self.create_election()
        campaigner1 = Member(first_name="Eddie", last_name="Huang", email="ezhuang2@illinois.edu", dateJoined=datetime.date.today())
        campaigner1.save()
        campaigner2 = Member(first_name="Daniel", last_name="Rong", email="drong2@illinois.edu", dateJoined=datetime.date.today())
        campaigner2.save()

        campaign1 = Campaign(job="President", campaigner=campaigner1, pitch="Make Badminton Great Again", election=self.election)
        campaign1.save()
        campaign2 = Campaign(job="President", campaigner=campaigner2, pitch="Hello Campaign", election=self.election)
        campaign2.save()

        response = self.client.get(reverse('api:get_all_campaigns'))
        self.assertGoodResponse(response)

        json = response.json()
        self.assertTrue('campaigns' in json)
        self.assertEqual(len(json['campaigns']), 2)


    def test_get_campaign_from_campaigner(self):
        # No campaign
        non_campaigner = Member(first_name="Eddie", last_name="Huang", email="ezhuang2@illinois.edu", dateJoined=datetime.date.today())
        non_campaigner.save()

        response = self.client.get(reverse('api:get_campaign_from_campaigner', args=(non_campaigner.id,)))
        self.assertEqual(response.json()['message'], 'Member is not campaigning')

        # Existing campaign
        self.create_election()
        campaigner = non_campaigner
        campaign = Campaign(job="President", campaigner=campaigner, pitch="Make Badminton Great Again", election=self.election)
        campaign.save()

        response = self.client.get(reverse('api:get_campaign_from_campaigner', args=(campaigner.id,)))
        self.assertGoodResponse(response)

        json = response.json()
        campaigns = json['campaigns']
        self.assertEqual(campaigns['pitch'], 'Make Badminton Great Again')
        self.assertEqual(campaigns['campaigner'], campaigner.id)
        self.assertEqual(campaigns['job'], 'President')


    def test_create_campaign(self):
        self.create_election()

        campaigner = Member(first_name="Eddie", last_name="Huang", email="ezhuang2@illinois.edu", dateJoined=datetime.date.today())
        campaigner.save()

        response = self.client.post(reverse('api:create_campaign'), {'job': 'President', 'campaigner_id': campaigner.id, 'pitch': 'Make Badminton Great Again'})
        self.assertGoodResponse(response)

        all_campaigns = Campaign.objects.all()
        campaign = all_campaigns[0]
        self.assertEqual(campaign.campaigner_id, campaigner.id)
        self.assertEqual(campaign.job, 'President')
        self.assertEqual(campaign.election_id, self.election.id)

