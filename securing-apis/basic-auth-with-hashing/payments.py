from flask import Flask, request, jsonify, Response
from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
import random
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


class Payment(BaseModel):
	amount : int
	payer_upi : str
	payee_upi: str
	note: str = ''

	class Config:
		extra = "forbid"

class SignUp(BaseModel):
	username : str
	password : str
	mobile: str

	class Config:
		extra = "forbid"

app = Flask(__name__)
auth = HTTPBasicAuth()
#PrometheusMetrics(app)


users_database = {
}


@auth.verify_password
def verify_password(username, password):
    if username in users_database and check_password_hash(users_database.get(username), password):
        return username

@app.route('/apiStatus')
@auth.login_required
def status():
	return {"message": "API is up!"}



payments = []
my_users = []


@app.route('/payments', methods=["GET"])
@auth.login_required
def getPayments():
	return {"data": payments}



@app.route('/payments', methods=["POST"])
@validate()
@auth.login_required
def initiatePayment(body: Payment):
	data = body.dict()				# extract the request body and store it in variable "data"
	txn_id = str(uuid.uuid4())		# create a new transaction ID using uuid() library
	current_timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["transaction_id"] = txn_id	# Attach transaction ID in the requestbody
	data["timestamp"] = current_timestamp 			# Attach timestamp in the request body
	payments.append(data)					# Add the request body in our "payments" database
 
	return data						# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc



@app.route('/payments/<transaction_id>')
@validate()
@auth.login_required
def getPayment(transaction_id: UUID4):
	for payment in payments:
		if payment["transaction_id"] == str(transaction_id):
			return payment

	return jsonify({"message": "Transaction not found"}),404



@app.route('/payments/note/<note>')
@auth.login_required
def getPaymentByNote(note):
	for payment in payments:
		if payment["note"] == note:
			return payment

	return jsonify({"message": "Transaction not found"}),404


@app.route('/payments/<transaction_id>', methods = ["PUT"])
@auth.login_required
def updatePayment(transaction_id):
	data = request.get_json()							# extract the request body and store it in variable "data"
	for payment in payments:							# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payment.update(data)						# update the previous JSON with new JSON
			return payment                              # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404


@app.route('/payments/<transaction_id>', methods = ["DELETE"])
@auth.login_required
def deletePayment(transaction_id):
	for index, payment in enumerate(payments):			# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)							# update the previous JSON with new JSON
			return Response({"message": "Resource deleted!"},  status=204)                 # then return the item

	return jsonify({"message": "Transaction not found"}),200   # otherwise return 404



@app.route('/signUp', methods=["POST"])
def signUp():
	data = request.get_json()				
	request_user_name= data["user_name"]
	request_password = data["password"]
	hashed_password = generate_password_hash(request_password)
	
	users_database[request_user_name] = hashed_password
	
	print(users_database)				
 
	return {"message":"User created"}						

@app.route('/random', methods=["GET"])
def random_path():
	number = random.randint(1, 10)
	if number < 3:
		return jsonify({"message": "Sending 201"}),201
	if number == 4:
		return jsonify({"message": "Sending 201"}),403
	if number >= 5:
		return jsonify({"message": "Sending 201"}),500
	else:
		return jsonify({"message": "Sending 201"}),204	


if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 5000)
