#!/usr/bin/env python
#-*- coding: utf-8 -*-

#! TODO 倘若该hash在数据库中不能找到对应记录, 则返回一个提示信息, 而不是返回一个错误
#! TODO 从webshell.log文件中读取key时, 去掉key中的所有空格


import json
import time
import thread
import sqlite3
import hashlib
import commands
import werkzeug
from flask import Flask, request
from flask_restful import reqparse
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

parser=reqparse.RequestParser()
phpStr="php -f {fPath}"
sqlDB='webshell.db'
queryKeys=['hash', 'status', 'uploadDate', 'processDate', 'finishData', 'message']

def getJsonFromLog(logs):
    listLogs=dict()
    for i in range(6):
        keySta=logs[i].find('[')
        keyEnd=logs[i].find(']')
        valSta=logs[i].find(']')
        print "The key of dict is {0}".format(logs[i][keySta+1:keyEnd])
        print "The value of dict is {0}".format(logs[i][valSta+3:-1])
        listLogs.setdefault(logs[i][keySta+1:keyEnd], logs[i][valSta+3:-1])

    return json.dumps(listLogs)

def phpExecute(filePath, hexHash, dtUpStr):

    tConn=sqlite3.connect(sqlDB)
    tc=tConn.cursor()

    if(not InsertWithoutDup(hexHash, dtUpStr, tConn, tc)):
        print "----Already in the stock----\n"
        return

    cmd=phpStr.format(fPath=filePath)
    sta, stdout=commands.getstatusoutput(cmd)
    print "----STD OUTPUT is----\n{0}".format(stdout)
    
    logs=open('/tmp/webshell.log').readlines()[-7:-1]
    logStr=getJsonFromLog(logs)
    print "----STD LOG is----\n{0}".format(logStr)

    tc.execute("UPDATE webshells SET status=1, message=?, stdout=? WHERE hash=?", (logStr, stdout, hexHash))

    tConn.commit()
    tConn.close()

def InsertWithoutDup(hexHash, dtStr, conn, c):

    c.execute("SELECT * FROM webshells where hash=?", (hexHash, ))
    if(c.fetchone()):
        return 0

    c.execute("INSERT INTO webshells (hash, status, uploadDate) VALUES (?, ?, ?)", (hexHash, 0, dtStr))
    conn.commit()
    return 1

def convQueIntoRes(c):

    resultVal=c.fetchone()
    resultList=list(resultVal)

    resultDict=dict(zip(queryKeys, resultVal))
    return json.dumps(resultDict)

class webshell(Resource):
    def post(self):

        #dtUpStr=datetime.datetime.now().strftime("%b, %d, %Y %H:%M:%S:%f")
        dt=time.time()
        print dt
        dtUpStr=str(dt)
        print dtUpStr

        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files')
        args=parser.parse_args()
        upWebshell=args['file']
        
        fileContent=upWebshell.read()
        fileHash=hashlib.md5(fileContent.encode())
        hexHash=fileHash.hexdigest()

        upWebshell.seek(0)
        filePath='/tmp/{fileName}'.format(fileName=hexHash)
        upWebshell.save(filePath)
        upWebshell.close()
        
        thread.start_new_thread(phpExecute, (filePath, hexHash, dtUpStr))
        return hexHash

class getWebshell(Resource):
    def get(self, webshell_hash):
        conn=sqlite3.connect(sqlDB)
        c=conn.cursor()

        print webshell_hash
        c.execute("SELECT hash, status, uploadDate, processDate, finishDate, message FROM webshells WHERE hash=?", (webshell_hash, ))

        return convQueIntoRes(c)

"""
" 
" @brief return the record of last request
"
"""
class lastWebshell(Resource):
    def get(self):
        conn=sqlite3.connect(sqlDB)
        c=conn.cursor()

        c.execute("SELECT hash, status, uploadDate, processDate, finishDate, message FROM webshells ORDER BY ID DESC")
        return convQueIntoRes(c)

class delWebshell(Resource):
    def get(self, webshell_hash):
        conn=sqlite3.connect(sqlDB)
        c=conn.cursor()

        c.execute("DELETE FROM webshells where hash=?", (webshell_hash, ))

        conn.commit()
        return "Deleted"
        
class webshells(Resource):
    def get(self):
        conn=sqlite3.connect(sqlDB)
        c=conn.cursor()

        rows=c.execute("SELECT * FROM webshells ").fetchall()
        return rows

api.add_resource(webshell,          '/webshell')
api.add_resource(lastWebshell,      '/webshell/last')
api.add_resource(delWebshell,       '/webshell/delete/<string:webshell_hash>')     #! Only for Debug
api.add_resource(getWebshell,       '/webshell/<string:webshell_hash>',    endpoint='webshell_ep')
api.add_resource(webshells,         '/webshells')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
