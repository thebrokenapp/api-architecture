# Add caching to your Payments API

## SQLite3
### Install SQLite3
```bash
sudo apt install sqlite3
```
Check if it's installed
```bash
sqlite3 --version
```


### Create payments table
#### Create a database
```bash
sqlite3 upi.db
```
In the shell that opens up, enter:
```sql
CREATE TABLE payments (
    transaction_id TEXT,
    user_name TEXT,
    amount TEXT NOT NULL,
    status TEXT NOT NULL,
    payer_upi TEXT NOT NULL,
    payee_upi TEXT NOT NULL,
    note TEXT,
    timestamp TEXT NOT NULL
);
```

#### Upload payment.csv in the db
```bash
.mode csv
.import /path/to/your/payments.csv payments
```


## Redis
### Install Redis
```url
https://github.com/ankitforcodes/redis/blob/main/installing_on_ubuntu.txt
```

### Start Redis
```bash
redis-server redis.conf
```


## API Changes
### POST /payments
Add import statement
```python
import sqlite3
```

#### Create a function to connect to SQLite DB
```python
# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn
```

#### Change the `POST /payments` logic
```python
@app.route('/payments', methods=['POST'])
@validate()
def initiate_payment(body: PaymentBody):
	data = request.get_json()
	user_name = data.get("user_name")
	amount = data.get("amount")
	payer_upi = data.get("payer_upi")
	payee_upi = data.get("payee_upi")
	note = data.get("note")				
	transaction_id = str(uuid.uuid4())		
	timestamp = datetime.utcnow()			
	status = "initiated"
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO payments (transaction_id, user_name,amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?, ?,?, ?, ?,?)''',
	(transaction_id, user_name,amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
 
	return {"message": "transaction created", "transaction_id": transaction_id}
```

### Fetch Single Payment
#### Change `GET /payments/<transaction_id>`
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

	return dict(payment)
	
```

### Update Payment
#### Change `PATCH /payment/<transaction_id>
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

	return jsonify({"message": "Transaction updated"})
```

### Delete Payment
#### Change `DELETE /payment/<transaction_id>`
```python
@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
	conn = get_db_connection()
	cursor = conn.cursor()

	cursor.execute('''DELETE FROM payments WHERE transaction_id = ?''', (transaction_id,))

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	conn.commit()
	conn.close()

	return jsonify({"message": "Transaction deleted!"})
```
