# Add Caching Logic to GET Payment Method

#### Install Redis
```bash
pip install redis
```

#### Import Redis
```python
import redis
```

#### Connect to Redis
```redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
```

#### Edit your `GET /payment/<transaction_id>` block to add caching logic
This code contains to send the data to cache everytime a transaction is fetched
```python
@app.route('/payments/<transaction_id>')
@validate()
def getPayment(transaction_id: UUID4):
	redis_key = str(transaction_id)
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
	payment = cursor.fetchone()
	conn.close()
	if payment is None:
		return {"message": "Transaction not found"}, 404

  	# Add this line
	r.hset(redis_key, mapping=dict(payment))

	return dict(payment)
```



Now, we add the logic - where everytime a transaction is fetched we first look into cache, then into SQLlite3
```python
@app.route('/payments/<transaction_id>')
@validate()
def getPayment(transaction_id: UUID4):
	redis_key = str(transaction_id)
	cache_data = r.hgetall(redis_key)
	if cache_data:
		print("data came from redis")
		return jsonify(cache_data)
	else:
		print("data came from sqlite3")
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
		payment = cursor.fetchone()
		conn.close()
		if payment is None:
			return {"message": "Transaction not found"}, 404

		r.hset(redis_key, mapping = dict(payment))

	return dict(payment)
```
