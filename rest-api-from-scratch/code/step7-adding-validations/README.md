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

## Validating Single Transaction Fetch Request
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
