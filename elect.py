import os.path
from flask import Flask, render_template
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "election.db")

app = Flask(__name__)

@app.route('/')
def states():
    db = sqlite3.connect(db_path)
    db.text_factory = str
    getStatesQuery = "select DISTINCT name from data where type='ST'"
    cursr = db.cursor()
    cursr.execute(getStatesQuery)
    listStates = []
    for row in cursr:
        listStates.append(row)
    return render_template('states.html', states=listStates)

@app.route('/<state>')
def constituencies(state):
    db = sqlite3.connect(db_path)
    db.text_factory = str
    curs = db.cursor()
    curs.execute("select name from data where type = 'ST' and keyy='{0}'".format(state))
    stateIn = curs.fetchone()
    getAcsQuery = "select name from data where type = 'AC' and parent = '{0}'".format(state)
    curs.execute(getAcsQuery)
    listAssembly = []
    for row in curs:
        listAssembly.append(row)
    return render_template('constituencies.html', constituencies = listAssembly, State = stateIn)

@app.route('/<state>/<constituency>')
def booths(state, constituency):
    db = sqlite3.connect(db_path)
    db.text_factory = str
    cursur = db.cursor()
    cursur.execute("select name from data where type = 'ST' and keyy='{0}'".format(state))
    stateIn = cursur.fetchone()
    boothParent = state+"/"+constituency
    cursur.execute("select name from data where type = 'AC' and keyy='{0}'".format(boothParent))
    constituencyIn = cursur.fetchone()
    getBoothsQuery = "select name from data where type = 'PB' and parent = '{0}'".format(boothParent)
    cursur.execute(getBoothsQuery)
    listBooths = []
    for row in cursur:
        listBooths.append(row)
    return render_template('booths.html', booths = listBooths, State = stateIn, Constituency = constituencyIn)

if __name__ == '__main__':
    app.run(debug=True)