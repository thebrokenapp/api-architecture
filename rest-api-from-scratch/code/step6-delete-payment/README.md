
# Implementing Delete Payment Endpoint

# Code
This code will be added as another `@app.route` in you `app.py` file.


#### Add New route
We are adding the `DELETE` request to the `/payments/{transaction_id}` path.
```python
@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
```


#### Attach the business logic to the route
The following piece of code  needs to be added in the `updatePayment` function
```python
for index, payment in enumerate(payments):			# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)							# update the previous JSON with new JSON
			return Response(status=204)                 # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404
```


`Line1` We loop over all the transactions in our `payments` list

`Line2` We check if any transaction matching with transaction_id

`Line3` Delete the JSON if there is any match

`Line4` Note the `204` response code

#### Your code should overall look like this right now
```python
from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from flask import Response

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
 
	return data								# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc


@app.route('/payments/<transaction_id>')
def getPayment(transaction_id):
	for payment in payments:				# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			return payment                              # if anything matches, then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 


@app.route('/payments/<transaction_id>', methods = ["PATCH"])
def updatePayment(transaction_id):
	data = request.get_json()
	timestamp = datetime.utcnow()							
	for payment in payments:							
		if payment["transaction_id"] == transaction_id:	
			payment["status"] = data["status"]						
			payment["timestamp"] = timestamp
			return payment                              

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 


@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
	for index, payment in enumerate(payments):			# loop over the list 
		if payment["transaction_id"] == transaction_id:	# check transaction_id of each item in the list
			payments.pop(index)							# update the previous JSON with new JSON
			return Response(status=204)                 # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 



if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
```

#### Run the code
```bash
python app.py
```
## Try to Make the API Call

#### Make the API call using POSTMAN
Make the API call to `/payments` endpoint in Postman to see if you are getting an empty response
```http
DELETE /payments/{transaction_id}
```

