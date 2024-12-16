from flask import Flask, request, jsonify, Response
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import sqlite3
import redis

payments = []
users = dict()

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn


class PaymentRequestBody(BaseModel):
	amount : int = Field(gt=0, lt=1000000)
	payer_upi : str = Field(min_length=3, max_length=30)
	payee_upi: str = Field(min_length=3, max_length=30)
	note: str = ''

	class Config:
		extra = "forbid"


class UpdateBody(BaseModel):
	status : str



app = Flask(__name__)


@app.route('/apiStatus', methods=['GET'])
def api_status():
	return {"message": "API is running!"}


@app.route('/payments', methods = ['GET'])
def fetch_all_payments():
	status = request.args.get('status')
	if status is not None:
		return_list = []
		for txn in payments:
			if txn["status"] == status:
				return_list.append(txn)
		return {"transactions": return_list}

	return {"transactions": payments}


@app.route('/payments', methods = ['POST'])
@validate()
def make_a_payments(body: PaymentRequestBody):
	data = request.get_json()
	amount = data.get("amount")
	payer_upi = data.get("payer_upi")
	payee_upi = data.get("payee_upi")
	note = data.get("note")				
	transaction_id = str(uuid.uuid4())		
	timestamp = datetime.utcnow()			
	status = "initiated"
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO payments (transaction_id, amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?,?, ?, ?,?)''',
	(transaction_id, amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
 
	return {"message": "transaction created", "transaction_id": transaction_id}


@app.route('/payments/<transaction_id>', methods = ['GET'])
@validate()
def getPayment(transaction_id: UUID4):
	redis_key = str(transaction_id)
	cache_data = r.hgetall(redis_key)
	if cache_data:
		print("data came from redis")
		return jsonify(cache_data)
	else:
		print("data came from sqlite3")
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
		payment = cursor.fetchone()
		conn.close()
		if payment is None:
			return {"message": "Transaction not found"}, 404

		r.hset(redis_key, mapping = dict(payment))

	return dict(payment)




@app.route('/payments/<transaction_id>', methods = ['PATCH'])
@validate()
def updatePayment(transaction_id: UUID4, body: UpdateBody):
	data = request.get_json()
	status = data.get("status")
	transaction_id = str(transaction_id)
	timestamp = datetime.utcnow()							
	
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('''UPDATE payments SET status = ?, timestamp = ? WHERE transaction_id = ? ''', (status, timestamp, transaction_id))
	conn.commit()
	conn.close()

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	r.delete(transaction_id)
	return jsonify({"message": "Transaction updated"})



@app.route('/payments/<transaction_id>', methods = ['DELETE'])
def deletePayment(transaction_id):
	conn = get_db_connection()
	cursor = conn.cursor()

	cursor.execute('''DELETE FROM payments WHERE transaction_id = ?''', (transaction_id,))

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	conn.commit()
	conn.close()

	return jsonify({"message": "Transaction deleted!"})




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
	app.run(host="0.0.0.0", port= 8001, debug=True)
