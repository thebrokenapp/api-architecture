from flask import Flask, request
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import sqlite3
import redis
import json

app = Flask(__name__)
payments = []
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn


class PaymentBody(BaseModel):
	amount : int
	payer_upi : str = Field(min_length=8, max_length=20)
	payee_upi: str = Field(min_length=8, max_length=20)
	note: str
	class Config:
		extra = "forbid"



@app.route('/payments/apiStatus', methods=["GET"])
def api_status():
	return {"message": "API is running successfulyy"}



@app.route('/payments', methods=["POST"])
@validate()
def initiatePayment(body: PaymentBody):
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
	cursor.execute('''INSERT INTO payments (transaction_id, amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?, ?,?, ?, ?)''',
	(transaction_id,amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
	redis_client.publish("initiate_payment_channel", json.dumps({"amount": amount, "payer_upi": payer_upi, "payee_upi": payee_upi, "note": note, "transaction_id": transaction_id, "timestamp": str(timestamp), "status": status}))
	return {"message": "transaction created", "transaction_id": transaction_id}


@app.route('/payments/<transaction_id>', methods=["GET"])
@validate()
def getPayment(transaction_id: UUID4):
	redis_key = str(transaction_id)
	cache_data = redis_client.hgetall(redis_key)

	if cache_data:
		print("Data coming from cache")
		return cache_data
	else:
		print("Data coming from sqlite3")
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
		payment = cursor.fetchone()
		conn.close()
		if payment is None:
			return {"message": "Transaction not found"}, 404

	redis_key = str(transaction_id)
	redis_client.hset(redis_key, mapping=dict(payment))
	return dict(payment)

@app.route('/payments', methods=["GET"])
def getAllPayments():
	page = int(request.args.get('page', 1))
	size = int(request.args.get('size', 5))
	if size > 10:
		size = 10
	offset = (page - 1) * size
	redis_key = "page_"+ str(page)
	cache = redis_client.get(redis_key)
	if cache:
		print("Data from cache")
		next_page_data = json.loads(cache)
		redis_client.publish("fetch_payment_channel", json.dumps({"page": page, "size": size})) 
		return {"payments": next_page_data, "page": page, "from": "redis"}
	else:
		print("Data from sqlite")
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments LIMIT ? OFFSET ?', (size, offset))
		payments = cursor.fetchall()
		conn.close()
		output_list = []
		for payment in payments:
			output_list.append(dict(payment))

	redis_client.publish("fetch_payment_channel", json.dumps({"page": page, "size": size})) 
	return {"payments": output_list, "page": page}



@app.route('/payments/<transaction_id>', methods=["PATCH"])
def update_one_transaction(transaction_id):
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
		return {"message": "Transaction not found"},404

	redis_client.delete(transaction_id)
	return {"message": "Transaction updated"}


@app.route('/payments/<transaction_id>', methods=["DELETE"])
def delete_one_payment(transaction_id):
	conn = get_db_connection()
	cursor = conn.cursor()

	cursor.execute('''DELETE FROM payments WHERE transaction_id = ?''', (transaction_id,))

	if cursor.rowcount == 0:
		conn.close()
		return {"message": "Transaction not found"},404

	conn.commit()
	conn.close()

	return {"message": "Transaction deleted!"},204






# Custom error handler for 405
@app.errorhandler(405)
def method_not_allowed_error(error):
	return {"error": "Method Not Allowed!"},405



if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 8000, debug=True)
