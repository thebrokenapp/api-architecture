### Filter all transactions with `status` as `success`
```python
@app.route('/payments', methods=['GET'])
def get_all_payments():
	status = request.args.get('status')
	if status is not None:
		return_list = []
		for txn in payments:
			if txn["status"] == status:
				return_list.append(txn)
		return {"transactions": return_list}

	return {"transactions": payments}

```

## Get all query params in one go in dictionary
```python
query_params = request.args.to_dict()
```
