from flask import Flask, request, jsonify, Response
from pydantic import BaseModel, Field, UUID4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import logging
import random
from flask_httpauth import HTTPBasicAuth
from functools import wraps


# Initialize Flask app and auth
app = Flask(__name__)
auth = HTTPBasicAuth()

# Token store (In-memory for this example)
token_store = {}
# In-memory databases
users_database = {}
payments = []


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



# Set up logging configuration
logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
audit_logger = logging.getLogger('audit')



# Pydantic Models
class Payment(BaseModel):
    amount: int
    payer_upi: str
    payee_upi: str
    note: str = ''

    class Config:
        extra = "forbid"

class SignUp(BaseModel):
    username: str
    password: str
    mobile: str

    class Config:
        extra = "forbid"

# Authentication logic
@auth.verify_password
def verify_password(username, password):
    if username in users_database and check_password_hash(users_database.get(username), password):
        return username

# Before request hook
@app.before_request
def before_request():
    # You can log every incoming request here (for audit, debugging, etc.)
    request.guid = str(uuid.uuid4())  # Store GUID in the request object
    audit_logger.info(f"Request GUID: {request.guid} - Incoming request: {request.method} {request.path}")

# After request hook
@app.after_request
def after_request(response):
    # You can log the response or modify it here (e.g., log status codes, modify headers)
    response.headers['X-Request-GUID'] = request.guid    # Add GUID to the response headers
    audit_logger.info(f"Response GUID: {request.guid} - Response: {response.status_code} for {request.method} {request.path}")
    return response


# Status route
@app.route('/apiStatus')
@token_required
def status(username):
    return {"message": "API is up!, " + username}

# Create a new payment
@app.route('/payments', methods=["POST"])
@token_required
def initiatePayment(username):
    body = request.get_json()
    txn_id = str(uuid.uuid4())
    current_timestamp = datetime.utcnow()
    data["status"] = "initiated"
    data["transaction_id"] = txn_id
    data["timestamp"] = current_timestamp
    payments.append(data)

    # Audit log
    audit_logger.info(f"Payment initiated: {data}")

    return jsonify(data)

# Get all payments
@app.route('/payments', methods=["GET"])
def getPayments():
    return jsonify({"data": payments})

# Update a payment
@app.route('/payments/<transaction_id>', methods=["PUT"])
def updatePayment(transaction_id):
    data = request.get_json()
    for payment in payments:
        if payment["transaction_id"] == transaction_id:
            payment.update(data)

            # Audit log
            audit_logger.info(f"Payment updated: {payment}")

            return jsonify(payment)

    return jsonify({"message": "Transaction not found"}), 404

# Delete a payment
@app.route('/payments/<transaction_id>', methods=["DELETE"])
def deletePayment(transaction_id):
    for index, payment in enumerate(payments):
        if payment["transaction_id"] == transaction_id:
            payments.pop(index)

            # Audit log
            audit_logger.info(f"Payment deleted: {transaction_id}")

            return Response({"message": "Resource deleted!"}, status=204)

    return jsonify({"message": "Transaction not found"}), 404

# User Sign-Up
@app.route('/signUp', methods=["POST"])
def signUp():
    data = request.get_json()
    username = data["user_name"]
    password = data["password"]
    hashed_password = generate_password_hash(password)

    users_database[username] = hashed_password

    # Audit log
    audit_logger.info(f"User signed up: {username}")

    return jsonify({"message": "User created"})

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


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)
