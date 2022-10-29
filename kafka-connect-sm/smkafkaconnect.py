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

# credential = {
#         "type": "service_account",
#         "project_id": "pnp-staging-dcfd",
#         "private_key_id": "0f364db8bd98f358c042893df4fe2dc41672bdf4",
#         "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0h+bLJpowJ75y\nuo3t5A+MHjpW0ZrmfwGa+c65a2UBE2+W2pszVGNq2gH3oYCfK4Ay4qeSv7kZbLJk\nlGgeRNZ5DO9+1esJlpoCBrZC5B17vjg9gCrhvpyLYrWXQDzpNeOVC8mTVKAsun1X\nC5JTEfLPa+LX8wSK50WEWa68IuSNKMb1bTlPxpjTAW1RYyMuMWiXDnPi2VBsqUcq\n5BcC5/CnD8vMy7DB8NGbJXGcnYt5CY0MiM+DOTd5RKAKx+lr8DfhzrNdjb7rbWLr\nSm4MfyBpAbSCgvQoPHgqbXeK5jzG+6uST4Lsy86f7AWUBZ2z2UXlBpVkDVj87IRu\nz5VcrdO9AgMBAAECggEABWCG30YnEYgdhA1KbOt+Cw5bbnqPwo3F3nfSUHOCbqXF\njRi1xrGcxHH53QZSbms9Rka59wT+3mL+bUB+WWhzeueHup9kgMSbkbPhedyRhD4G\nLs7CeDbVMtGd1wNyzP9t5+KR/nFm0+46DX2qvg6qzMLJ3uS+HeUFjQueyLvBUvL3\nD5gW70Z17FWla5XE1SxJgpB20/O8Wz1v9SO/XwUgxLaF9DQMDbm4GIAts4CgdUM6\nmSa4qTuku4IMx575lC/S9V0Nb9zN6k3VRxv+RsNDm7PSz3X5RWL65TfmO65Cg+hP\nLrbN0HKtpngGfcM62dpE5+PSf1/Ctt/oU6PPqGMIAQKBgQD1A3rx+qOZceihl4aM\n4PP59IxOEeaW5ccU0TfvPlk4HXe54czNV7gUBfHugVlc76OYqX4F5PynKOcCP8fO\nODDz/yK7babdTsHqrug1VsC4rg58Y2pgxskfimZDWBpmq4ZQnSY7ywTUH3nX8sDE\nQth2Qaq1QOk8CgwhHlyFNGS+DQKBgQC8oDjERLEBHG6ZNDKQq4Ty+24H3CckrXfP\nY62pgNHlaSmOaa8d78J4C7j+bVJZ1HSpUhUKrFxOU6xEZLzNJex99Y45ZBEj08jm\nzQD9mCoo6jzbXOUR5ApkI9u8H1JeN2p1ULQ5lziKFsicFYCSetLPWt61wDjSosuC\nUw3oyYGwcQKBgQCWsoZLEQLQ3SvdP+qE+dN1+MDXP9FZHIj/N9O0dd/AUPeTv9sM\nrZhN0H5GWQ6Sx94ShqU5kOcJFXJIgtws7YjGejVtnHrWgZtp8hxmui4dKQlF3ovO\nbFXF7YUKhMTwQy2ApbefbTZSFe4GMYv46rhiu+74Pq11vSRKtnbngxs3fQKBgGT/\nWUXmDeytX57Srxx9amN8Mw8sVx0xcMxv7+Wpnzm6FFE3z1c1MKh8hmJdANIuiwS6\neZ/MaGRcMwov8lPaMYXEPJIIPZE0bgb+z7/5gOGFgm5mkBUDSHkUJizVjJH8FBma\ny9VmXhS6XFIOxVgpQcVbP5KLySEnn9Y5SGJTuwhRAoGAa7VXFakyUppeOkDaBa1S\n3JTx6PiXSYBGQQ78ZgmoAn9OJdhKpJimDEbY6zUJlFicYPS8XfnYHQ0VFtnEbhrF\n+h0MFs6hp2OoBte9C/lNL8MFHU9S5EZ7p008Jeb25DyU2BNJ/KiYIzlyXZ1FG6/m\npzWHnJmA2pLEI/bIzveezmM=\n-----END PRIVATE KEY-----\n",
#         "client_email": "pnp-sm-kafka-connect@pnp-staging-dcfd.iam.gserviceaccount.com",
#         "client_id": "101071840494534977300",
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#         "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#         "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pnp-sm-kafka-connect%40pnp-staging-dcfd.iam.gserviceaccount.com"
# }
# props={
#     'CONNECTION_connector__class':'com.google.pubsub.kafka.sink.CloudPubSubSinkConnector' ,
#     'CONNECTION_name':'sink-pnp-public-output-deposit-rules-v2-pusub' ,
#     'CONNECTION_tasks__max':'1',
#     'CONNECTION_topics':'pnp.public.output.deposit-rules.v2' ,
#     'CONNECTION_cps__topic':'pnp.public.output.deposit-rules.v2' ,
#     'CONNECTION_cps__project':'pnp-staging-dcfd'
#     }
# def set_environ_items():
#     for k, v in props.items():
#         os.environ[k] = v
#     os.environ['CONNECTION_gcp__credentials__json'] = json.dumps(credential)

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
