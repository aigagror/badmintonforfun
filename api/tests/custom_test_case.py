from django.test import TestCase
from api.models import *
import datetime
import api.datetime_extension

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

        # Create a casual queue
        queue = Queue(type="CASUAL")
        queue.save()


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
        now = datetime.datetime.now(tz=api.datetime_extension.utc)
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-80),
                             endDateTime=now + datetime.timedelta(minutes=-70), scoreA=21, scoreB=19))
        matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-70),
                             endDateTime=now + datetime.timedelta(minutes=-60), scoreA=21, scoreB=19))
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

        # Create a tournament bracket with all of the children having a match
        tournament = Tournament(date=datetime.date.today())
        tournament.save()

        # Create a full tree of height 3
        for level in range(4):
            for sibling_index in range(2**level):
                bracket_node = BracketNode(tournament=tournament, level=level, sibling_index=sibling_index)
                bracket_node.save()

        for index in range(2**3):
            bracket_node = BracketNode.objects.get(tournament=tournament, level=3, sibling_index=index)
            match = matches[index]
            bracket_node.match = match
            bracket_node.save()

        # Create some announcements
        self._create_announcements()



    def _create_announcements(self):
        # Create some announcements
        announcements = []
        announcements.append(Announcement(title='B4F Tournament draws and details', entry=
        '''
        Hi everyone!
        
        
        Thank you all for signing up for the B4f tournament! The draws for the games have been made, please refer to the following link to view your doubles pairing as well as the bracket run-down. These draws were made randomly so that hopefully there will not be any bias on any particular team, and for you guys to meet different players within the club!
        
        Link to brackets and teams: https://challonge.com/514dwqpt
        
        The tournament will be single-elimination based, with double games out of 21. They will be held during normal practice time (Mar 30-31, 6:00PM - 8:00PM) at ARC Gym 3. The tentative schedule will be that we will aim to finish the games up to semi-finals by the end of Friday, and finish up the tournament by Saturday. The cash prizes for the tournament will be split between the two players per winning team: 1st: $80 ; 2nd: $50 ; 3rd: $30.
        
        If there are any questions about the draws or if you can't access the link above, do feel free to shoot us an email (b4f.uiuc@gmail.com) ASAP.
        
        We look forward to seeing you all this Friday, and good luck!
        
        
        Best,
        
        Badminton For Fun
        '''
                                          , date=datetime.date.today()))
        announcements.append(Announcement(title='Badminton For Fun - Elections for B4F Executive Board', entry=
        '''
        Hi everyone!
        
        
        This is just information as to how we are going to end the rest of the semester. To those who showed up and participated in the tournament the past weekend, hope you all enjoyed yourselves! Due to the lack of time, we will have our final matches (1st v 2nd ; 3rd v 4th) held during practice this Friday. If you are competing, please show up before 6:15pm. To everyone else, do feel free to show up to watch the final games!
        
        Attached below is a Google Form link to sign up for any executive positions of your choosing. This is for anyone who would like to run for President, Vice-President, Treasurer, or Officer of Badminton For Fun 2018-2019. Every position except for Officer has only one opening. We will be having a short election after the due date. 
        
        https://docs.google.com/forms/d/e/1FAIpQLSfca1Urv6MZ0tAn869NLy7xPPRsG4Wr156uj1nI63AJvZsyiQ/viewform
        
        Please fill out the form by April 12th 11:59:59 pm if you are interested in applying. 
        
        Do feel free to shoot us an email if there are any further inquiries about the election or anything else on your mind. 
        
        
        Best, 
        
        Badminton For Fun
        '''
                                          , date=datetime.date.today()))
        announcements.append(Announcement(title='B4F Spring 2018 Tournament - Semi Final update', entry=
        '''
        Hey everyone!
        
        
        Congratulations on getting to the semi finals of the B4F Spring 2018 tournament! Just a quick reminder that you all are playing tomorrow for the semi finals, and need to be at the ARC by 6:15pm latest. If you don’t show up or arrive late, you will be forced to forfeit.
        
        Do feel free to let us know if there are any further questions. Otherwise, all the best to you all tomorrow!
        
        
        Best,
        
        Badminton For Fun
        
        
        -- Hannah
        '''
                                          , date=datetime.date.today()))
        for announcement in announcements:
            announcement.save()






