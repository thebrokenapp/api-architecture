## Adding Token Based Auth to Payment API


#### Change your `@app.before_request
Now we have one endpoint `/login` that taken in UN:Password and other endpoints `/payments` that takes in Token
```python
# Before request hook
@app.before_request
def before_request():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_header = auth_header.split(' ')
		if auth_header[0] == "Bearer":
			request.username = "Token Based User"
		elif auth_header[0] == "Basic":
			encoded_credentials = auth_header[1]
			decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
			request.username = decoded_credentials.split(':')[0]
	else:
		request.username = "anonymous"
	
	if not request.headers.get('X-Request-GUID'):
		request.guid = str(uuid.uuid4())  # Store GUID in the request object
	else:
		request.guid = request.headers.get('X-Request-GUID')
	audit_logger.info(f"Request -> User: {request.username} | Request GUID: {request.guid} | Action: {request.method} | Resource: {request.path}")
```


#### Implement /login route to create tokens
```python
# Login route to authenticate and generate a token
@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    username = auth.current_user()  # Get the authenticated username
    # Generate a token (for simplicity, using a random UUID)
    token = str(uuid.uuid4())
    r.setex(token, 120, username)	# store the token as key and username as value in Redis with a TTL of 2 mins
    # Store the token in the token store
    #token_store[token] = username
    return jsonify({"token": token}), 200
```

#### Protect the routes behind @token_required decorator
Pass the `username` argument to the function and return the username in response too. This shows the capability of finding out the user from the token provided
```python
# Status route
@app.route('/payments', methods=['GET'])
@token_required
def get_all_payments(username):
	status = request.args.get('status')
	if status is not None:
		return_list = []
		for txn in payments:
			if txn["status"] == status:
				return_list.append(txn)
		return {"transactions": return_list}

	return {"transactions": payments, "requested_by": username}
```

#### Add token_required function
```python
def token_required(f):
    @wraps(f)
    def wrapper():
        try:
            token = request.headers.get('Authorization').split("Bearer ")[1]
            if not token:
            	return {"msg": "No token provided"}, 401

            username = r.get(token)
            if not username:
            	return {"msg": "Token expired!"}, 401

            return f(username)
        except:
            return {"msg": "No token provided"}, 401
    return wrapper
```

#### Check the increase in speed!
Keep any other route still behind simple auth which check username password again using hashing
```python
@app.route('/apiStatus', methods=['GET'])
@limiter.limit("8000 per day")
@auth.login_required
def api_status():
	print("User is: ", auth.current_user())
	return {"message": "API is up!"}
```

Make an API request to `/apiStatus` and compare the speed!
Any route behind `Token` auth is at least 5X faster than routes behind `Basic` auth
