### Validating Update Payment

```http
PATCH  /payments/{transaction_id}
```
#### Request Body
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`         | `string` | **Required** |

Add one more validation class (note this will also enusre clients cannot add any extra fields)
```python
class Status(BaseModel):
	status : str
	class Config:
		extra = "forbid"
```


Let's add `@validate` to our route like the following:
```python
@app.route('/payments/<transaction_id>', methods = ["PATCH"])
@validate()
```

This time, we have to validate both the `url` and the `body` and we do it using the same logic as earliers

```python
@app.route('/payments/<transaction_id>', methods = ["PATCH"])
@validate()
def updatePayment(body: Status, transaction_id: UUID4):
  data = request.get_json()
```

Overall your code should look like this
```python
@app.route('/payments/<transaction_id>', methods = ["PATCH"])
@validate()
def updatePayment(body: Status, transaction_id: UUID4):
	data = request.get_json()
	timestamp = datetime.utcnow()							
	for payment in payments:							
		if payment["transaction_id"] == str(transaction_id):	
			payment["status"] = data["status"]						
			payment["timestamp"] = timestamp
			return payment                              

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404 

```

### Postman
* Try making a valid request
* Try making a request with invalid transaction_id
* Try making a request with invalid request body (missing fields or invalid data-type)
