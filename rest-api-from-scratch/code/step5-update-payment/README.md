
# Implementing Update Payment Endpoint

# Code
This code will be added as another `@app.route` in you `app.py` file.


#### Add New route
We are adding the `PUT` request to the `/payments/{transaction_id}` path.
```python
@app.route('/payments/<transaction_id>', methods = ["PATCH"])
def updatePayment(transaction_id):
```


#### Attach the business logic to the route
The following piece of code  needs to be added in the `updatePayment` function
```python
data = request.get_json()
timestamp = datetime.utcnow()							
for payment in payments:							
	if payment["transaction_id"] == transaction_id:	
		payment["status"] = data["status"]						
		payment["timestamp"] = timestamp
		return payment                              

return jsonify({"message": "Transaction not found"}),404
```
`Line1`: We get the payload from request and store it in data 
variable

`Line2` We loop over all the transactions in our `payments` list

`Line3` We check if any transaction matching with transaction_id

`Line4` Update the previous JSON with new JSON

`Line5` return the new JSON to the user

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
PUT /payments/{transaction_id}
```

#### Sample Request Body
```http
{
    "amount": 130,
    "note": "Ola",
    "payee_upi": "qwe-sbi",
    "payer_upi": "abx@okhdfc",
    "status": "initiated",
    "timestamp": "Sun, 07 Jul 2024 18:43:31 GMT",
    "transaction_id": "23cf27ff-489c-428d-81cb-1eb556291560"
}
```


