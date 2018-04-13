# import datetime
#
# from django.test import TestCase
# from django.urls import reverse
#
# from api import cursor_api
# from .custom_test_case import *
# from api.models import *
#
#
# class VotesTest(CustomTestCase):
#     def create_election_helper(self):
#         election = Election(date=datetime.date.today())
#         election.save()
#
#         campaigner1 = Member(first_name='Eddie', last_name='Huang', dateJoined=datetime.date.today(), email='ezhuang2@illinois.edu')
#         campaigner2 = Member(first_name='Bhuvan', last_name='Venkatesh', dateJoined=datetime.date.today(), email='bhuvan2@illinois.edu')
#         campaigner3 = Member(first_name='Grace', last_name='Shen', dateJoined=datetime.date.today(), email='gshen3@illinois.edu')
#         campaigner4 = Member(first_name='Daniel', last_name='Rong', dateJoined=datetime.date.today(), email='drong4@illinois.edu')
#
#         campaigner1.save()
#         campaigner2.save()
#         campaigner3.save()
#         campaigner4.save()
#
#         campaign1 = Campaign(job='President', campaigner=campaigner1, election=election, pitch='I am Eddie')
#         campaign2 = Campaign(job='President', campaigner=campaigner2, election=election, pitch='I am Bhuvan')
#         campaign3 = Campaign(job='President', campaigner=campaigner3, election=election, pitch='I am Grace')
#         campaign4 = Campaign(job='President', campaigner=campaigner4, election=election, pitch='I am Dan')
#
#         campaign1.save()
#         campaign2.save()
#         campaign3.save()
#         campaign4.save()
#
#         return election
#
#
#
#
#     def test_cast_votes(self):
#         election = self.create_election_helper()
#
#         campaigns = Campaign.objects.filter(election=election)
#
#         voter = Member(first_name='Some', last_name='Voter', dateJoined=datetime.date.today(), email='voter@illinois.edu')
#         voter.save()
#
#         response = self.client.post(reverse('api:cast_vote'), {'voter': voter.id, 'campaign': campaigns[0].id})
#         self.assertGoodResponse(response)
#
#     def test_get_all_votes(self):
#         response = self.client.get(reverse('api:get_all_votes'))
#         json = response.json()
#         self.assertEqual(json['message'], 'No current election available')
#
#         self.test_cast_votes()
#
#         response = self.client.get(reverse('api:get_all_votes'))
#         json = response.json()
#         votes = json['all_votes']
#         self.assertEqual(len(votes), 1)