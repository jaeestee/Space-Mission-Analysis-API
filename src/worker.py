import csv
from hotqueue import HotQueue

data = {}
data['launches'] = []

with open('mission_launches.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data['launches'].append(dict(row))

# q = HotQueue("queue", host="10.233.38.133", port=6379, db=1)

def return_rocket_names_by_org(org_name):
    rocket_names = []
    for item in data['launches']:
        if item['Organisation'] == org_name:
            rocket_names.append(item['Detail'])

    return(rocket_names)

print(return_rocket_names_by_org('Roscosmos'))
