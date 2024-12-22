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
    
    # Store the token in the token store
    token_store[token] = username
    return jsonify({"token": token}), 200
```

#### Protect the routes behind @token_required decorator
```python
# Status route
@app.route('/apiStatus')
@token_required
def status(username):
    return {"message": "API is up!, " + username}
```

#### Add token_required function
```python
# A simple decorator to check token in the request
# custom decorator must return a function
def token_required(f):
    @wraps(f)
    def wrapper():
        try:
            token = request.headers.get('Authorization').split("Bearer ")[1]
            print("From header: ", token)
            if not token or token not in token_store:
                return {"msg": "No token provided"}, 401
                #abort(401, description="Unauthorized: Invalid or missing token")

            # Optional: You can access user info from token
            username = token_store[token]

            return f(username)
        except:
            return {"msg": "No token provided"}, 401
    return wrapper
```
