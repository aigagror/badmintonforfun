from django.test import TestCase
from api.models import *
import datetime

class CustomTestCase(TestCase):
    def assertGoodResponse(self, response):
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json['message'], 'OK')

    def assertBadResponse(self, response):
        self.assertNotEqual(response.status_code, 200)

    def create_example_data(self):
        # Create some courts
        courts = []
        for i in range(8):
            courts.append(Court())
            courts[i].save()


        # Create some members
        members = []
        members.append(Member(first_name="Eddie", last_name="Huang", dateJoined=datetime.date.today(),
                              email="ezhuang2@illinois.edu"))
        members.append(Member(first_name="Bhuvan", last_name="Venkatesh", dateJoined=datetime.date.today(),
                              email="bhuvan2@illinois.edu"))
        members.append(Member(first_name="Daniel", last_name="Rong", dateJoined=datetime.date.today(),
                              email="drong4@illinois.edu"))
        members.append(Member(first_name="Grace", last_name="Shen", dateJoined=datetime.date.today(),
                              email="gshen3@illinois.edu"))
        members.append(Member(first_name="Jared", last_name="Franzone", dateJoined=datetime.date.today(),
                              email="jfranz2@illinois.edu"))

        for member in members:
            member.save()

        # Eddie has played many matches, an hour in total
        matches = []
        now = datetime.datetime.now()
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-60),
                             endDateTime=now + datetime.timedelta(minutes=-50), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-50),
                             endDateTime=now + datetime.timedelta(minutes=-40), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-40),
                             endDateTime=now + datetime.timedelta(minutes=-30), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-30),
                             endDateTime=now + datetime.timedelta(minutes=-20), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-20),
                             endDateTime=now + datetime.timedelta(minutes=-10), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-10),
                             endDateTime=now + datetime.timedelta(minutes=-0), scoreA=21, scoreB=19))
        for match in matches:
            match.save()
            playedin = PlayedIn(member=members[0],match=match, team="A")
            playedin.save()

        # Bhuvan has played one match (10 minutes)
        playedin = PlayedIn(member=members[1], match=matches[0], team="A")
        playedin.save()

        # Dan has played one match (10 minutes)
        playedin = PlayedIn(member=members[2], match=matches[0], team="B")
        playedin.save()


        # Create a casual queue
        queue = Queue(type="CASUAL")
        queue.save()

        # Add the first four courts to the casual queue
        for i in range(4):
            courts[i].queue = queue
            courts[i].save()

        # Eddie is on the casual queue as a party of 1
        party = Party(queue=queue)
        party.save()
        members[0].party = party
        members[0].save()

        # Bhuvan and Dan are on the casual queue as a party of 2 (Bhuvan and Dan have priority)
        party = Party(queue=queue)
        party.save()
        members[1].party = party
        members[1].save()
        members[2].party = party
        members[2].save()




