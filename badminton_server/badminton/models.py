import datetime

from django.db import models
from django.utils import timezone


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

class Queue(models.Model):
    type = models.CharField(max_length=64, choices=QUEUE_TYPE)

class Court(models.Model):
    number = models.IntegerField()
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True, blank=True)

class Tournament(models.Model):
    date = models.DateField('date of tournament')

class Interested(models.Model):
    name = models.CharField(max_length=64)
    formerBoardMember = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Member(Interested):
    level = models.IntegerField(default=0)
    private = models.BooleanField(default=False)
    dateJoined = models.DateField('date joined')
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True, blank=True)


class BoardMember(Member):
    job = models.CharField(max_length=64, choices=JOBS)

class Election(models.Model):
    date = models.DateField('date of the election')

class Votes(models.Model):
    votee = models.ForeignKey(Member, related_name='votee', on_delete=models.SET_NULL, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(Member, related_name='voter', on_delete=models.CASCADE)

class Campaign(models.Model):
    job = models.CharField(max_length=64, choices=JOBS)
    pitch = models.CharField(max_length=500)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    campaigner = models.ForeignKey(Member, on_delete=models.CASCADE)

class Team(models.Model):
    memberA = models.ForeignKey(Member, related_name='memberA', on_delete=models.PROTECT)
    memberB = models.ForeignKey(Member, related_name='memberB', on_delete=models.SET_NULL, null=True, blank=True)

class Match(models.Model):
    startDate = models.DateTimeField('date started')
    scoreA = models.IntegerField()
    scoreB = models.IntegerField()
    teamA = models.ForeignKey(Team, related_name='teamA', on_delete=models.SET_NULL, null=True)
    teamB = models.ForeignKey(Team, related_name='teamB', on_delete=models.SET_NULL, null=True)
    court = models.ForeignKey(Court, on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True)

class FinishedMatch(Match):
    endDate = models.DateTimeField('date ended')