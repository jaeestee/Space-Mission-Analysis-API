import csv
from hotqueue import HotQueue
import matplotlib as plt

def generate_jid():
    """
      Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def generate_job_key(jid):
    """
      Generate the redis key from the job id to be used when storing, retrieving or updating
      a job in the database.
    """
    return 'job.{}'.format(jid)

def instantiate_job(jid, status, start, end):
    """
      Create the job object description as a python dictionary. Requires the job id, status,
      start and end parameters.
    """
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'start': start,
                'end': end
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
    }

def save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hset(job_key, job_dict)

def queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)

def add_job(start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = instantiate_job(jid, status, start, end)
    save_job(jid, job_dict)
    queue_job(jid)
    return job_dict

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

def populate_launch_data():
    data = {}
    data['launches'] = []

    with open('mission_launches.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['launches'].append(dict(row))
    return(data)
# q = HotQueue("queue", host="10.233.38.133", port=6379, db=1)

def get_data() -> dict:
    """
    This function returns the data from Redis, but only if it exists or is empty.
    Otherwise it will return a message saying that the data does not exist.

    Returns:
        redisData (dict): The entire gene data.
    """

    #try-except block that returns if the data doesn't exist and an error occurs because of it
    try:
        #un-seralizing the string into a dictionary
        redisData = json.loads(rd.get('data'))
    except NameError:
        return 'The data does not exist...\n'
    except TypeError:
        return 'The data does not exist...\n'

    return redisData

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
