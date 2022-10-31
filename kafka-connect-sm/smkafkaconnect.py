#!/usr/bin/env python3

from distutils.command.config import config
from math import fabs
from operator import truediv
import re
import sys
import os
import json
import subprocess
from this import d
import requests

import_existing_connection = False

CONNECTION_NAME_KEY = 'CONNECTION_name'

FORWARDED_PORT='25001'
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
    subprocess.run(["kill $(lsof -t -i:"+FORWARDED_PORT+")"], shell=True)


def create_post_payload():
    payload = {}
    payload['name'] = os.environ[CONNECTION_NAME_KEY]
    payload['config'] = create_config()
    return payload

def create_config():
    config = {}
    for k, v in os.environ.items():
        if k != CONNECTION_NAME_KEY and k[:11] == 'CONNECTION_':
            config[k[11:].replace('__', '.')] = v
    return config

def get_request(path: str):
    return requests.get(BASE_ENDPOINT+path)
    

def post_request(path: str, payload: str):
    headers = {'content-type':'application/json'}
    res = requests.post(BASE_ENDPOINT+path, data=payload, headers=headers)
    if res.status_code != 200 and res.status_code != 201:
        sys.exit(res.raise_for_status)
    

def put_request(path: str, payload: str):
    headers = {'content-type':'application/json'}
    res = requests.put(BASE_ENDPOINT+path, data=payload, headers=headers)
    if res.status_code != 200:
        sys.exit(res.raise_for_status)

def delete_request(path: str):
    res = requests.delete(BASE_ENDPOINT+path)
    if res.status_code == 404:
        print(f'Connector {os.environ[CONNECTION_NAME_KEY]} does not exists')
    elif res.status_code != 200 and res.status_code != 204:
        sys.exit(res.raise_for_status)

def get_connectors_list():
    result = get_request('/connectors')
    if result.status_code == 200:
        return result.json()
    else:
        sys.exit(result.raise_for_status) 

def get_connector(name: str):
    result =  get_request('/connectors/'+name)  
    if result.status_code == 200:
        return result.json()
    elif result.status_code == 404:
        return None
    else:
        sys.exit(result.raise_for_status) 

def connector_exists():
    if os.environ[CONNECTION_NAME_KEY]:
        print(os.environ[CONNECTION_NAME_KEY])
        result = get_connector(os.environ[CONNECTION_NAME_KEY])
        if result:
            return True
    return False

def save():
    if not connector_exists():
        print(f'{os.environ[CONNECTION_NAME_KEY]} not exists. Creating Connector')
        payload = create_post_payload()
        post_request('/connectors',json.dumps(payload))
        print(f'{os.environ[CONNECTION_NAME_KEY]} New Config : ')
        print(get_connector(os.environ[CONNECTION_NAME_KEY]))
    else:
        print(f'{os.environ[CONNECTION_NAME_KEY]} exists. Updating Connector')
        payload = create_config()
        put_request(f'/connectors/{os.environ[CONNECTION_NAME_KEY]}/config',json.dumps(payload))
        print(f'{os.environ[CONNECTION_NAME_KEY]} New Config : ')
        print(get_connector(os.environ[CONNECTION_NAME_KEY]))

def delete():
    delete_request('/connectors/'+os.environ[CONNECTION_NAME_KEY])
    print(f'{os.environ[CONNECTION_NAME_KEY]} Deleted')


def read():
    result = get_connectors_list()
    print(result)


if __name__=='__main__':
    #set_environ_items()
    if not os.environ[CONNECTION_NAME_KEY]:
        sys.exit('Connection Name does not exists !!')
    port_forward()
    read()
    # if len(sys.argv) > 1:
    #     if sys.argv[1]=='create':
    #         save()
    #     elif sys.argv[1]=='update':
    #         save()
    #     elif sys.argv[1]=='delete':
    #         delete()
    #     elif sys.argv[1]=='read':
    #         read()
    terminate_port_forward()
