# Space-Mission-Analysis-API

This repository contains the code for an API capable of certain functionalities related to space mission analysis, developed for COE 332. The repository is organized into three folders: 'docker', 'kubernetes', and 'src'. And is capable of performing various tasks related to visualizing and organizing information on space mission rocket launches.

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
* `DELETE /jobs/clear`: This route clears the current list of jobs previously done.
* `GET /help`: This route returns a description of each available route.

### jobs.py

The `jobs.py` file contains helper functions to manage job queues. It contains the following functions:

* `get_launches_data()`: This function retrieves the launch data from the web.
* `list_of_jobs()`: This function returns a list of all the jobs in the job queue.
* `add_job(route)`: This function adds a job to the job queue.

### worker.py

The `worker.py` file contains code to run background jobs.

## Docker

The `docker` folder contains the Dockerfile used to build the Docker image. Also contained in here is the 'docker-compose.yml' file that can be used to setup the docker images quickly. The image is built using the following command:

```
docker build -t <NAME_OF_DOCKER_IMAGE> .
```

And the codebase can be setup quickly using the next command:

```
docker-compose up
```

## Kubernetes

The `kubernetes` folder contains the Kubernetes deployment files. If the user wishes to setup a kubernetes cluster use the following command on each file to deploy it:

```
kubectl apply -f <YML_FILE>
```

## Run Instructions

### Pulling and Using Existing Image from Docker Hub

To pull and use the existing image from Docker Hub, run the following command:

```
docker pull jaeestee/space_mission_analysis:wrk
docker pull jaeestee/space_mission_analysis:api
docker-compose up -d
```

Replace `<redis_ip>` with the IP address of your Redis server.

### Building a New Image from Dockerfile

To build a new Docker image, navigate to the root folder of the repository and run the following command:

```
docker build -t <DOCKER_IMAGE> .
```

### Example API Query Commands and Expected Outputs

To add the launch data to the Redis database, run the following command:

```
curl -X POST http://localhost:5000/data
```

Expected output: `Successfully loaded in the dictionary.\n`

To get a list of all the jobs in the job queue, run the following command:

```
curl -X GET http://localhost:5000/jobs
```

Expected output: A JSON array containing the details of all the jobs in the job queue.

For information on the commands and routes available use the following command:

```
curl -X POST http://localhost:5000/help
```

Expected output: A JSON array containing the details of all the jobs in the job queue.

To add a job to the job queue, run the following command with a route from the /help message:

```
curl -X POST http://localhost:5000/jobs/<ROUTE>
```