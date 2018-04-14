import pandas


data_files = ['foo.csv', 'bar.csv']

for file in data_files:
    foo = pandas.read_csv(file)
    for row_index, bar in foo[['email', 'full_name']].iterrows():
        first_name, last_name = bar.full_name.split()
        email = bar.email
        x = 0
