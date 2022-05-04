from flask import Flask, jsonify, request
import mysql.connector
import json
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')