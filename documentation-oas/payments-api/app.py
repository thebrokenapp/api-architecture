from flask import Flask, request, jsonify, Response
from datetime import datetime
import uuid


app = Flask(__name__)



@app.route('/apiStatus', methods=["GET"])
def status():
	return {"message": "API is running!"}

payments = []


@app.route('/payments', methods=["GET"])
def getPayments():
	return {"data": payments}


@app.route('/payments', methods=["POST"])
def initiatePayment():
	data = request.get_json()
	transaction_id = str(uuid.uuid4())
	timestamp = datetime.utcnow()
	data["status"] = "initiated"
	data["transaction_id"] = transaction_id
	data["timestamp"] = timestamp
	payments.append(data) 	

	return data

@app.route('/payments/<transaction_id>')
def getPayment(transaction_id):
	for payment in payments:
	    if payment["transaction_id"] == transaction_id:
	        return payment

	return jsonify({"message": "Transaction not found"}),404


@app.route('/payments/<transaction_id>', methods = ["PUT"])
def updatePayment(transaction_id):
	data = request.get_json()							# extract the request body and store it in variable "data"
	for index, payment in enumerate(payments):							# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)
			payments.append(data)						# update the previous JSON with new JSON
			return data                              # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404


@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
	for index, payment in enumerate(payments):			# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)							# update the previous JSON with new JSON
			return Response(status=204)                 # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404


if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 5000, debug=True)


