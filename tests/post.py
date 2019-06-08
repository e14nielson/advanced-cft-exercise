import json
import requests
import boto3
import uuid
import time

profile_name = 'mine'
region = 'us-west-2'
session = boto3.Session(profile_name=profile_name)
api = session.client('apigateway', region_name=region)
cf = session.client('cloudformation', region_name=region)


def get_key(name_of_key):
    print('Discovering API Key')
    response = api.get_api_keys(includeValues=True)
    items = response['items']
    for item in items:
        if name_of_key in item['name']:
            return item['value']


def get_url(name_of_stack):
    print('Discovering Cloudformation Exports')
    exports = cf.list_exports()['Exports']
    for export in exports:
        if export['Name'] == 'url-{}'.format(name_of_stack):
            return export['Value']


def post(url, key, data):
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json', 'x-api-key': key}
    return requests.post(url, data=data_json, headers=headers)


if __name__ == "__main__":
    name = 'advanced'
    full_url = get_url(name)
    api_key = get_key(name)
    while True:
        body = {
            "input": [
                str(uuid.uuid4()),
                str(uuid.uuid4())
            ]
        }
        print(post(full_url, api_key, body))
        time.sleep(1)
