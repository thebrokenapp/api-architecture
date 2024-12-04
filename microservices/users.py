from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from flask import Response

app = Flask(__name__)

@app.route('/user/apiStatus')
def status():
	return {"message": "User API is running!"}

users = []

@app.route('/user')
def getUsers():
	return {"users": users}

@app.route('/user', methods=["POST"])
def initiatePayment():
	data = request.get_json()				# extract the request body and store it in variable "data"
	timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["timestamp"] = timestamp 			# Attach timestamp in the request body
	users.append(data)					# Add the request body in our "payments" database
 
	return data								# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc


@app.route('/user/<user_id>')
def getUser(user_id):
	for user in users:				# loop over the list 
		if user["user_id"] == user_id:	# check transaction_id of each item in the list
			return user                              # if anything matches, then return the item

	return jsonify({"message": "User not found"}),404   # otherwise return 404 


if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8001, debug=True)
