from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from flask import Response

app = Flask(__name__)

@app.route('/payments/apiStatus')
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
 
	return data								# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc


@app.route('/payments/<transaction_id>')
def getPayment(transaction_id):
	for payment in payments:				# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			return payment                              # if anything matches, then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 


@app.route('/payments/<transaction_id>', methods = ["PUT"])
def updatePayment(transaction_id):
	data = request.get_json()							# extract the request body and store it in variable "data"
	for payment in payments:							# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payment.update(data)						# update the previous JSON with new JSON
			return payment                              # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 

@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
	for index, payment in enumerate(payments):			# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)							# update the previous JSON with new JSON
			return Response(status=204)                 # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 



if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8000, debug=True)
