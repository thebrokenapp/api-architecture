from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import sqlite3
import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
payments_db = []


# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn



class PaymentBody(BaseModel):
	user_name: str
	amount : int = Field(gt=0, lt=100000)
	payer_upi : str = Field(min_length=8, max_length=20)
	payee_upi: str = Field(min_length=8, max_length=20)
	note: str = ''
	class Config:
		extra = "forbid"


class UpdatePaymentBody(BaseModel):
	status: str
	class Config:
		extra = "forbid"

class UserNameModel(BaseModel):
    user_name: str = Field(..., min_length=10, max_length=20)

@app.route('/apiStatus', methods=["GET"])
def api_status():
	return {"message": "Payments API is up!"}


@app.route('/payments', methods=["POST"])
@validate()
def initiate_payment(body:PaymentBody):
	data = request.get_json()
	user_name = data.get("user_name")
	amount = data.get("amount")
	payer_upi = data.get("payer_upi")
	payee_upi = data.get("payee_upi")
	note = data.get("note")				
	transaction_id = str(uuid.uuid4())		
	timestamp = datetime.utcnow()			
	status = "initiated"
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO payments (transaction_id, user_name,amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?, ?,?, ?, ?,?)''',
	(transaction_id, user_name,amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
 
	return {"message": "transaction created", "transaction_id": transaction_id}

@app.route('/payments/<transaction_id>', methods=["PATCH"])
@validate()
def update_payment(body: UpdatePaymentBody,transaction_id: UUID4):
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



@app.route('/payments/<txn_id>', methods=["DELETE"])
def delete_payment(txn_id):
	conn = get_db_connection()
	cursor = conn.cursor()

	cursor.execute('''DELETE FROM payments WHERE transaction_id = ?''', (transaction_id,))

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	conn.commit()
	conn.close()

	return jsonify(	)




@app.route('/payments/<user_name>', methods=["GET"])
def get_payments_for_one_user(user_name: str):
	status = request.args.get('status','NA')
	payment_list = []
	for txn in payments_db:
		if user_name == txn["user_name"]:
			if txn["status"] == status:
				payment_list.append(txn)

	return {"payments": payment_list}



@app.route('/payments/transaction/<transaction_id>', methods=["GET"])
@validate()
def get_payment_by_txn_id(transaction_id : UUID4):
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


















# Custom error handler for 405
@app.errorhandler(405)
def method_not_allowed_error(error):
	return {"error": "Method Not Allowed!"},405


# Custom error handler for 405
@app.errorhandler(404)
def resource_not_found_error(error):
	return {"error": "Resource Not found!"},404

if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8001, debug=True)
