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
