from flask import Flask, jsonify, request
import mysql.connector
import json
import os

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

#Get avaibility of the charging point
@app.route('/avaibility')
def get_avaibility():
    #check if at least one locker is available
    return 0

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

    return json.dumps({'free_locker': free_locker[0]})

#Update locker state
@app.route('/locker/<id>', methods=['PUT'])
def update_locker():
    new_state = request.args.get("new_state", type=int)
    locker = Locker.query.get(id)
    return json.dumps({'test_table': test_table()})


if __name__ == '__main__':
    app.run(host='0.0.0.0')