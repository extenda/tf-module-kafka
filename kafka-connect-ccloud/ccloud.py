#!/usr/bin/env python3

import sys
import os
import json
import subprocess
import tarfile


import_existing_connection = False


def download_confluent():
    if not os.path.exists('confluent/confluent'):
        url = 'https://s3-us-west-2.amazonaws.com/confluent.cloud/confluent-cli/archives/latest/confluent_latest_%s_amd64.tar.gz' % sys.platform
        os.system('curl -o confluent.tar.gz %s' % url)
        os.system('tar -xzf confluent.tar.gz confluent/confluent')
        os.remove('confluent.tar.gz')


def create_connection_config():
    config = {}
    for k, v in os.environ.items():
        if k[:11] == 'CONNECTION_':
            config[k[11:].replace('__', '.')] = v
    open('connection.config', 'w').write(json.dumps(config, indent=2))


def delete_connection_config():
    os.remove('connection.config')


def confluent_login(login, password):
    testcmd = subprocess.run('./confluent/confluent connect list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', timeout=60)
    if 'Error: you must log in to Confluent Cloud' in testcmd.stderr:
        logincmd = subprocess.Popen('timeout 60 ./confluent/confluent login --prompt --no-browser', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0, encoding='utf-8')
        logincmd.communicate('%s\n%s\n' % (login, password))
        if logincmd.returncode != 0:
            sys.exit(logincmd.returncode)


def get_real_connection_config(environment, cluster, id):
    cmd = subprocess.run('./confluent/confluent connect describe --environment %s --cluster %s %s -o json' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, encoding='utf-8', timeout=60)
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)
    config = {}
    config['id'] = id
    data = json.loads(cmd.stdout)
    for i in data['configs']:
        config[ i['config'] ] = i['value']
    return config


def get_existing_connection_id(environment, cluster, name):
    cmd = subprocess.run('./confluent/confluent connect list --environment %s --cluster %s -o json' % (environment, cluster), shell=True, stdout=subprocess.PIPE, encoding='utf-8', timeout=60)
    connectors = json.loads(cmd.stdout)
    for connector in connectors:
        if connector['name'] == name:
            return connector['id']

# ------------ terraform commands ------------

def create():
    confluent_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']

    id = get_existing_connection_id(environment, cluster, os.environ['CONNECTION_name']) if import_existing_connection else None
    if not id:
        create_connection_config()
        cmd = subprocess.run('./confluent/confluent connect create --environment %s --cluster %s --config connection.config' % (environment, cluster), shell=True, stdout=subprocess.PIPE, encoding='utf-8', timeout=300)
        delete_connection_config()
        if cmd.returncode != 0:
            sys.exit(cmd.returncode)
        id = cmd.stdout.split(' ')[-1].strip()

    output = get_real_connection_config(environment, cluster, id)
    print(json.dumps(output))


def delete():
    confluent_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    cmd = subprocess.run('./confluent/confluent connect delete --environment %s --cluster %s %s' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, encoding='utf-8', timeout=300)
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)


def read():
    confluent_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    output = get_real_connection_config(environment, cluster, id)
    print(json.dumps(output))


def update():
    confluent_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    create_connection_config()
    cmd = subprocess.run('./confluent/confluent connect update --environment %s --cluster %s --config connection.config %s' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, encoding='utf-8', timeout=300)
    delete_connection_config()
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)

    output = get_real_connection_config(environment, cluster, id)
    print(json.dumps(output))


if __name__=='__main__':
    download_confluent()
    if len(sys.argv) > 1:
        if sys.argv[1]=='create':
            create()
        elif sys.argv[1]=='delete':
            delete()
        elif sys.argv[1]=='read':
            read()
        elif sys.argv[1]=='update':
            update()
