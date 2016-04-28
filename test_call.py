# coding: utf-8

import requests
from requests.auth import HTTPBasicAuth

# Auth server
login = 'Xxxxxxx'
mdp = 'xxxxxxx'

set_user = requests.post(url='http://127.0.0.1:5000/api/users', json={'username': login, 'password': mdp})
user = set_user.json()['username']

get_token = requests.get(url='http://127.0.0.1:5000/api/token', auth=HTTPBasicAuth(login, mdp))
token = get_token.json()['token']

get_resource = requests.get(url='http://127.0.0.1:5000/api/resource', auth=HTTPBasicAuth(token, ''))
resource = get_resource.json()['data']

print '\n\tUser: {0} \n\tToken: {1}\n\tMessage: {2}\n'.format(user, token, resource)
