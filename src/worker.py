from hotqueue import HotQueue
from geopy.geocoders import Nominatim
from redis import Redis
from jobs import *

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
    current_job = rd.hget(current_jid)

    # PRASE THE ROUTE INTO USABLE VARIABLES
    current_route = current_job['route'] # full route, e.g., '/jobs/names-by-org/'

    args = current_route.split('/')

    function = args[1] # second part of the route, e.g., '/names-by-org'
    
    # EXECUTE FUNCTION IN ROUTE
    full_data = get_data()
    result = []

    if function == 'names-by-org':
        result = get_rocket_names_by_org(full_data, args[2])
    elif function == 'total-cost-by-org':
        result = get_total_cost_for_org(full_data, args[2])
    elif function == 'map-of-launches':
        result = create_map(full_data)
    elif function == 'list-all-active-rockets':
        result = list_active_rockets(full_data)
    else: 
        result = update_job_status(current_jid, 'uncompleted')
        return '\n Could not parse a proper function from the route provided.'
    
    # SAVE RESULT AND UPDATE STATUS TO COMPLETE
    rd2.set(current_jid, result)

    update_job_status(current_jid, 'completed')

    # RETURN THE NEW JOB DICTIONARY OBJECT
    new_job = rd.hget(current_jid)

    return new_job

execute_job()
