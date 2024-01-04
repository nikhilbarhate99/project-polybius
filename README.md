# project-polybius

## Overview

project-polybius is a text based game that uses Large Language Models to generate new experiences for the player.
This repo provides the code to deploy it on cloud and a client to interact with the deployed system.


## Instructions

### Running the services
I have tested this code on google cloud platform's kubernetes engine (GKE) because it uses GCP's Vertex AI APIs for text generation, but technically it can run on any cloud or locally provided that an appropriate `generate_text()` function (imported in `llm-handler.py`) is implemented in its corresponding api_helper file. If you are using VertexAI on GKE then make sure that API access to VertexAI is enabled.

After starting a kubernetes cluster, clone the repo:
```
git clone https://github.com/nikhilbarhate99/project-polybius.git
cd project-polybius
``` 
Install minio on kubernetes cluster using helm (make sure helm is installed before)
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install -f ./minio/minio-config.yaml -n minio-ns --create-namespace minio-proj bitnami/minio
```
Deploy the system on the cluster, this will start running all the pods, services, deployments required for the game.
```
./deploy-cloud.sh
```
Run the following command to expose the rest service using:
```
kubectl apply -f expose-rest.yaml
```
After a while, the kubernetes cluster will assign an external IP to the `expose-rest-svc` service. 
You can check this by running:
```
kubectl get all
```
**Important:** Now copy that external IP to the `REST_HOST` variable in the `global_variables.py` file. 
This allows the client to find the rest service.

### Running the client
finally, once all the servcies are running on the cluster, we can install all the requirements in a virtual env and use the client to play the game:
```
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 polybius_client.py
```
As long as the cluster is running, multiple clients can play the game and their games will be saved in the Database.

**Note:** To play the game (on client side) four files are required which can be zipped an distributed to users: `polybius_client.py`, `global_variables.py`, `utils.py`, `requirements.txt`

## System

The current architecture is simple as illustrated in the figure
![](https://github.com/nikhilbarhate99/dcsc-project-polybius/blob/main/media/polybius_fig.png)


## Examples

| ![](https://github.com/nikhilbarhate99/dcsc-project-polybius/blob/main/media/game_pic_1.png) | ![](https://github.com/nikhilbarhate99/dcsc-project-polybius/blob/main/media/game_pic_2.png)  |
| :---:|:---: |



## To Do

- [ ] Add Authentication
- [ ] Better error handling for REST Success/Failures
- [ ] Change to a JSON DB
- [ ] Fix UI issues
- [ ] Use logs service
- [ ] Add support for different settings/genre for game stories
- [ ] Implement `generate_text()` function for other LLM APIs e.g. Gemini, GPT4 etc.

