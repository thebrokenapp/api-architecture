## Standalone JWT Demo
#### Install dependencies
```bash
pip install PyJWT
```

#### Update the `generate_jwt.py` file with the expiry timestamp
#### Run the code
```bash
python generate_jwt.py
```

## Add JWT logic to your Payments API

#### Import required dependencies
```python
import jwt
import datetime
```

#### Add secrte key
```python
app.config['SECRET_KEY'] = "mysecretkey"
```


#### Update your `/login` route
Note how we have removed the logic to store token in Redis.
This is the idea of stateless token (we dont store token on the server side at all)
```python
app.config['SECRET_KEY'] = 'your_secret_key'   # this is the key that will be used to generate hash

@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    username = auth.current_user()  # Get the authenticated username
    # Generate a token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    token = jwt.encode({'username': username, 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm='HS256')
    return {'token': token}, 200
```


#### Update your `token_required` decorator
```python
def token_required(f):
    @wraps(f)
    def wrapper():
        try:
            token = request.headers.get('Authorization')
            if not token:
            	return {"msg": "No token provided"}, 401

            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            username = decoded_token['username']
            return f(username)
        except jwt.ExpiredSignatureError:
            return {"msg": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"msg": "Invalid token"}, 401
    return wrapper
```
