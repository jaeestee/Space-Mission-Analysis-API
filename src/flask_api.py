from flask import Flask, request, send_file
import requests, json, os
import jobs as j 
from redis import Redis
from hotqueue import HotQueue

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

rd = Redis(host = redis_ip, port=6379, db=0)
q = HotQueue('queue', host = redis_ip, port = 6379, db=1)
rd2 = Redis(host = redis_ip, port=6379, db=2)

app = Flask(__name__)

@app.route('/data', methods=['DELETE'])
def delete_data() -> str:
    """
    This function deletes the data completely.

    Returns:
        message (str): Message saying that the data was deleted.
    """

    #deletes the entire data set from the redis client
    rd2.set('data', json.dumps({}))

    message = 'Successfully deleted all the data from the dictionary!\n'
    return message

@app.route('/data', methods=['POST'])
def post_data() -> str:
    """
    This function gets the launch data and posts it to the rd2 redis database.

    Returns:
        message (str): Message saying that the data was successfully reloaded.
    """

    #pulling the data using the function from jobs.py
    data = j.get_launches_data()

    #stores the data into the redis client
    rd2.set('data', json.dumps(data))

    #the success message
    message = 'Successfully reloaded the dictionary with the data from the web!\n'
    return message

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs() -> list:
    """
    This function returns the list of current jobs that the user has queried to the api.
    It contains the job ID, the route that the user requested, and the status of the job.
    
    Returns:
        jobsList (list): The list of current jobs.
    """
    
    jobsList = j.list_of_jobs()
    return jobsList

@app.route('/jobs/<string:route>', methods=['POST'])
def post_job(route: str) -> str:
    """
    This function adds a job that the user requested into the jobs queue. Then it will
    return a success message.
    
    Returns:
        message (str): The success message.
    """
    
    #sends the route that the user requested to jobs.py and it takes care of the rest
    j.add_job(route)
    message = 'Successfully queued a job! \nTo view the status of the job, curl /jobs.\n'
    return message

@app.route('/jobs/<string:jid>', methods=['GET'])
def get_job(jid: str) -> dict:
    """
    This function returns the results of a specific job using its job ID. If the job ID is
    invalid, it will return a falure message.
    
    Returns:
        results (dict): The results of the job from the rd2 redis database.
        error message (str): An error message saying that the job ID is invalid.
    """
    
    try:
        results = rd2.get(jid)
    except TypeError:
        return 'The job ID is invalid, please try again.\n'
        
    return results

@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    """
    This function clears the list of jobs in case the user wanted a fresh jobs list.
    Returns a success message.
    
    Returns:
        message (str): The success message.
    """
    
    rd.flushdb()
    message = 'Successfully cleared the jobs list!\n'
    return message

@app.route('/help', methods=['GET'])
def help() -> str:
    """
    This function returns a human readable string that explains all the available
    routes in this API.
    Returns:
       helpOutput (str): The string that explains the routes.
    """

    helpOutput = '''usage: curl -X [COMMAND] localhost:5000/<ROUTE>\n
Different COMMANDS: 
    GET                                 Responsible for returning any data. 
    POST                                Responsible for generating any data. 
    DELETE                              Responsible for deleting any data. 

GET routes:
    /jobs                               Returns list of all previous jobs.
    /jobs/<string:JOB_ID>               Returns specific job given job's id.
    /help                               Returns the help text that describes each route
    
POST routes:
    /data                               Updates the current variable data with the current .csv.
    /jobs/<string:ROUTE>                Queues a job specified by ROUTE, and completes it.

DELETE routes:
    /data                               Deletes all of the launch mission data.
    /jobs/clear                         Clears the current list of jobs.
'''
    
    return helpOutput
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
