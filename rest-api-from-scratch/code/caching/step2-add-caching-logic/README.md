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
