import datetime
from api.models import *


def create_election():
    voter = Member(first_name='Michelle', last_name='Obama', email='michelle@usa.com',
                   dateJoined=datetime.date.today())
    voter.save()
    campaigner = Member(first_name='Barack', last_name='Obama', email='obama@usa.com',
                        dateJoined=datetime.date.today())
    campaigner.save()
    election = Election(date=datetime.date.today())
    election.save()
    campaign = Campaign(job='PRESIDENT', campaigner=campaigner, election=election)
    campaign.save()
    return election, campaign, voter


