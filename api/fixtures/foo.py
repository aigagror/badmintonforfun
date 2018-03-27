import json

if __name__ == '__main__':
    interesteds = []
    data = json.load(open('fixtures.json'))
    for d in data:
        if d['model'] == 'api.interested':
            interesteds.append(d['pk'])

    for d in data:
        if d['model'] == 'api.interested': # Add new pk and move email
            d['fields']['email'] = d['pk']
            d['pk'] = interesteds.index(d['pk'])

        if d['model'] == 'api.member' or d['model'] == 'api.boardmember':
            d['pk'] = interesteds.index(d['pk'])

        if d['model'] == 'api.playedin':
            d['fields']['member'] = interesteds.index(d['fields']['member'])

        if d['model'] == 'api.campaign':
            d['fields']['campaigner'] =  interesteds.index(d['fields']['campaigner'])

    json.dump(data, open('foo.json', 'w'), indent=4)