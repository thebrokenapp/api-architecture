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
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
	payment = cursor.fetchone()
	conn.close()
	if payment is None:
		return {"message": "Transaction not found"}, 404

  # Add these two extra lines
	redis_key = str(transaction_id)
	r.hmset(redis_key, dict(payment))

	return dict(payment)
```
