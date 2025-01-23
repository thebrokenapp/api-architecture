## Read Ahead Implementation in Payments API

#### Make the change in GET /payments 
```python
@app.route('/payments', methods=["GET"])
def get_all_payments():
	print("yo")
	page = int(request.args.get('page', 1))
	size = int(request.args.get('size', 3))
	offset = (page - 1) * size
	redis_key = "page_"+ str(page)
	cache = r.get(redis_key)
	if cache:
		next_page_data = json.loads(cache)
		r.publish("fetch_payment_channel", json.dumps({"page": page, "size": size})) 
		return {"payments": next_page_data, "page": page, "from": "redis"}

	else:
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments LIMIT ? OFFSET ?', (size, offset))
		payments = cursor.fetchall()
		conn.close()
		output_list = []
		for payment in payments:
			output_list.append(dict(payment))

	r.publish("fetch_payment_channel", json.dumps({"page": page, "size": size})) 
	return {"payments": output_list, "page": page, "from": "sqlite3"}
```

#### Read Ahead Listener
```python
import redis
import json
import random
import sqlite3

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('/dev_box/trainings/npci-hyd-jan-2025/trials/microservices/upi.db')    # This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn

# Subscribe to the payment channel
pubsub = redis_client.pubsub()
pubsub.subscribe("fetch_payment_channel")

print("Listening for payment messages...")

# Listen for messages and process them
for message in pubsub.listen():
    if message['type'] == 'message':
        # Parse the message data
        payment_data = json.loads(message['data'])
        page = int(payment_data.get('page')) + 1
        size = int(payment_data.get('size'))
        offset = (page - 1) * size

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payments LIMIT ? OFFSET ?', (size, offset))
        payments = cursor.fetchall()
        conn.close()
        output_list = []
        for payment in payments:
            output_list.append(dict(payment))
        redis_key = "page_" + str(page)
        redis_client.set(redis_key, json.dumps(output_list))
```
