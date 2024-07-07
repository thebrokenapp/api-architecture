from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments')
def getPayments():
	return {"payments": payments}

@app.route('/payments', methods=["POST"])
def initiatePayment():
	data = request.get_json()				# extract the request body and store it in variable "data"
	transaction_id = str(uuid.uuid4())		# create a new transaction ID using uuid() library
	timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["transaction_id"] = transaction_id	# Attach transaction ID in the requestbody
	data["timestamp"] = timestamp 			# Attach timestamp in the request body
	payments.append(data)					# Add the request body in our "payments" database
 
	return dataclasses						# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
