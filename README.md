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

# Kubernetes Cluster:
## Setting Up The Cluster:
To set up the cluster, first run these commands while in the `kubernetes/prod` directory:
```bash
$ kubectl apply -f app-prod-api-deployment.yml
$ kubectl apply -f app-prod-api-ingress.yml
$ kubectl apply -f app-prod-api-nodeport.yml
$ kubectl apply -f app-prod-db-deployment.yml
$ kubectl apply -f app-prod-db-pvc.yml
$ kubectl apply -f app-prod-db-service.yml
$ kubectl apply -f app-prod-wrk-deployment.yml
```
> The deployment-python-debug.yml will be used to test whether the cluster is functioning correctly

Next, use this command to make sure everything is now running properly:
```bash
$ kubectl get pods
```

The output should look similar to this:
```
NAME                                    READY   STATUS    RESTARTS   AGE
jo25672-test-geneapi-67b8c5b8d4-hcg8s   1/1     Running   0          18m
jo25672-test-geneapi-67b8c5b8d4-w5f2w   1/1     Running   0          17m
jo25672-test-redis-5678f8fd88-6njvq     1/1     Running   0          16m
py-debug-deployment-f484b4b99-tprrp     1/1     Running   0          17m
```
> IMPORTANT: Make sure that the status all say Running, else something failed. If it seems to be building, give it some time and try the command again.

Now everything is set up!


## Testing the Kubernetes Cluster:
To test the cluster and make sure the flask api is functioning properly, use this command to enter the python pod:
```bash
$ kubectl exec -it <py-debug-deployment pod name> -- /bin/bash
```
> IMPORTANT: Make sure to copy and paste the pod name from the pods list that you got earlier.
> Example:
> ```bash
> $ kubectl exec -it py-debug-deployment-f484b4b99-tprrp -- /bin/bash
> ```

If done properly, the command line should change to something like this:
```bash
root@py-debug-deployment-f484b4b99-tprrp:/#
```

Now you can curl using the queries below in the **Queries To Use** section. Just make sure to have the ```localhost``` swapped with ```jo25672-test-geneapi-service```.
For example:
```bash
root@py-debug-deployment-f484b4b99-tprrp:/# curl jo25672-test-geneapi-service:5000/genes
```


## Creating Your Own Image for K8:
To build a new image from the **Dockerfile** present in this directory, run this command:
```
$ docker build -t <dockerhubusername>/gene_api:hw8 .
```
> **IMPORTANT: Make sure to be in the same directory as the ``Dockerfile`` and DO NOT FORGET THE "." at the very end of this command!!!**

If done properly, the output should look similar to this:
```
Sending build context to Docker daemon  19.46kB
Step 1/6 : FROM python:3.8.10
 ---> a369814a9797
Step 2/6 : RUN pip install Flask==2.2.2
 ---> Using cache
 ---> bbf69ba6f74f
Step 3/6 : RUN pip install requests==2.22.0
 ---> Using cache
 ---> 4ffa49d19ef5
Step 4/6 : RUN pip install redis==4.5.1
 ---> Using cache
 ---> c5c9cd8cc964
Step 5/6 : COPY gene_api.py /gene_api.py
 ---> 06dc8f8ebd53
Step 6/6 : CMD ["python", "gene_api.py"]
 ---> Running in b7b7f007b29f
Removing intermediate container b7b7f007b29f
 ---> 2a2936689823
Successfully built 2a2936689823
Successfully tagged jaeestee/gene_api:hw8
```
Now you have successfully created your own image!


## Pushing the New Image for K8:
Now that your own image was created, it must be pushed for the Kubernetes Cluster to function properly. To do so, use this command:
```bash
$ docker push <dockerhubusername>/gene_api:hw8
```

If done properly, the output should look similar to this:
```
The push refers to repository [docker.io/jaeestee/gene_api]
b7441079a5eb: Layer already exists
739f6e8204e4: Layer already exists
e91a4bead186: Layer already exists
43b09f4e921f: Layer already exists
6ab97ebc930b: Layer already exists
e726038699f2: Layer already exists
b8e0cb862793: Layer already exists
4b4c002ee6ca: Layer already exists
cdc9dae211b4: Layer already exists
7095af798ace: Layer already exists
fe6a4fdbedc0: Layer already exists
e4d0e810d54a: Layer already exists
4e006334a6fd: Layer already exists
hw8: digest: sha256:a722680b5e6dff7fac131dc8128bc1563700e88c67d7c617745ed227b2f066a1 size: 3057
```


## Editing a File for K8:
Since you have your own image now, you need to edit the ```jo25672-test-geneapi-deployment.yml``` file. To do this, enter into any text editing command like this:
```bash
$ emacs jo25672-test-geneapi-deployment.yml
```

If done properly, the window should look like this:
```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jo25672-test-geneapi
  labels:
    app: jo25672-test-geneapi
    username: jo25672
    env: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: jo25672-test-geneapi
  template:
    metadata:
      labels:
        app: jo25672-test-geneapi
        username: jo25672
        env: test
    spec:
      containers:
        - name: jo25672-test-geneapi
          imagePullPolicy: Always
          image: jaeestee/gene_api:hw8
          env:
          - name: FLASK_APP
            value: "gene_api.py"
          - name: REDIS_IP
            value: jo25672-test-redis-service
          ports:
          - name: http
            containerPort: 5000
```

Now, go all the way to the bottom where it says "image: jaeestee/gene_api:hw8" and make sure that the ```jaeestee``` is switched with your own dockerhub username.
To save the file in ```emacs```, press ```Ctrl+X``` and then ```Ctrl+C```, where it will prompt you to save. Simply press ```y``` on the keyboard.

You have now completed making your own image for the K8 cluster!


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

### Endpoints
|Route|Method|What it should do|
|---|---|---|
|``/data``|POST|Loads in the data.|
|``/data``|DELETE|Deletes the data.|
|``/data``|GET|Prints the data.|
|``/jobs``|GET|Prints the jobs.|
|``/jobs/<job_id>``|GET|Prints a specific job.|
|``/jobs/<route>``|POST|Posts a job to be executed.|
|``/jobs/clear``|DELETE|Deletes the current list of jobs.|
|``/help``|GET|Gets the help message.|
