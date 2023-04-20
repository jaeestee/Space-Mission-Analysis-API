import csv
from hotqueue import HotQueue
import matplotlib as plt

data = {}
data['launches'] = []

with open('mission_launches.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data['launches'].append(dict(row))

# q = HotQueue("queue", host="10.233.38.133", port=6379, db=1)

def get_rocket_names_by_org(org_name:str) -> list:
    rocket_names = []
    for item in data['launches']:
        if item['Organisation'] == org_name:
            rocket_names.append(item['Detail'])

    return(rocket_names)

def get_total_cost_for_org(org_name:str) -> float:
    cost = 0
    for item in data['launches']:
        if item['Organisation'] == org_name:
            cost += item['Price']

    return(cost) # cost is in millions

def get_success_rate_for_org(org_name:str) -> float:
    total_launches = 0
    successful_launches = 0
    for item in data['launches']:
        if item['Organisation'] == org_name:
            total_launces += 1
            if item['Mission_Status'] == 'Success':
                successful_launches += 1
    success_rate = success_launches / total_launches

    return(success_rate)

def list_active_rockets() -> list:
    active_rockets = []
    for item in data['launches']:
        if item['Rocket_Status'] == 'StatusActive':
            active_rockets.append(item['Detail'][:item['Detail'].index(" |")])
    active_rockets = list(set(active_rockets)) # remove duplicates from list
    return(active_rockets)

print(list_active_rockets())
