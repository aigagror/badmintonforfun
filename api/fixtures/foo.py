import pandas

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

        interested_exists = Interested.objects.filter(email=email).count() > 0

        if interested_exists == False:
            # Add him as member or interested
            print('Adding {}'.format(email))
            if status is None:
                print('Adding new interested {}'.format(email))
            else:
                print('Adding new member {}'.format(email))

        else:
            print('Ignoring {}'.format(email))
