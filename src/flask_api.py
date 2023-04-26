from flask import Flask, request, send_file
import requests, redis, json
import os
import jobs as j 


redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

app = Flask(__name__)

rd = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)

@app.route('/data', methods=['DELETE'])
def delete_data() -> str:
    """
    This function deletes the data completely.

    Returns:
        message (str): Message saying that the data was deleted.
    """

    #deletes the entire data set from the redis client
    rd.flushdb()

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
    rd.set('data', json.dumps(data))

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
    results = rd2.get(jid)
    return results
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
