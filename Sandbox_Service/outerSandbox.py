#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import json
import thread
import sqlite3
import datetime
import werkzeug
import requests
from flask import Flask, request
from flask_restful import reqparse
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

port=       [5001, 5002, 5003]
parser=     reqparse.RequestParser()
url=        'http://127.0.0.1:{port}/webshell'
lastUrl=    'http://127.0.0.1:{port}/webshell/last'

class webshell(Resource):
    def post(self):
        dtUpStr=str(time.time())
        print dtUpStd

        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args=parser.parse_args()
        upWebshell=args['file']

        lastStatus=requests.get(lastUrl)
        
        print "content {0}, type: {1}".format(lastStatus.text, type(lastStatus.text))

        # files={'file': upWebshell}
        # r=requests.post(url, files=files)
        # print r.text



api.add_resource(webshell, '/webshell')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

