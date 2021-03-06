import os
import logging, sys
from flask import Flask, redirect, url_for, request, render_template, abort
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.simuldb
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

@app.route('/')
def simul():

    _items = db.simuldb.find({"info2":None})
    items = [item for item in _items]

    _compitems = db.simuldb.find({"info2":{"$ne":None}})
    compitems = [item for item in _compitems]

    return render_template('simul.html', items=items, compitems=compitems)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'key': request.form['key'],
        'info1': request.form['info1']
    }
    db.simuldb.insert_one(item_doc)

    return redirect(url_for('simul'))

@app.route('/update', methods=['PATCH','POST'])
def update():
    #Note: POST method is only for HTML forms workaround
    if request.method=='POST' and request.form['_method']!='PATCH':
        abort(400);
    if request.method=='PATCH':
        criteria = request.args.get('key')
        info_payload = request.args.get('info')
    if request.method=='POST':
        criteria = request.form['key']
        info_payload = request.form['info']
    item_doc = {
        'key' : criteria,
        'info2' : info_payload
    }
    db.simuldb.update_one(
    {'key': criteria},
     {'$set': item_doc
     })
    logging.debug("Updated Key: " + str(criteria) + " with info: " + str(info_payload))
    return redirect(url_for('simul'))

@app.route('/get_id', methods=['GET'])
def get_id():
    get_id_for_this_key = request.args.get('key')
    items=db.simuldb.find({"key":get_id_for_this_key})

    return render_template('simul.html',items=items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
