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
    transaction_id TEXT PRIMARY KEY,
    amount TEXT NOT NULL,
    status TEXT NOT NULL,
    payer_upi TEXT NOT NULL,
    payee_upi TEXT NOT NULL,
    note TEXT,
    timestamp TEXT NOT NULL
);
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

Create a function to connect to SQLite DB
```python
# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn
```

Change the `POST /payments` logic
```python
@app.route('/payments', methods=['POST'])
@validate()
def initiate_payment(body: PaymentBody):
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
 
	return {"message": "transaction created", "transaction_id": transaction_id}
```