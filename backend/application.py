from os import environ
from flask import Flask, jsonify, request, json
# from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

application = Flask(__name__)
db = SQLAlchemy()

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
application.config['SQLALCHEMY_ECHO'] = False
application.config['WTF_CSRF_ENABLED'] = True
application.config['SECRET_KEY'] = 'CTaUlI2kbIe9GFA9jI2Hz9krZRZzF0wEW0Tw7kqf'
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mikelam:12345678@awssample1.cji0zdy5khnh.us-west-2.rds.amazonaws.com:3306/PortSlate'

db.init_app(application)

# mysql = MySQL(application)
bcrypt = Bcrypt(application)
jwt = JWTManager(application)

CORS(application)

@application.route('/users/register', methods=['POST'])
def register():

    # cur = mysql.connection.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
	
    cur = db.engine.execute("INSERT INTO users (first_name, last_name, email, password, created) VALUES ('" + 
		str(first_name) + "', '" + 
		str(last_name) + "', '" + 
		str(email) + "', '" + 
		str(password) + "', '" + 
		str(created) + "')")
    # mysql.connection.commit()
	
    result = {
		'first_name' : first_name,
		'last_name' : last_name,
		'email' : email,
		'password' : password,
		'created' : created
	}

    return jsonify({'result' : result})
	

@application.route('/users/login', methods=['POST'])
def login():
    # cur = mysql.connection.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""
	
    cur = db.engine.execute("SELECT * FROM users where email = '" + str(email) + "'")
    rv = cur.fetchone()
	
    if bcrypt.check_password_hash(rv['password'], password):
        access_token = create_access_token(identity = {'first_name': rv['first_name'],'last_name': rv['last_name'],'email': rv['email']})
        result = access_token
    else:
        result = jsonify({"error":"Invalid username and password"})
    
    return result

@application.route('/')
def home():
    return "hello world!"

if __name__ == '__main__':
    application.run(debug=True)