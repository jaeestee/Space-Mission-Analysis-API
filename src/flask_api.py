from flask import Flask, request, send_file
import requests, redis, json
import os
import matplotlib.pyplot as plt

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
    
    #stores the data from the get request into the data variable and converts it into a dictionary
    data = requests.get(url='https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json')
    data = data.json()

    #stores the data into the redis client, but as a serialized dictionary string
    rd.set('data', json.dumps(data))

    #the success message
    message = 'Successfully reloaded the dictionary with the data from the web!\n'
    
    return message
    
@app.route('/data', methods=['GET'])
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
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
