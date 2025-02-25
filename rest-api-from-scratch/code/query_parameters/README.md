### Filter all transactions with `status` as `success`
```python
@app.route('/payments', methods=["GET"])
def get_payment_for_one_user(user_name):
	status = request.args.get('status', 'initiated')
	amount = request.args.get('amount', 0)
	print(status)
	return_list = []
	for payment in payments_db:
		if payment["user_name"] == user_name:
			if payment["status"] == status and payment["amount"]> int(amount):
				return_list.append(payment)

	return {"payment_list": return_list}
```

## Get all query params in one go in dictionary
```python
query_params = request.args.to_dict()
```
