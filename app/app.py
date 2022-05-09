from flask import Flask, jsonify, request
import mysql.connector
import json
import os
from datetime import datetime

app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'charging_point'
    }
def test_table():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'charging_point'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM locker')
    rows = cursor.fetchall()
    resp = rows
    cursor.close()
    connection.close()

    return resp


@app.route('/')
def index() -> str:
    return json.dumps({'test_table': test_table()})

#Get avaibility of the charging point, number of free locker
@app.route('/avaibility')
def get_avaibility():
    #check if at least one locker is available
    query = ("SELECT COUNT(*) FROM locker "
         "WHERE locker_state = 0")

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)

    nb_free_locker = cursor.fetchone()

    return json.dumps({'nb_free_locker': nb_free_locker[0]})

#Get free locker according the connector
@app.route('/locker')
def get_locker():
    conn = request.args.get("connector", type=str)

    query = ("SELECT id_locker FROM locker "
         "WHERE locker_state = 0 AND connector = %s LIMIT 1")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query, (conn,))

    free_locker = cursor.fetchone()

    if free_locker is not None:
        return json.dumps({'free_locker': free_locker[0]})
    else:
        return json.dumps({'free_locker': 'null'})

#Update locker state and add UID and timestamp
@app.route('/locker', methods=['PUT'])
def update_locker():
    new_state = request.args.get("new_state", type=int)
    id_locker = request.args.get("id_locker", type=str)
    user_uid =  request.args.get("user_uid", type=str)

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    if(new_state==1 and user_uid is not None):
        ts = datetime.now()
        query = ("UPDATE locker SET locker_state = %s, user_uid = %s, deposit_time = %s WHERE id_locker = %s")
        cursor.execute(query, (new_state, user_uid, ts, id_locker))
    elif(new_state==0):
        query = ("UPDATE locker SET locker_state = %s, user_uid = NULL, deposit_time = NULL WHERE id_locker = %s")
        cursor.execute(query, (new_state, id_locker))
        #return deposit_time?

    connection.commit()
    result = cursor.rowcount

    return json.dumps({'result': result})

#Add charge data to charge table
@app.route('/charge', methods=['POST'])
def add_charge():
    charge_data = request.get_json()
    pickup_time = datetime.now()
    charge_data['pickup_time'] = pickup_time
    
    add_charge = ("INSERT INTO charge "
               "(id_locker, user_uid, deposit_time, pickup_time) "
               "VALUES (%(id_locker)s, %(user_uid)s, %(deposit_time)s, %(pickup_time)s)")

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(add_charge, charge_data)

    connection.commit()
    result = cursor.rowcount
    
    return json.dumps({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0')