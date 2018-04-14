from django.test import TestCase
from api.models import *
import datetime
import api.datetime_extension
from enum import Enum
from django.urls import reverse


_class_ranking = [Interested, Member, BoardMember]

NO_ONE = 'noone@illinois.edu'
INTERESTED = 'interested@illinois.edu'
MEMBER = 'member@illinois.edu'
EDDIE = 'ezhuang2@illinois.edu'
GRACE = 'gshen3@illinois.edu'
BHUVAN = 'bhuvan2@illinois.edu'
DAN = 'drong4@illinois.edu'
JARED = 'jfranz2@illinois.edu'
BOARD_MEMBER = 'board_member@illinois.edu'
JOSHUA = 'jcheng2@illinois.edu'

POST = "post"
GET = "get"

def run(path_name, email, method, args):
    """
    This decorator extracts Permission p \in {None, Interested, Member, BoardMember} from the email that was given
    It then asserts that the api described by the path_name and method is not valid for any person with permission below
    permission p.

    It then calls the api with the given parameters encapsulated by args and stores the result in
    self.response

    After calling the api, it stores some nice results in some variables such as
    self.interesteds_now = Interested.objects.all()
    self.number_of_interesteds_now = len(list(self.interesteds_now))

    :param path_name:
    :param email:
    :param method:
    :param args:
    :return:
    """
    def wrapper(test_func):
        def call_api(self):
            if method == POST:
                self.response = self.client.post(reverse('api:{}'.format(path_name)), args)
            elif method == GET:
                self.response = self.client.get(reverse('api:{}'.format(path_name)), args)

        def authentication(self):
            for x in reversed(_class_ranking):
                try:
                    person = x.objects.get(email=email)
                except:
                    person = None
                if person is not None:
                    self.permission = x
                    break

            self.path_name = path_name

            # Login
            user = User.objects.create_user(username=email, email=email)
            self.client.force_login(user)

            call_api(self)

            # Get the resulting models
            self.interesteds_now = Interested.objects.all()
            self.number_of_interesteds_now = len(list(self.interesteds_now))

            self.members_now = Member.objects.all()
            self.number_of_members_now = len(list(self.members_now))

            self.parties_now = Party.objects.all()
            self.number_of_parties_now = len(list(self.parties_now))

            self.matches_now = Match.objects.all()
            self.number_of_matches_now = len(list(self.matches_now))

            # Run the test case
            test_func(self)



            # Assert that the url requires authentication
            ranking = _class_ranking.index(self.permission)
            for i in range(ranking):
                self.client.logout()
                lower_class = _class_ranking[i]

                person = lower_class.objects.first()

                user = User.objects.create_user(username=person.first_name, email=person.email)
                self.client.force_login(user)

                call_api(self)

                self.assertEqual(self.response.status_code, 403)

            self.client.logout()
            call_api(self)
            self.assertEqual(self.response.status_code, 302)

        return authentication
    return wrapper

class CustomTestCase(TestCase):
    def setUp(self):
        self.create_example_data()
        self.original_interesteds = Interested.objects.all()
        self.original_number_of_interesteds = len(list(self.original_interesteds))

        self.original_members = Member.objects.all()
        self.original_number_of_members = len(list(self.original_members))

        self.original_boards = Member.objects.all()
        self.original_number_of_boards = len(list(self.original_boards))

        self.original_parties = Party.objects.all()
        self.original_number_of_parties = len(list(self.original_parties))

        self.original_matches = Match.objects.all()
        self.original_number_of_matches = len(list(self.original_matches))

    def assertGoodResponse(self, response):
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json['message'], 'OK')

    def assertBadResponse(self, response):
        self.assertNotEqual(response.status_code, 200)

    def create_example_data(self):
        # Create a casual queue
        casual_queue = Queue(type="CASUAL")
        casual_queue.save()

        # Create a ranked queue
        ranked_queue = Queue(type="RANKED")
        ranked_queue.save()

        # Create some courts
        courts = []
        for i in range(8):
            courts.append(Court())
            courts[i].save()

        # Add the first four courts to the casual queue
        for i in range(4):
            courts[i].queue = casual_queue
            courts[i].save()

        # Add the next two courts to the ranked queue
        for i in range(4, 6):
            courts[i].queue = ranked_queue
            courts[i].save()

        # Create some people
        people = self._create_people()

        # Create some matches
        self._create_matches()

        # Create the parties
        self._create_parties()

        # Create the tournament
        self._create_tournament()

        # Create some announcements
        self._create_announcements()

    def _create_tournament(self):
        """
        Creates a tournament in which the bracket tree structure is a perfect tree of height 3
        The leaf nodes contain empty matches with no one on them
        :param now:
        :return:
        """


        now = datetime.datetime.now(tz=api.datetime_extension.utc)


        # Create a tournament bracket with all of the children having a match
        tournament = Tournament(date=datetime.date.today())
        tournament.save()
        # Create a full tree of height 3
        for level in range(4):
            for sibling_index in range(2 ** level):
                bracket_node = BracketNode(tournament=tournament, level=level, sibling_index=sibling_index)
                bracket_node.save()
        for index in range(2 ** 3):
            bracket_node = BracketNode.objects.get(tournament=tournament, level=3, sibling_index=index)
            # Create an empty match
            match = Match(startDateTime=now, scoreA=0, scoreB=0)
            match.save()
            bracket_node.match = match
            bracket_node.save()

    def _create_parties(self):
        """
        Member is on the casual queue as a party of 1
        Eddie is on the casual queue as a party of 1
        Bhuvan and Dan are on the casual queue as a party of 2

        (Member has the highest priority on the casual queue)

        There is no party on the ranked queue

        No one else is on any party

        :return:
        """
        casual_queue = Queue.objects.get(type='CASUAL')
        eddie = Member.objects.get(first_name='Eddie')
        bhuvan = Member.objects.get(first_name='Bhuvan')
        dan = Member.objects.get(first_name='Daniel')
        member = Member.objects.get(first_name='Member')

        # 3 Parties
        parties = [Party(queue=casual_queue) for _ in range(3)]
        for party in parties:
            party.save()

        # Eddie is on the casual queue as a party of 1
        eddie.party = parties[0]
        eddie.save()

        # Bhuvan and Dan are on the casual queue as a party of 2 (Bhuvan and Dan have priority)
        bhuvan.party = parties[1]
        bhuvan.save()
        dan.party = parties[1]
        dan.save()

        # Member is on the casual queue as a party of 1
        member.party = parties[2]
        member.save()

        print("ID's of parties")
        for party in parties:
            party_members = Member.objects.filter(party=party)
            ret = '{}: ['.format(party.id)
            for member in party_members:
                ret += '{},'.format(str(member))
            ret += ']'

            print(ret)


    def _create_matches(self):
        """
        NOTE: This function asssumes that certain people were already created

        This function creates
            8 finished matches, 10 minutes long each.
            4 unfinished matches, all on the first four courts
                which are associated with the CASUAL queue

            1 unfinished match on a RANKED court

        Eddie has played all 8 finished matches (80 minutes in total)
        Bhuvan has played one match (10 minutes)
        Dan has played one match (10 minutes)

        Grace is on one of the 4 unfinished matches that's on a casual court
        (yes, that means 3 of the unfinished matches have no one associated with them...). That is a TODO

        Joshua is on the 1 unfinished match that's on a ranked court

        Everyone else has not played in any matches

        :return:
        """

        eddie = Member.objects.get(email='ezhuang2@illinois.edu')
        bhuvan = Member.objects.get(first_name='Bhuvan')
        dan = Member.objects.get(first_name='Daniel')
        grace = Member.objects.get(first_name='Grace')
        joshua = Member.objects.get(first_name='Joshua')

        now = datetime.datetime.now(tz=api.datetime_extension.utc)
        finished_matches = []

        # Finished matches
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-80),
                             endDateTime=now + datetime.timedelta(minutes=-70), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-70),
                             endDateTime=now + datetime.timedelta(minutes=-60), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-60),
                             endDateTime=now + datetime.timedelta(minutes=-50), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-50),
                             endDateTime=now + datetime.timedelta(minutes=-40), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-40),
                             endDateTime=now + datetime.timedelta(minutes=-30), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-30),
                             endDateTime=now + datetime.timedelta(minutes=-20), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-20),
                             endDateTime=now + datetime.timedelta(minutes=-10), scoreA=21, scoreB=19))
        finished_matches.append(Match(startDateTime=now + datetime.timedelta(minutes=-10),
                             endDateTime=now + datetime.timedelta(minutes=-0), scoreA=21, scoreB=19))

        for match in finished_matches:
            match.save()

            # Eddie played in all finished matches
            playedin = PlayedIn(member=eddie, match=match, team="A")
            playedin.save()

        # Bhuvan and Dan
        playedin = PlayedIn(member=bhuvan, match=finished_matches[0], team="A")
        playedin.save()

        playedin = PlayedIn(member=dan, match=finished_matches[0], team="B")
        playedin.save()

        # Unfinished casual matches
        unfinished_casual_matches = [Match(startDateTime=now, scoreA=21, scoreB=19),
                                     Match(startDateTime=now, scoreA=21, scoreB=19),
                                     Match(startDateTime=now, scoreA=21, scoreB=19),
                                     Match(startDateTime=now, scoreA=21, scoreB=19)]

        for match in unfinished_casual_matches:
            # Assign these unfinished matches on the courts
            # That are associated with the casual queue
            casual_queue = Queue.objects.get(type='CASUAL')
            i = unfinished_casual_matches.index(match)
            courts = Court.objects.filter(queue=casual_queue)
            court = courts[i]
            match.court = court

            match.save()

        # Grace playing in one unfinished casual match
        playedin = PlayedIn(member=grace, match=unfinished_casual_matches[0], team='A')
        playedin.save()


        # Unfinished ranked matches
        unfinished_ranked_matches = [Match(startDateTime=now, scoreA=21, scoreB=19)]

        for match in unfinished_ranked_matches:
            ranked_queue = Queue.objects.get(type='RANKED')
            i = unfinished_ranked_matches.index(match)
            courts = Court.objects.filter(queue=ranked_queue)
            court = courts[i]
            match.court = court

            match.save()

        # Joshua playing in one unfinished ranked match
        playedin = PlayedIn(member=joshua, match=unfinished_ranked_matches[0], team='A')
        playedin.save()

    def _create_people(self):
        # Create some interesteds
        interesteds = []
        interesteds.append(Interested(first_name='Interested', last_name='Guy', email='interested@illinois.edu'))

        # Create some members
        members = []
        members.append(Member(first_name="Member", last_name="Guy", dateJoined=datetime.date.today(),
                              email="member@illinois.edu", bio="I'm a member"))
        members.append(Member(first_name="Eddie", last_name="Huang", dateJoined=datetime.date.today(),
                              email="ezhuang2@illinois.edu", bio="Hi my name is Eddie. I like badminton"))
        members.append(Member(first_name="Bhuvan", last_name="Venkatesh", dateJoined=datetime.date.today(),
                              email="bhuvan2@illinois.edu"))
        members.append(Member(first_name="Daniel", last_name="Rong", dateJoined=datetime.date.today(),
                              email="drong4@illinois.edu"))
        members.append(Member(first_name="Grace", last_name="Shen", dateJoined=datetime.date.today(),
                              email="gshen3@illinois.edu"))
        members.append(Member(first_name="Jared", last_name="Franzone", dateJoined=datetime.date.today(),
                              email="jfranz2@illinois.edu"))
        members.append(Member(first_name='Joshua', last_name='Cheng', dateJoined=datetime.date.today(),
                              email='jcheng2@illinois.edu'))

        # Create some boards
        boards = []
        boards.append(BoardMember(first_name='Board', last_name='Member', dateJoined=datetime.date.today(),
                                  job="SOME_JOB", email='board_member@illinois.edu', bio="I'm a board member"))
        boards.append(BoardMember(first_name='Barack', last_name='Obama', dateJoined=datetime.date.today(),
                                  job="PRESIDENT", email='obama@gmail.com', bio='Change we can believe in'))

        print("ID's of people in the example data")
        for person in (interesteds + members + boards):
            person.save()
            print("{}: {}".format(person, person.id))
        return members

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






