# Microservices with API Gateway
## High Level Steps involved
#### 1. Start payments api on port 8000
#### 2. Start users api on port 8001
#### 3. Install Nginx
#### 4. Configure routing
#### 5. Launch Nginx
#### 6. Try in Postman

This guide provides steps to install and configure NGINX on an Ubuntu system to serve your applications.

## Steps
### Users Service
#### Create a users table
```bash
sqlite3 upi.db
CREATE TABLE users (
    username TEXT,
    password TEXT,
    registration_date TEXT,
    product TEXT
);
```
#### Sign Up (Create a user)
```python
@app.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()				   # extract the request body and store it in variable "data"
	user_name = data.get("user_name")		# extract user name from request body
	password = data.get("password")			# extract password from request body
	registration_date = datetime.utcnow()
	product = data.get("product")
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO users (username, password, registration_date, product) VALUES (?, ?, ?,?)''',
	(user_name, password, registration_date, product))
	conn.commit()
	conn.close()
	return {"message": "User created"},201
```
#### Request body for Creating user
```json
{
    "user_name": "ankit",
    "password": "admin",
    "product": "upi"
}
```


#### Fetch All Users
```python
@app.route('/users', methods=['GET'])
def get_all_users():
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''SELECT * FROM users''')
	users = cursor.fetchall()
	users_list = []
	for row in users:
		users_list.append( {"user_name": row[0], "password": row[1], "date": row[2], "product": row[3]})

	return {"users": users_list},200
```

#### Fetch One User
```python
@app.route('/users/<user_name>', methods=['GET'])
def get_one_user(user_name):
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''SELECT * FROM users where username = ?''',(user_name,))
	user = cursor.fetchone()

	if user is None:
		conn.close()
		return {"message": "User not found"}, 404

	user_data = {"user_name": user[0], "password": user[1], "date": user[2], "product": user[3]}
	conn.close()
	return jsonify(user_data), 200
```

#### Delete a user
```python
@app.route('/users/<user_name>', methods=['DELETE'])
def delete_one_user(user_name):
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute("""DELETE FROM users WHERE username = ?""", (user_name,))
	conn.commit()

	if cursor.rowcount == 0:  # Check if no rows were deleted
		conn.close()
		return {"message": "User not found"}, 404

	conn.close()
	return {}, 204
```

#### Question
```http
Is this a microservice or monolith?
```

## Separate Payments and User functionality in different microservices
```bash
Payments API 5000
Users API 5001
```


**Install NGINX**:
   ```bash
   sudo apt update
   sudo apt install nginx -y
   ```
**Start and Enable NGINX**:
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

**Check NGINX Status**:
   ```bash
   sudo systemctl status nginx
   ```
**Adjust Firewall (if applicable)**:
   ```bash
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   sudo ufw status
   ```

   
### Access NGINX Default Page**:
   Open a web browser and navigate to your server’s IP address or `http://localhost`.

### Configure NGINX for Your Application:
   1. Create a new server block:
      ```bash
      sudo nano /etc/nginx/sites-available/payments
      ```
   3. Add the following configuration:
      ```json
      server {
         listen 80;
         server_name 127.0.0.1;  # Replace with your actual domain or IP
      
         location  /payments  {
            proxy_pass http://127.0.0.1:8000;
         }
         
         location  /users  {
            proxy_pass http://127.0.0.1:8001;
         }
      }
      ```
   4. Enable the configuration:
      ```bash
      sudo ln -s /etc/nginx/sites-available/payments /etc/nginx/sites-enabled/
      ```
   5. Test the configuration:
      ```bash
      sudo nginx -t
      ```
   7. Restart NGINX:
      ```bash
      sudo systemctl restart nginx
      ```

#### Make requests from POSTMAN
```url
GET http://127.0.0.1:80/payments/c80e58fb-2806-48f1-9e40-90feeabd38c7
GET http://127.0.0.1:80/users
```


#### Uninstalling nginx
```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
sudo apt remove --purge nginx nginx-common -y
sudo apt autoremove --purge -y
sudo rm -rf /etc/nginx
sudo rm -rf /var/log/nginx
nginx -v
```
