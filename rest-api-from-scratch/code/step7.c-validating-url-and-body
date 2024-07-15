### Validating Update Payment

```http
  PUT /payments/{transaction_id}
```
#### Request Body
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `amount`         | `Integer` | **Required** |
| `payer_upi`      | `string`  | **Required** |
| `payee_upi`      | `string`  | **Required** |
| `note`      	   | `string`  | **Optional** |

Let's add `@validate` to our route like the following:
```python
@app.route('/payments/<transaction_id>', methods = ["PUT"])
@validate()
```

This time, we have to validate both the `url` and the `body` and we do it using the same logic as earliers

```python
@app.route('/payments/<transaction_id>', methods = ["PUT"])
@validate()
def updatePayment(body: Payment, transaction_id: UUID4):
  data = body.dict()
```

Overall your code should look like this
```python
@app.route('/payments/<transaction_id>', methods = ["PUT"])
@validate()
def updatePayment(body: Payment, transaction_id: UUID4):
	data = body.dict()									# extract the request body and store it in variable "data"
	for payment in payments:							# loop over the list 
		if payment["transaction_id"] == str(transaction_id):	# check transaction_id of each item in the list
			payment.update(data)						# update the previous JSON with new JSON
			return payment                              # then return the item

	return jsonify({"message": "Transaction not found"}),404   # otherwise return 404
```

### Postman
* Try making a valid request
* Try making a request with invalid transaction_id
* Try making a request with invalid request body (missing fields or invalid data-type)
