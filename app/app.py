from flask import Flask, jsonify, request
import mysql.connector
import json
import os
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1000)
jwt = JWTManager(app)

config = {
        'user': 'root',
        'password': os.environ.get("MYSQL_PASSWORD"),
        'host': 'db',
        'port': '3306',
        'database': 'charging_point'
    }
def test_table():
    config = {
        'user': 'root',
        'password': os.environ.get("MYSQL_PASSWORD"),
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

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(hours=500))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route('/token', methods=["POST"])
def create_token():
    user = request.json.get("user", None)
    password = request.json.get("password", None)
    if user != "app" or password != "test":
        return {"msg": "Wrong user or password"}, 401

    access_token = create_access_token(identity=user)
    response = {"access_token":access_token}
    return response

@app.route('/')
# @jwt_required()
def index() -> str:
    return json.dumps({'test_table': test_table()})

#Get avaibility of the charging point, number of free locker
@app.route('/avaibility')
# @jwt_required()
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
# @jwt_required()
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

#Update locker state
@app.route('/locker', methods=['PUT'])
# @jwt_required()
def update_locker():
    new_state = request.args.get("new_state", type=int)
    id_locker = request.args.get("id_locker", type=str)
    user_uid =  request.args.get("user_uid", type=str)

    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    if(new_state==1 and user_uid is not None):
        ts = datetime.now()
        update_to_busy = ("UPDATE locker SET locker_state = %s, user_uid = %s, deposit_time = %s WHERE id_locker = %s")
        cursor.execute(update_to_busy, (new_state, user_uid, ts, id_locker))
    elif(new_state==0):
        #Retrieve deposit_time
        get_deposit_time = ("SELECT deposit_time FROM locker "
         "WHERE id_locker = %s LIMIT 1")
        cursor.execute(get_deposit_time, (id_locker,))
        
        retrieved_deposit_time = cursor.fetchone()

        #Update locker state to free
        update_to_free = ("UPDATE locker SET locker_state = %s, user_uid = NULL, deposit_time = NULL WHERE id_locker = %s")
        cursor.execute(update_to_free, (new_state, id_locker))
    elif(new_state==2):
        #Update locker state to free
        update_to_out_of_service = ("UPDATE locker SET locker_state = %s WHERE id_locker = %s")
        cursor.execute(update_to_out_of_service, (new_state, id_locker))
        
    connection.commit()
    result = cursor.rowcount

    if(new_state==1 and user_uid is not None):
        return json.dumps({'result': result}) 
    elif(new_state==0):
        return json.dumps({'result': result, 'deposit_time': retrieved_deposit_time[0]}, default=str) 
    elif(new_state==2):
        return json.dumps({'result': result}) 


#Add charge data to charge table
@app.route('/charge', methods=['POST'])
# @jwt_required()
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

#Get locker id where the device of the given user if a device is in the charging point
@app.route('/device')
# @jwt_required()
def get_device():
    user_uid =  request.args.get("user_uid", type=str)

    query = ("SELECT id_locker FROM locker "
         "WHERE user_uid = %s LIMIT 1")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query, (user_uid,))

    id_locker = cursor.fetchone()

    if id_locker is not None:
        return json.dumps({'id_locker': id_locker[0]})
    else:
        return json.dumps({'id_locker': 'null'})

#Get list of out-of-service lockers
@app.route('/outofservice')
def get_out_of_service_lockers():

    query = ("SELECT id_locker FROM locker "
         "WHERE locker_state = 2")
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(query)

    response = cursor.fetchall()

    list_id_locker = list()
    for i, item in enumerate(response):
        list_id_locker.append(item[0])
        
    if list_id_locker is not None:
        return json.dumps({'out_of_service_lockers': list_id_locker})
    else:
        return json.dumps({'out_of_service_lockers': 'null'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')