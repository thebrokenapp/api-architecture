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
