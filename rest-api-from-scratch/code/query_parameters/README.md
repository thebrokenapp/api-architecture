### Filter all transactions with `status` as `success`
```python
@app.route('/payments/<user_name>', methods=["GET"])
def get_payment_for_one_user(user_name):
	status = request.args.get('status', 'initiated')
	return_list = []
	if status is not None:
		for txn in payments_db:
			if txn["status"] == status:
				return_list.append(txn)
		return {"transactions": return_list}

	for payment in payments_db:
		if payment["user_name"] == user_name:
			return_list.append(payment)
	return {"payment_list": return_list}
```

## Get all query params in one go in dictionary
```python
query_params = request.args.to_dict()
```
