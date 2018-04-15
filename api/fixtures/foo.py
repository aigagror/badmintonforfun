import pandas
import datetime

from api.models import *

data_files = ['api/fixtures/foo.csv', 'api/fixtures/bar.csv']

for file in data_files:
    foo = pandas.read_csv(file)
    for row_index, bar in foo[['email', 'full_name', 'status']].iterrows():
        name_words = bar.full_name.split()
        first_name = name_words[0]
        last_name = name_words[-1]
        email = bar.email
        status = bar.status

        interested_exists = Interested.objects.filter(email=email).exists()

        if interested_exists == False:
            # Add him as member or interested
            if status == 'paid':
                print('Adding new member {}'.format(email))
                member = Member(first_name=first_name, last_name=last_name, email=email, dateJoined=datetime.date.today())
                member.save()
            else:
                print('Adding new interested {}'.format(email))
                interested = Interested(first_name=first_name, last_name=last_name, email=email)
                interested.save()

        else:
            print('Ignoring {}'.format(email))
