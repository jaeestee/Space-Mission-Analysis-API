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

@app.route('/help', methods=['GET'])
def help() -> str:
    """
    This function returns a human readable string that explains all the available
    routes in this API.
    Returns:
       helpOutput (str): The string that explains the routes.
    """

    helpOutput = '''usage: curl localhost:5000[<route>][?<query parameter>]\n
The different possible routes:
    /post-data                          Loads/reloads the dictionary with data from the website
    /delete-data                        Deletes all the data from the dictionary
    
    /                                   Returns the entire data set (if it exists)
    /now                                Returns the current location of the ISS
    /epochs                             Returns the list of all Epochs in the data set
    /epochs/<epoch>                     Returns the state vectors for a specific Epoch from the data set
    /epochs/<epoch>/location            Returns the location for a specific Epoch in the data set
    /epochs/<epoch>/speed               Returns the instantaneous speed for a specific Epoch in the data set
    /comment                            Returns the comments in the ISS data
    /header                             Returns the header in the ISS data
    /metadata                           Returns the metadata in the ISS data
    /help                               Returns the help text that describes each route
    
The different query parameters (only works for the "/epochs" route):
    limit=<int>                         Returns a specific integer amount of Epochs from the data set
    offset=<int>                        Returns the entire data set starting offset by a certain integer amount
    limit=<int>'&'offset=<int>          Combining the limit and offset query parameters
    example:
    /epochs?limit=15'&'offset=3         Returns the 15 Epochs from the data set offset by 3
'''
    
    return helpOutput
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
