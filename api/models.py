from django.core.exceptions import ValidationError
from django.db import models
from .cursor_api import serializeDate
import base64
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

JOBS = (
        ('PRESIDENT', 'President'),
        ('TREASURER', 'Treasurer'),
        ('OFFICER', 'Officer'),
    )

QUEUE_TYPE = (
        ('CASUAL', 'Casual'),
        ('RANKED', 'Ranked'),
        ('KOTH', 'King of the Hill'),
    )

ELIMINATION_TYPE = (
    ('SINGLE', 'Single'),
    ('DOUBLE', 'Double'),
)

MATCH_TYPE = (
    ('SINGLES', 'Singles'),
    ('DOUBLES', 'Doubles'),
)

TEAMS = (
        ('A', 'A'),
        ('B', 'B'),
    )

class Queue(models.Model):
    type = models.CharField(max_length=64, choices=QUEUE_TYPE, unique=True)

    def __str__(self):
        parties = Party.objects.filter(queue=self)
        ret = self.type
        for party in parties:
            ret += ' | {}'.format(party)
        return ret

class Party(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)

    def __str__(self):
        members = Member.objects.filter(party=self.id)
        ret = ''
        for member in members:
            ret += '{}'.format(str(member))
        return ret


class Court(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True, blank=True)
    match = models.ForeignKey('Match', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'Queue: {}, Match: {}'.format(self.queue.type if self.queue is not None else 'None', self.match)

class Tournament(models.Model):
    date = models.DateField('date of tournament', unique=True)
    endDate = models.DateField('end date of tournament', unique=True, null=True, blank=True)
    elimination_type = models.CharField(max_length=64, choices=ELIMINATION_TYPE, default=ELIMINATION_TYPE[0][0])
    match_type = models.CharField(max_length=64, choices=MATCH_TYPE, default=MATCH_TYPE[0][0])

class BracketNode(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    level = models.IntegerField()
    sibling_index = models.IntegerField()

    class Meta:
        unique_together = (('tournament', 'level', 'sibling_index'),)

class Interested(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    formerBoardMember = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Member(Interested):
    level = models.IntegerField(default=0)
    private = models.BooleanField(default=False)
    dateJoined = models.DateField('date joined')
    party = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)

    in_tournament = models.BooleanField(default=False)

    bio = models.CharField(max_length=500, default='', blank=True)
    picture = models.TextField(null=True, blank=True)



class BoardMember(Member):
    job = models.CharField(max_length=64, choices=JOBS)

class Election(models.Model):
    date = models.DateField('date of the election', unique=True)
    endDate = models.DateField('election end date', null=True, blank=True)

    def __str__(self):
        return '{} to {}'.format(self.date, self.endDate)


class Campaign(models.Model):
    job = models.CharField(max_length=64, choices=JOBS)
    pitch = models.CharField(max_length=500)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    campaigner = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return '{} for {}: {}'.format(self.campaigner, self.job, self.election)


class Vote(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='vote', on_delete=models.CASCADE)
    voter = models.ForeignKey(Member, related_name='voter', on_delete=models.CASCADE)

    def __str__(self):
        return '{} voted for {}: {}'.format(self.voter, self.votee, self.election)


class Match(models.Model):
    startDateTime = models.DateTimeField('date time started')
    scoreA = models.IntegerField(default=0, blank=True)
    scoreB = models.IntegerField(default=0, blank=True)

    endDateTime = models.DateTimeField('date time ended', null=True, blank=True)

    bracket_node = models.ForeignKey(BracketNode, related_name='match', on_delete=models.SET_NULL, blank=True, null=True)

    def clean(self):
        if self.endDateTime is not None:
            if abs(self.scoreA - self.scoreB) < 2:
                raise ValidationError('Violates win by 2 rule')
            if self.scoreA < 21 and self.scoreB < 21:
                raise ValidationError('Someone should have at least 21 points')

    def __str__(self):
        plays = PlayedIn.objects.filter(match=self)
        team_a_members = []
        team_b_members = []
        for play in plays:
            if play.team == TEAMS[0][0]:
                team_a_members.append(play.member)
            elif play.team == TEAMS[1][0]:
                team_b_members.append(play.member)

        return 'A|{}{}\tB|{}{}\tTime|{}-{}'.format(self.scoreA, [str(m) for m in team_a_members],
                                                 self.scoreB, [str(m) for m in team_b_members],
                                                 self.startDateTime.time().strftime('%H:%M'),
                                                 self.endDateTime.time().strftime('%H:%M') if self.endDateTime is not None else '')

class PlayedIn(models.Model):
    class Meta:
        unique_together = (('member', 'team', 'match'),)

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.CharField(max_length=64, choices=TEAMS)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.member, self.match)


class Announcement(models.Model):
    date = models.DateField('date of announcement')
    title = models.CharField(max_length=64)
    entry = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.title)

class Schedule(models.Model):
    date = models.DateField('date of session', unique=True)
    number_of_courts = models.IntegerField(default=4)

    def __str__(self):
        return '{}'.format(self.date)

