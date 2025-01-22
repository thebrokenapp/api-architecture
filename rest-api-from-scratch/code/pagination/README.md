## Get All Payments in a Paginated Way

```python
@app.route('/payments', methods=["GET"])
def get_all_payments():
	page = int(request.args.get('page', 1))
	size = int(request.args.get('size', 3))
	offset = (page - 1) * size

	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM payments LIMIT ? OFFSET ?', (size, offset))
	payments = cursor.fetchall()
	conn.close()
	output_list = []
	for payment in payments:
		output_list.append(dict(payment))

	return {"payments": output_list}
```
