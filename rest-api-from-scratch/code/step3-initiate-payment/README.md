
# Implementing Creating One Payment Endpoint 
### POST /payments


# Code
This code will be added as another `@app.route` in you `app.py` file.

#### Import new functions
Since we are adding some features, we want to import some python libraries like `request`, `uuid`, `datetime`, etc
Change you import statements to make them look like below
```python
from flask import Flask, request, jsonify
from datetime import datetime
import uuid
```
#### Add New route
We are adding the `POST` request to the `/payments` path to add the payment initiation endpoint.
Note, that this time we had to add `methods` as `[POST]` explicitly.
In earlier routes we did not have to mention methods because `[GET]` gets defined by default
```python
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
```

#### Attach the business logic to the route
The following piece of code  needs to be added in the `initiatePayment` function
```python
	data = request.get_json()				# extract the request body and store it in variable "data"
	transaction_id = str(uuid.uuid4())		# create a new transaction ID using uuid() library
	timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["transaction_id"] = transaction_id	# Attach transaction ID in the requestbody
	data["timestamp"] = timestamp 			# Attach timestamp in the request body
	payments.append(data)					# Add the request body in our "payments" database
 
	return data						# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc
```

#### Your code should overall look like this right now
```python
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
 
	return data						# respond back to client with request body along with newly added fields like transaction ID, timestamp, etc


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
POST /payments
```

#### Sample Request Body
```http
{
    "amount": 12000,
    "payer_upi": "abx@okhdfc",
    "payee_upi": "qwe-sbi",
    "note": "Books"
}
```


