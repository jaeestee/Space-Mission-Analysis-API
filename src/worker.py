from hotqueue import HotQueue
from geopy.geocoders import Nominatim
from redis import Redis
from jobs import *
import json

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host = redis_ip, port=6379, db=0)
q = HotQueue('queue', host = redis_ip, port = 6379, db=1)
rd2 = Redis(host = redis_ip, port=6379, db=2)

@q.worker
def execute_job(item: str) -> dict:
    """
    Retrieve a job id from the task queue and execute the job.
    Monitors the job to completion and updates the database accordingly.

    Args:
        Item (str): the job's id from the queue object created by jobs.py

    Returns: 
        new_job (Dict): the dictionary object of the job that was completed. 
    """

    # JOBS ID 
    current_jid = item #string, JID

    # TURN STATUS TO 'IN PROGESS'
    update_job_status(current_jid, 'in progress')

    # ACQUIRE JOB'S DICTIONARY OBJECT
    current_job = json.loads(rd.get(current_jid))
    
    # PASS THE ROUTE INTO USABLE VARIABLES
    current_route = current_job['route'] # full route, e.g., '/get-rockets-by-org/org'

    args = current_route.split('/') 
    function = args[0] # the 'get-rockets-by-org'
    
    # EXECUTE FUNCTION IN ROUTE
    full_data = get_data()
    result = []

    # SETTING THE STATUS TO COMPLETED NOW SO THAT THIS LINE DOESN'T HAVE TO BE IN EVERY SINGLE IF STATEMENT
    status = 'completed'
    
    if function == 'get-rockets-by-org':
        result = get_rocket_names_by_org(full_data, args[1])
    elif function == 'total-cost-by-org':
        result = get_total_cost_for_org(full_data, args[1])
    elif function == 'map-of-launches':
        result = create_map(full_data)
    elif function == 'list-all-active-rockets':
        result = list_active_rockets(full_data)
    else: 
        status = 'incompleted' # changes to incompleted if the route doesn't exist
        result = 'Could not parse a proper function from the route provided.'
    
    # SAVE RESULT AND UPDATE STATUS TO COMPLETE
    rd2.set(current_jid, json.dumps(result))
    update_job_status(current_jid, status)

execute_job()
