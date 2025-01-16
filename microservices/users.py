from flask import Flask, request, jsonify, Response
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import sqlite3
import redis



app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn

@app.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()				# extract the request body and store it in variable "data"
	user_name = data.get("user_name")		# extract user name from request body
	password = data.get("password")			# extract password from request body
	registration_date = datetime.utcnow()
	product = data.get("product")
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO users (user_name, password, registration_date, product) VALUES (?, ?, ?,?)''',
	(user_name, password, registration_date, product))
	conn.commit()
	conn.close()
	return {"message": "User created"},201


@app.route('/users', methods=['GET'])
def get_all_users():
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''SELECT * FROM users''')
	users = cursor.fetchall()
	users_list = []
	for row in users:
		users_list.append( {"user_name": row[0], "password": row[1], "date": row[2], "product": row[3]})
	conn.close()
	return jsonify({"users": users_list}),200


@app.route('/users/<user_name>', methods=['GET'])
def get_one_user(user_name):
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''SELECT * FROM users where user_name = ?''',(user_name,))
	user = cursor.fetchone()

	if user is None:
		conn.close()
		return {"message": "User not found"}, 404

	user_data = {"user_name": user[0], "password": user[1], "date": user[2], "product": user[3]}
	conn.close()
	return jsonify(user_data), 200



@app.route('/users/<user_name>', methods=['DELETE'])
def delete_one_user(user_name):
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute("""DELETE FROM users WHERE user_name = ?""", (user_name,))
	conn.commit()

	if cursor.rowcount == 0:  # Check if no rows were deleted
		conn.close()
		return {"message": "User not found"}, 404

	conn.close()
	return {}, 204



if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8002, debug=True)
