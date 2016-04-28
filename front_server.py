# coding: utf-8

from bottle import Bottle
from bottle import run
from bottle import request
import requests
import json
import os

app = Bottle()

@app.route('/')
def index():
    getter = requests.get('http://10.9.11.6:8000/usage')
    return getter._content


@app.route('/hello/<a>')
def hello(a):
    text = 'hello {0} !'.format(a)
    return text


@app.get('/name')
def get_name():
    with open('{0}/server.json'.format(os.path.dirname(os.path.realpath(__file__))), mode='r') as server:
        data = json.load(server)
    return 'Server name: {0}'.format(data['name'])


@app.post('/name')
def set_name():
    name = request.POST.get('name')
    with open('{0}/server.json'.format(os.path.dirname(os.path.realpath(__file__))), mode='wa') as server:
        json.dump({'name': name}, server)
    return 'Server name set to {0}'.format(name)

run(app, host='0.0.0.0', port=8080)
