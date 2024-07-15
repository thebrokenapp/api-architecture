# Validation Layer

Additional libraries are required for validations, so lets install them
```bash
pip install Flask-Pydantic
pip install pydantic
```

## Import the required libraries 

```python
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
```

## Validating Single Transaction Fetch Request: GET /payments/{transaction_id}
We can fetch details of one transaction using transaction ID. And the transaction id has to be in `UUID` format. So let's add the validation logic, which will reject any request that does not pass valid `UUID` in the request URL

To put any path behind a validation layer, we add `@validate` just before the function definition:
```python
@app.route('/payments/<transaction_id>')
@validate()
```

In the function definition, asses the datatype of transaction_id as `UUID`
```python
def getPayment(transaction_id: UUID4):
```

Overall, your function should look like this:
```python
@app.route('/payments/<transaction_id>')
@validate()
def getPayment(transaction_id: UUID4):
	for payment in payments:				
		if payment["transaction_id"] == str(transaction_id):	
			return payment                             

	return jsonify({"message": "Transaction not found"}),404
```

#### Try making request in Postman with incorrect format of transaction ID and observe if the error message indicates the invalid request
---



### Validating Initiate Payment

```http
POST /payments/{transaction_id}
```


| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `amount`         | `Integer` | **Required** |
| `payer_upi`      | `string`  | **Required** |
| `payee_upi`      | `string`  | **Required** |
| `note`      	   | `string`  | **Optional** |


We will implement two kinds of validation: `lax` and `strict`

#### Lax Validation
Is a loose validation where you allow the client to make request in data-types in format other than specified ones. For example: `amount` is Integer, but we can allow user to make request as `string` but internally we will convert it to `integer`

#### Let's Create a Class for Request Body
```python
class Payment(BaseModel):
	amount : int
	payer_upi : str
	payee_upi: str
	note: str = ''
```

Now we add validation layer on `POST /payments` route
```python
@app.route('/payments', methods=["POST"])
@validate()
```

In the validation, we assess that `body` conforms to `Payment` class using the following code:
```python
def initiatePayment(body: Payment):
```

We then convert body to JSON/dictionary:
```python
def initiatePayment(body: Payment):
	data = body.dict()
```

Overall your `POST /payments` should look like this:
```python
@app.route('/payments', methods=["POST"])
@validate()
def initiatePayment(body: Payment):
	data = body.dict()				# extract the request body and store it in variable "data"
	transaction_id = str(uuid.uuid4())		# create a new transaction ID using uuid() library
	timestamp = datetime.utcnow()			# create a new timestamp to capture the transaction time
	data["status"] = "initiated"			# by default all transactions starts with status as "initiated"
	data["transaction_id"] = transaction_id	# Attach transaction ID in the requestbody
	data["timestamp"] = timestamp 			# Attach timestamp in the request body
	payments.append(data)					# Add the request body in our "payments" database
 
	return data
```

#### Postman Request
Try to make postman request with amount as both `int` and `string`.
You will notice, that even though we have defined `amount` as `int`, our API still allows `string` value but stores it as an `int` (confirm with `GET` request)


#### String Validation
In strict validation we dont allow any request with any mismatch of datatypes and to enforce strict validation, change the `Payment` class as following

```python
class Payment(BaseModel):
	amount : int = Field(strict=True)
	payer_upi : str
	payee_upi: str
	note: str = ''
```

#### Postman
* Try making request with correct and incorrect dataype
* Try making request without some of the `required` field and confirm if it's getting rejected
