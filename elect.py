import os.path
from flask import Flask, render_template
import sqlite3
import json

APP_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(APP_DIR, "election.db")

app = Flask(__name__)

def getSub(root):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("select name from data where type = 'ROOT' and key='{0}'".format(root))
    rootIn = cursor.fetchone()[0]
    getAcsQuery = "select name from data where type = 'SUB' and parent = '{0}'".format(root)
    cursor.execute(getAcsQuery)
    subList = []
    for row in cursor:
        subList.append(row[0])
    dictSub = {"subList":subList, "rootIn":rootIn}
    return dictSub

def getSubSub(root, sub):
    db = sqlite3.connect(db_path)
    cursur = db.cursor()
    cursur.execute("select name from data where type = 'ROOT' and key='{0}'".format(root))
    rootIn = cursur.fetchone()[0]
    subSubParent = root+"/"+sub
    cursur.execute("select name from data where type = 'SUB' and key='{0}'".format(subSubParent))
    subIn = cursur.fetchone()[0]
    getSubSubQuery = "select name from data where type = 'SUBSUB' and parent = '{0}'".format(subSubParent)
    cursur.execute(getSubSubQuery)
    listSubSub = []
    for row in cursur:
        listSubSub.append(row[0])
    dictSubSub = {"listSubSub":listSubSub, "rootIn":rootIn, "subIn":subIn}
    return dictSubSub

@app.route('/')
def home():
    db = sqlite3.connect(db_path)
    getRootQuery = "select DISTINCT name from data where type='ROOT'"
    cursr = db.cursor()
    cursr.execute(getRootQuery)
    listRoot = []
    for row in cursr:
        listRoot.append(row[0])
    return render_template('roots.html', roots=listRoot)

@app.route('/<root>')
def sub(root):
    dictSub = getSub(root)
    return render_template('sub.html', subs = dictSub['subList'], root = dictSub['rootIn'])

@app.route('/<root>.json')
def subJson(root):
    dictSub = getSub(root)
    return json.dumps(dictSub['subList'])

@app.route('/<root>/<sub>')
def subSub(root, sub):
    dictSubSub = getSubSub(root, sub)
    return render_template('subSub.html', subSubs = dictSubSub['listSubSub'], root = dictSubSub['rootIn'], sub = dictSubSub['subIn'])

@app.route('/<root>/<sub>.json')
def subSubJson(root, sub):
    dictSubSub = getSubSub(root, sub)
    return json.dumps(dictSubSub['listSubSub'])

if __name__ == '__main__':
    app.run(debug=True)
