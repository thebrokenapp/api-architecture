from flask import Flask, request, jsonify, Response
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import sqlite3
import redis

users = dict()





app = Flask(__name__)


@app.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()				# extract the request body and store it in variable "data"
	user_name = data.get("user_name")		# extract user name from request body
	password = data.get("password")			# extract password from request body
	
	if user_name in users:					# check is username already exists in users DB
		return {"message": "user already exists"}, 409
	
	users[user_name] = password
	return data, 201


@app.route('/users', methods=['GET'])
def get_all_users():
	return users


@app.route('/users/<user_name>', methods=['GET'])
def get_one_user(user_name):
	if user_name in users:
		return {"user_name": user_name, "password": users.get(user_name)}
	else:
		return {"message": "User not found"}, 404


@app.route('/users/<user_name>', methods=['DELETE'])
def delete_one_user(user_name):
	if user_name in users:
		users.pop(user_name)
		return '',204
	else:
		return {"message": "User not found"}, 404



if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 9000, debug=True)
