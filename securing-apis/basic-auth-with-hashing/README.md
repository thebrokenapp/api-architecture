# Hash Password 

#### Import Library
```python
from werkzeug.security import generate_password_hash, check_password_hash
```

#### Create an empty users DB
```
users = dict()
```

#### Add password checking logic
```python
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
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
	
	users[request_user_name] = hashed_password
	
	print(users)				
 
	return {"message":"User created"}
```
