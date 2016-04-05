import os.path
from flask import Flask, render_template
import sqlite3
import json

APP_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(APP_DIR, "election.db")

app = Flask(__name__)

def getConstituencies(state):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute("select name from data where type = 'ST' and keyy='{0}'".format(state))
    stateIn = cursor.fetchone()[0]
    getAcsQuery = "select name from data where type = 'AC' and parent = '{0}'".format(state)
    cursor.execute(getAcsQuery)
    listAssembly = []
    for row in cursor:
        listAssembly.append(row[0])
    dictAssembly = {"listAssembly":listAssembly, "stateIn":stateIn}
    return dictAssembly

def getBooths(state, constituency):
    db = sqlite3.connect(db_path)
    cursur = db.cursor()
    cursur.execute("select name from data where type = 'ST' and keyy='{0}'".format(state))
    stateIn = cursur.fetchone()[0]
    boothParent = state+"/"+constituency
    cursur.execute("select name from data where type = 'AC' and keyy='{0}'".format(boothParent))
    constituencyIn = cursur.fetchone()[0]
    getBoothsQuery = "select name from data where type = 'PB' and parent = '{0}'".format(boothParent)
    cursur.execute(getBoothsQuery)
    listBooths = []
    for row in cursur:
        listBooths.append(row[0])
    dictBooths = {"listBooths":listBooths, "stateIn":stateIn, "constituencyIn":constituencyIn}
    return dictBooths

@app.route('/')
def states():
    db = sqlite3.connect(db_path)
    getStatesQuery = "select DISTINCT name from data where type='ST'"
    cursr = db.cursor()
    cursr.execute(getStatesQuery)
    listStates = []
    for row in cursr:
        listStates.append(row[0])
    return render_template('states.html', states=listStates)

@app.route('/<state>')
def constituencies(state):
    dictAssembly = getConstituencies(state)
    return render_template('constituencies.html', constituencies = dictAssembly['listAssembly'], State = dictAssembly['stateIn'])

@app.route('/<state>.json')
def constituenciesJson(state):
    dictAssembly = getConstituencies(state)
    return json.dumps(dictAssembly['listAssembly'])

@app.route('/<state>/<constituency>')
def booths(state, constituency):
    dictBooths = getBooths(state, constituency)
    return render_template('booths.html', booths = dictBooths['listBooths'], State = dictBooths['stateIn'], Constituency = dictBooths['constituencyIn'])

@app.route('/<state>/<constituency>.json')
def boothsJson(state, constituency):
    dictBooths = getBooths(state, constituency)
    return json.dumps(dictBooths['listBooths'])

if __name__ == '__main__':
    app.run(debug=True)
