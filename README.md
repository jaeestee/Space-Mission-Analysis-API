# Space-Mission-Analysis-API

This repository contains the code for an API capable of certain functionalities related to space mission analysis, developed for the "Software Engineering" class. The repository is organized into three folders: 'docker', 'kubernetes', and 'src'. 

## src Folder

The `src` folder contains three main files:
* `flask_api.py`: This file contains the Flask API implementation.
* `jobs.py`: This file contains helper functions to manage job queues.
* `worker.py`: This file contains code to run background jobs.

### flask_api.py

The `flask_api.py` file contains the implementation of the Flask API. It exposes several routes to perform different actions. Here's a brief description of each route:

* `DELETE /data`: This route deletes all the data stored in the Redis database.
* `POST /data`: This route adds the launch data to the Redis database.
* `GET /jobs`: This route returns a list of all the jobs in the job queue.
* `POST /jobs/<string:route>`: This route adds a job to the job queue.
* `GET /jobs/<string:jid>`: This route returns the status of the job with the given job ID.
* `DELETE /jobs/clear`: This route clears the job queue.
* `GET /help`: This route returns a description of each available route.

### jobs.py

The `jobs.py` file contains helper functions to manage job queues. It contains the following functions:

* `get_launches_data()`: This function retrieves the launch data from the web.
* `list_of_jobs()`: This function returns a list of all the jobs in the job queue.
* `add_job(route)`: This function adds a job to the job queue.

### worker.py

The `worker.py` file contains code to run background jobs.

## Docker

The `docker` folder contains the Dockerfile used to build the Docker image. The image is built using the following command:

```
docker build -t space-mission-analysis-api .
```

## Kubernetes

The `kubernetes` folder contains the Kubernetes deployment and service configuration files.

## Run Instructions

### Pulling and Using Existing Image from Docker Hub

To pull and use the existing image from Docker Hub, run the following command:

```
docker pull <username>/space-mission-analysis-api
docker run -p 5000:5000 -e REDIS_IP=<redis_ip> <username>/space-mission-analysis-api
```

Replace `<username>` with your Docker Hub username and `<redis_ip>` with the IP address of your Redis server.

### Building a New Image from Dockerfile

To build a new Docker image, navigate to the root folder of the repository and run the following command:

```
docker build -t space-mission-analysis-api .
```

### Launching the Containerized App and Redis Using Docker Compose

To launch the containerized app and Redis using Docker Compose, navigate to the root folder of the repository and run the following command:

```
docker-compose up
```

### Example API Query Commands and Expected Outputs

To add the launch data to the Redis database, run the following command:

```
curl -X POST http://localhost:5000/data
```

Expected output: `Successfully reloaded the dictionary with the data from the web!`

To get a list of all the jobs in the job queue, run the following command:

```
curl -X GET http://localhost:5000/jobs
```

Expected output: A JSON array containing the details of all the jobs in the job queue.

To add a job to the job queue, run the following command:

```
curl -X POST http://localhost:5000