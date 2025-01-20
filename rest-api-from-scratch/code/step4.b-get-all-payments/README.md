
# Implementing Fetch All Payments For a User

### A question
We have seen how `GET` requests should not be having a request body.
So where do we provide the `user_name` information?

# Code
This code will be added as another `@app.route` in you `app.py` file.

#### Create an empty payment list
This will act as our database. We are not adding the actual database logic to keep the code simple and concentrated on the API part
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []
```
#### Add New route
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments/<user_name>')
```

#### Attach the business logic to the route
We call this function as `getPayments` function
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments/<user_name>')
def getPayments(user_name):
	payment_list = []
	for payment in payments:
		if payment["user_name"] == user_name:
			payment_list.append(payment)
	return {"payments": payment_list}
```

#### Return the `payments` list
`payments` list that we created holds all the payment transaction.
We will later add the insertion logic to the payment list. But for now, we are interested in returing the `payments` list which holds all transactions

```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments/<user_name>')
def getPayments(user_name):
	payment_list = []
	for payment in payments:
		if payment["user_name"] == user_name:
			payment_list.append(payment)
	return {"payments": payment_list}
```

#### Add the server and port details
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments/<user_name>')
def getPayments(user_name):
	payment_list = []
	for payment in payments:
		if payment["user_name"] == user_name:
			payment_list.append(payment)
	return {"payments": payment_list}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
```
## Try to Make the API Call

#### Make the API call using POSTMAN
Make the API call to `/payments` endpoint in Postman to see if you are getting an empty response
```http
GET /payments/ankit
```



