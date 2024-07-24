from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "ankit": generate_password_hash("my_password"),
    "kumar": generate_password_hash("12345")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/apiStatus')
@auth.login_required
def index():
    print(request.headers)
    return {"message": "API is up!"}
    #return "Hello, {}! API is up!".format(auth.current_user())

@app.route('/noAuth')
def noAuth():
    return {"message": "API is up!"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port= 5000)

# Try in POSTMAN
# 1. Try requesting in a regualar way: you will get error
# 2. Go to "Authorization Tab" and add username password
# Note: Dont add username password in header. That work is done by POSTMAN
