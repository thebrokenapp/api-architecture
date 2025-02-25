from flask import Flask, request
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate

app = Flask(__name__)
payments = []

class PaymentBody(BaseModel):
	amount : int
	payer_upi : str = Field(min_length=8, max_length=20)
	payee_upi: str = Field(min_length=8, max_length=20)
	note: str
	class Config:
		extra = "forbid"



@app.route('/apiStatus', methods=["GET"])
def api_status():
	return {"message": "API is running successfulyy"}



@app.route('/payments', methods=["POST"])
@validate()
def initiatePayment(body: PaymentBody):
	data = request.get_json()				# extract the request body and store it in variable "data"
	transaction_id = str(uuid.uuid4())		# create a new transaction ID using uuid() library
	timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["transaction_id"] = transaction_id	# Attach transaction ID in the requestbody
	data["timestamp"] = timestamp 			# Attach timestamp in the request body
	payments.append(data)					# Add the request body in our "payments" database
 
	return data,201


@app.route('/payments/<transaction_id>', methods=["GET"])
@validate()
def getPayment(transaction_id: UUID4):
	for txn in payments:
		if txn["transaction_id"] == str(transaction_id):
			return txn

	return {"message": "Transaction not found"},404

@app.route('/payments', methods=["GET"])
def getAllPayments():
	return payments



@app.route('/payments/<transaction_id>', methods=["PATCH"])
def update_one_transaction(transaction_id):
	input_status = request.get_json().get("status")
	for txn in payments:
		if txn["transaction_id"] == transaction_id:
			txn["status"] = input_status
			return txn

	return {"message": "Transaction not found"}


@app.route('/payments/<transaction_id>', methods=["DELETE"])
def delete_one_payment(transaction_id):
	for index, txn in enumerate(payments):
		if txn["transaction_id"] == transaction_id:
			payments.pop(index)
			return {"message": "Transaction deleted"}
	return {"message": "Transaction not found"}



# Custom error handler for 405
@app.errorhandler(405)
def method_not_allowed_error(error):
	return {"error": "Method Not Allowed!"},405



if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 8000, debug=True)
