import requests
from flask import Flask,request
import json
import mysql.connector
import secrets
import time

host = "localhost"
user = "root"
password = "root"
database = "bac"
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
def check_user(user):
    cursor = connection.cursor()
    find_user="""
        SELECT * FROM users WHERE username = %s
    """
    data=(user,)
    cursor.execute(find_user,data)
    isindp=cursor.fetchone()
    if isindp:
        cursor.fetchall()
        cursor.close()
        return True
    else:
        cursor.fetchall()
        cursor.close()
        return False

def generate_random_cookie():
    random_string = secrets.token_urlsafe(50)
    return random_string

def add_user(user,passw,userid):
    if check_user(user):
        return '{"status":401,"message":"had w9 déja kayn f database"}'
    cursor=connection.cursor()
    insert_user = """
    INSERT INTO users (username, password, userid) VALUES (%s, %s,%s)
    """
    data_user = (user, passw,userid)
    cursor.execute(insert_user, data_user)
    connection.commit()
    cookie=generate_random_cookie()
    now=time.time()+1296000
    insert_cookie="""
    INSERT INTO cookies (cookies,userid,valid) VALUES (%s,%s,%s)
    """
    data_cookie = (cookie,userid,now)
    cursor.execute(insert_cookie,data_cookie)
    connection.commit()
    cursor.close()
    return '{"status":200,"message":"user added successfully","cookie":"'+cookie+'"}'

import hashlib
def hash(username):
    md5_hash = hashlib.md5()
    md5_hash.update(username.encode('utf-8'))
    return md5_hash.hexdigest()

app=Flask(__name__)

@app.route("/register",methods=["POST"])
def register():
    data=request.data.decode()
    data=json.loads(data)
    print(data)
    user=data["user"]
    passw=data["pass"]
    print(user,passw)
    userid=hash(user)
    return add_user(user,passw,userid)
    

@app.route("/getuserdata")
def get_user_data():
    return "NOT YET"

@app.route("/getexam")
def get_exam():
    return "NOT YET"

@app.route("/")
def home():
    return "Welcome to BAC-ARCHIVE BACKEND"

app.run(port=5050)
