from flask import Flask, request, send_file
import requests, redis, json
import os
import matplotlib.pyplot as plt

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

app = Flask(__name__)

rd = redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
