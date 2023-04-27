from flask import Flask, request, send_file
import requests, json
import os
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
    This function adds the DATA dictionary object with the data from the web and returns
    a success message.

    Returns:
        message (str): Message saying that the data was successfully reloaded.
    """

    data = j.get_launches_data()

    #stores the data into the redis client, but as a serialized dictionary string
    rd2.set('data', json.dumps(data))

    #the success message
    message = 'Successfully reloaded the dictionary with the data from the web!\n'

    return message

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs():

    jobsList = j.list_of_jobs()
    return jobsList

@app.route('/jobs/<string:route>', methods=['POST'])
def post_job(route: str) -> dict:
    j.add_job(route)
    return 'Successfully queued a job! \nTo view the status of the job, curl /jobs.\n'

@app.route('/jobs/<string:jid>', methods=['GET'])
def get_job(jid: str) -> dict:
    try:
        results = rd2.get(jid)
    except TypeError:
        return 'The job ID is invalid, please try again.\n'
        
    return results

@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    
    rd.flushdb()
    
    return 'Successfully cleared the jobs list!\n'

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
