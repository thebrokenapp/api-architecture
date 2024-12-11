# There is a Problem!

#### Fetch a transaction ID so that its loaded in Redis
#### Now, make a PATCH request to update the payment
#### Fetch the data again using GET request - do you see the change? No!

#### Add the logic to invalidate the cache everytime a PATCH or DELETE request is made (2nd last line)
```python
@app.route('/payments/<transaction_id>', methods = ["PATCH"])
@validate()
def updatePayment(transaction_id: UUID4, body: Status):
	data = request.get_json()
	status = data.get("status")
	transaction_id = str(transaction_id)
	timestamp = datetime.utcnow()							
	
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('''UPDATE payments SET status = ?, timestamp = ? WHERE transaction_id = ? ''', (status, timestamp, transaction_id))
	conn.commit()
	conn.close()

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	r.delete(transaction_id)	# this deletes the key in redis
	return jsonify({"message": "Transaction updated"})
```
