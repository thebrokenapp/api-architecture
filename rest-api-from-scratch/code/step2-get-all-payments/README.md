
# Implementing Fetch All Payments Endpoints


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

@app.route('/payments')
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

@app.route('/payments')
def getPayments():
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

@app.route('/payments')
def getPayments():
	return {"payments": payments}
```

#### Add the server and port details
```python
from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments')
def getPayments():
	return {"payments": payments}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
```
## Try to Make the API Call

#### Make the API call using POSTMAN
Make the API call to `/payments` endpoint in Postman to see if you are getting an empty response
```http
GET /payments
```



