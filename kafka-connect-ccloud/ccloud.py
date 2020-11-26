#!/usr/bin/env python3

import sys
import os
import json
import subprocess
import tarfile


def download_ccloud():
    if not os.path.exists('ccloud/ccloud'):
        url = 'https://s3-us-west-2.amazonaws.com/confluent.cloud/ccloud-cli/archives/latest/ccloud_latest_linux_amd64.tar.gz'
        os.system('curl -o ccloud_latest_linux_amd64.tar.gz %s' % url)
        os.system('tar -xzf ccloud_latest_linux_amd64.tar.gz ccloud/ccloud')
        os.remove('ccloud_latest_linux_amd64.tar.gz')


def create_connection_config():
    config = {}
    for k, v in os.environ.items():
        if k[:11] == 'CONNECTION_':
            config[k[11:]] = v
    open('connection.config', 'w').write(json.dumps(config, indent=2))


def delete_connection_config():
    os.remove('connection.config')


def ccloud_login(login, password):
    testcmd = subprocess.run('./ccloud/ccloud connector list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if 'Error: not logged in' in testcmd.stderr:
        logincmd = subprocess.Popen('./ccloud/ccloud login', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=0, text=True)
        output = ''
        while 'Email: ' not in output: output+=logincmd.stdout.read(1)
        logincmd.stdin.write('%s\n' % login)
        while 'Password: ' not in output: output+=logincmd.stdout.read(1)
        logincmd.stdin.write('%s\n' % password)
        logincmd.communicate()
        if logincmd.returncode != 0:
            sys.exit(logincmd.returncode)


def get_real_connection_config(environment, cluster, id):
    cmd = subprocess.run('./ccloud/ccloud connector describe --environment %s --cluster %s %s -o json' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, text=True)
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)
    config = {}
    config['id'] = id
    data = json.loads(cmd.stdout)
    for i in data['configs']:
        config[ i['config'] ] = i['value']
    return config

# ------------ terraform commands ------------

def create():
    ccloud_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    create_connection_config()
    cmd = subprocess.run('./ccloud/ccloud connector create --environment %s --cluster %s --config connection.config' % (environment, cluster), shell=True, stdout=subprocess.PIPE, text=True)
    delete_connection_config()
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)
    id = cmd.stdout.split(' ')[-1].strip()

    output = get_real_connection_config(environment, cluster, id = id)
    print(json.dumps(output))


def delete():
    ccloud_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    cmd = subprocess.run('./ccloud/ccloud connector delete --environment %s --cluster %s %s' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, text=True)
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)


def read():
    ccloud_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    output = get_real_connection_config(environment, cluster, id = id)
    print(json.dumps(output))


def update():
    ccloud_login(os.environ['CONFLUENT_USERNAME'], os.environ['CONFLUENT_PASSWORD'])

    previous_output = json.loads(sys.stdin.read())
    environment = os.environ['CONFLUENT_ENVIRONMENT']
    cluster = os.environ['CONFLUENT_CLUSTER']
    id = previous_output['id']

    create_connection_config()
    cmd = subprocess.run('./ccloud/ccloud connector update --environment %s --cluster %s --config connection.config %s' % (environment, cluster, id), shell=True, stdout=subprocess.PIPE, text=True)
    delete_connection_config()
    if cmd.returncode != 0:
        sys.exit(cmd.returncode)

    output = get_real_connection_config(environment, cluster, id = id)
    print(json.dumps(output))


if __name__=='__main__':
    download_ccloud()
    if len(sys.argv) > 1:
        if sys.argv[1]=='create':
            create()
        elif sys.argv[1]=='delete':
            delete()
        elif sys.argv[1]=='read':
            read()
        elif sys.argv[1]=='update':
            update()
