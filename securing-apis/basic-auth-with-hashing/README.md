# Hash Password 


#### Create `users` table in SQLite3
Enter in your UPI DB
```bash
sqlite3 upi.db
```
Create table
```sql
CREATE TABLE users (
    user_name TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);
```



#### Import Library
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

#### Add password checking logic
```python
@auth.verify_password
def verify_password(username, password):
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT hashed_password FROM users WHERE user_name = ?', (username,))
	password_row = cursor.fetchone()
	if password_row is None:
		return None
	retrieved_password = password_row["hashed_password"]
	print("password from sqlite3:",retrieved_password)
	print("password from Auth header", password)
	conn.close()
	if check_password_hash(retrieved_password, password):
		return username
```

#### Create `/user` route
```python
@app.route('/user', methods=["POST"])
def sign_up():
	data = request.get_json()				
	request_user_name= data["user_name"]
	request_password = data["password"]
	hashed_password = generate_password_hash(request_password)
	print(request_user_name, hashed_password)

	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO users (user_name, hashed_password) VALUES (?, ?)''',(request_user_name, hashed_password))
	conn.commit()
	conn.close()
	#users[request_user_name] = hashed_password
	return {"message":"User created"}
```

#### Make a request to protected route
```python
@app.route('/apiStatus', methods=['GET'])
@auth.login_required
def api_status():
	return {"message": "API is up!"}
```
