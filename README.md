# Machine Learning on Cloud
With this project will help you to train your machine learning models on Kubernetes cluster

## Setup

### Prerequisites

Before you begin ensure you have fulfilled the below requirements

1. Kubernetes Cluster - you have access to a Kubernetes cluster you can create a cluster on any Cloud provider , use minikube, or use a cluster on a private server
2. Install Docker - you need to install docker to build your images and push them to dockerhub.
3. Install kubectl - this will be used to communicate with the Kubernetes cluster using the terminal.
4. Requirements - add all the required Python libraries in the requirements.txt file

### Steps to setup

1. Configure your kubectl with the Kubernetes cluster

2. To create the docker image of the app use the below command
   ```bash
   docker build -t ml-on-cloud-app
   ```
3. Tag the image to push in docker hub
   ```bash
   docker tag ml-on-cloud-app:<docker-hub-username>/ml-on-cloud-app:<release-tag>
   ```
4. Push the image to the docker hub
   ```bash
   docker push <docker-hub-username>/ml-on-cloud-app:<release-tag>
   ```
5. Go to the manifest directory
   ```bash
   cd manifest
   ```
6. In the deployment.yaml change the image to the image you have created
   ```bash
       spec:
       containers:
       - name: ml-on-cloud-app-container
         image: indranil0603/ml-on-cloud-app:1.0.0 #Change the image to the image you created
   ```
7. Run the command to create your cluster
   ```bash
     kubectl apply -f .
   ```
    and check when all the pods are running using - kubectl get all
  
8. After all the pods are running the cluster is ready to get you models

### API endpoints 

1. /upload_script

   This endpoint is used to upload your model scripts to run them
    Ex
   ```bash
   curl -X POST -F "script=@model.py" http://<node-ip>:30001/upload_script
   ```

   make sure you are in the folder where you have your model.py

2. /download_output

   This endpoint is used to download the results you may have got from running the scripts i.e. returns the output of the print statements in the script.

   Ex
   ```bash
   curl -X GET http://<node-ip>:30001/download_output
   ```
   
