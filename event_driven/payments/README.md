## Make Changes to your Payments API

#### POST Request
Add the logic to publish json to pubsub channel after data is inserted in primary DB (not before)
```python
r.publish("initiate_payment_channel", json.dumps({"amount": amount, "payer_upi": payer_upi, "payee_upi": payee_upi, "note": note, "transaction_id": transaction_id, "timestamp": str(timestamp), "status": status}))
```

Overall your POST request will look like
```python
@app.route('/payments', methods = ['POST'])
@validate()
def make_a_payments(body: PaymentRequestBody):
	data = request.get_json()
	amount = data.get("amount")
	payer_upi = data.get("payer_upi")
	payee_upi = data.get("payee_upi")
	note = data.get("note")				
	transaction_id = str(uuid.uuid4())		
	timestamp = datetime.utcnow()			
	status = "initiated"
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO payments (transaction_id, amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?,?, ?, ?,?)''',
	(transaction_id, amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
	r.publish("initiate_payment_channel", json.dumps({"amount": amount, "payer_upi": payer_upi, "payee_upi": payee_upi, "note": note, "transaction_id": transaction_id, "timestamp": str(timestamp), "status": status}))
	return {"message": "transaction created", "transaction_id": transaction_id}
```

### Create a fraud_detection.py listener
```python
import redis
import json
import random

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Subscribe to the payment channel
pubsub = redis_client.pubsub()
pubsub.subscribe("initiate_payment_channel")

print("Listening for payment messages...")

# Listen for messages and process them
for message in pubsub.listen():
    if message['type'] == 'message':
        # Parse the message data
        payment_data = json.loads(message['data'])
        # Randomly decide if it's fraud or not
        if random.choice([True, False]):
            fraud_status = "fraud"
        else:
            fraud_status = "not fraud"
        
        # Print the result
        print("Payment ID:", payment_data['transaction_id'], " Status:", fraud_status)
```

### Create send_notification listener
```python
import redis
import json
import random

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Subscribe to the payment channel
pubsub = redis_client.pubsub()
pubsub.subscribe("initiate_payment_channel")

print("Listening for payment messages...")

# Listen for messages and process them
for message in pubsub.listen():
    if message['type'] == 'message':
        # Parse the message data
        payment_data = json.loads(message['data'])        
        # Print the result
        print("SMS Sent to:", payment_data['payee_upi'])

```


### Create reward_calculator listener
```python
import redis
import json
import random

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Subscribe to the payment channel
pubsub = redis_client.pubsub()
pubsub.subscribe("initiate_payment_channel")

print("Listening for payment messages...")

# Listen for messages and process them
for message in pubsub.listen():
    if message['type'] == 'message':
        # Parse the message data
        payment_data = json.loads(message['data'])
        reward_multiplier = round(random.uniform(0.01, 0.3), 2)
        
        # Print the result
        print("Rewards:", int(payment_data['amount'])* reward_multiplier)

```

### DIY
```http
When the transaction is fraud, update the payment status as failed.
When is not-fraud, update the status as success
```
