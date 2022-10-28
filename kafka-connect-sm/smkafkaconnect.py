#!/usr/bin/env python3

import sys
import os
import json
import subprocess
import requests

import_existing_connection = False

FORWARDED_PORT='8083'
BASE_ENDPOINT='http://localhost:' + FORWARDED_PORT

def port_forward():
    #Connect to cluster
    project = subprocess.run(["gcloud config list --format 'value(core.project)' 2>/dev/null"], capture_output=True, shell=True).stdout.decode('utf-8')
    subprocess.run(["gcloud container clusters get-credentials k8s-cluster --region europe-west1 --project " + project ], shell=True)

    #Port-forward pod on port 8083 to port 25001 on localhost
    podName = subprocess.run(["kubectl get po -n pnp-sm-kafka-connect --output=jsonpath={.items..metadata.name}"], capture_output=True, shell=True).stdout.decode('utf-8')
    subprocess.run(["kubectl port-forward " + podName + " " + FORWARDED_PORT + ":8083"], shell=True)


#If necessary, terminate the process on port 25001 ( after curl commands are run )
def terminate_port_forward():
    subprocess.run(["kill $(lsof -t -i:25001)"], shell=True)


def create_connection_config():
    config = {}
    for k, v in os.environ.items():
        if k[:11] == 'CONNECTION_':
            config[k[11:].replace('__', '.')] = v
    print(config)
    #open('connection.config', 'w').write(json.dumps(config, indent=2))

def delete_connection_config():
    os.remove('connection.config')

def get_request(path: str):
    res = requests.get(BASE_ENDPOINT+path)
    if res.ok and res.status_code == 200:
        return res.json()
    sys.exit(res.raise_for_status)

def post_request(path: str, json: str):
    headers = {'content-type':'application/json'}
    res = requests.post(BASE_ENDPOINT+path, data=json, headers=headers)

def put_request(path: str, json: str):
    headers = {'content-type':'application/json'}
    res = requests.put(BASE_ENDPOINT+path, data=json, headers=headers)

def delete_request(path: str):
    res = requests.delete(BASE_ENDPOINT+path)


# ------------ terraform commands ------------
def get_connectors_list():
    connectors = get_request('/connectors')
    for connector in connectors:
        print(connector)

def create():
    print('create')

def delete():
    print('delete')


def read():
    print('read')


def update():
    print('update')


if __name__=='__main__':
    port_forward()
    print('******** CONNECTION_CONFIG ******')
    create_connection_config()
    print('******** CONNECTORS_LIST ********')
    get_connectors_list()
    terminate_port_forward()
