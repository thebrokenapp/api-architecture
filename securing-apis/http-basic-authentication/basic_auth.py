from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "ankit": "my_password",
    "kumar": "12345"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username) == password):
        return username

@app.route('/checkBalance')
@auth.login_required
def check_balance():
    print(request.headers)
    return {"message": "Your balance is Rs 500"}
    #return "Hello, {}! API is up!".format(auth.current_user())

@app.route('/apiStatus')
def apiStatus():
    return {"message": "API is up!"}


if __name__ == '__main__':
    app.run(host="127.0.0.1", port= 5000)

# Try in POSTMAN
# 1. Try requesting in a regualar way: you will get error
# 2. Go to "Authorization Tab" and add username password
# Note: Dont add username password in header. That work is done by POSTMAN
