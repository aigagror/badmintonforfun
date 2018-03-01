import datetime

from django.db import models
from django.utils import timezone


# Create your models here.

class Interested(models.Model):
    name = models.CharField(max_length=64)
    formerBoardMember = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Member(Interested):
    level = models.IntegerField(min_value=0, default=0)
    private = models.BooleanField(default=False)
    dateJoined = models.DateField('date joined')


class BoardMember(Member):
    JOBS = (
        ('PRESIDENT', 'President'),
        ('TREASURER', 'Treasurer'),
        ('OFFICER', 'Officer'),
    )
    job = models.CharField(choices=JOBS)

