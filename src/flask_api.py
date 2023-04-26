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

@app.route('/jobs', methods=['POST'])
def jobs_api():
    
    try:
        job = request.get_json(force=True)
    except Exception as e:
          return True, json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    return json.dumps(j.add_job(job['route'], job['status']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
