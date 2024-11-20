## Basic Auth in our Payments API

Install the required library
```bash
pip install Flask-HTTPAuth
```

Import the required library
```python
from flask_httpauth import HTTPBasicAuth
```

Add the Auth feature in your app
```python
app = Flask(__name__)
auth = HTTPBasicAuth()
```

Add the password verification function
```python
@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username)== password:
        return username
```

Protect all your routes behind password except /signUp
```python
@app.route('/apiStatus')
@auth.login_required
def status():
	return {"message": "API is up!"}


@app.route('/payments', methods=["GET"])
@auth.login_required
def getPayments():
	return {"data": payments}

```
