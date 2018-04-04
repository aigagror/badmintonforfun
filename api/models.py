from django.core.exceptions import ValidationError
from django.db import models
from .cursor_api import serializeDate

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
        ret = str(self.leader) + ':'
        for member in members:
            ret += ' {}'.format(str(member))
        return ret


class Court(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True, blank=True)

class Tournament(models.Model):
    date = models.DateField('date of tournament', unique=True)
    endDate = models.DateField('end date of tournament', unique=True, null=True, blank=True)

class BracketNode(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    level = models.IntegerField()
    sibling_index = models.IntegerField()
    match = models.ForeignKey('Match', on_delete=models.SET_NULL, null=True, blank=True)

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
    bio = models.CharField(max_length=500, default='', blank=True)

    def clean(self):
        if self.party is not None:
            leader = self.party.leader
            other_party_members = Member.objects.filter(party=self.party)
            if leader == self:
                raise ValidationError('Cannot assign member to party that he/she is the party\'s leader')
            if other_party_members.count() == 3:
                raise ValidationError('Party is full')


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
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True, blank=True)

    endDateTime = models.DateTimeField('date time ended', null=True, blank=True)

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

        return 'A{}-B{}:{}-{}'.format([str(m) for m in team_a_members], [str(m) for m in team_b_members], self.scoreA, self.scoreB)

class PlayedIn(models.Model):
    class Meta:
        unique_together = (('member', 'team', 'match'),)

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.CharField(max_length=64, choices=TEAMS)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.member, self.match)


class Announcement(models.Model):
    date = models.DateTimeField('date of announcement')
    title = models.CharField(max_length=64)
    entry = models.CharField(max_length=500)

    def __str__(self):
        return '{}'.format(self.title)

class Schedule(models.Model):
    date = models.DateField('date of session', unique=True)
    number_of_courts = models.IntegerField(default=4)

    def __str__(self):
        return '{}'.format(self.date)

