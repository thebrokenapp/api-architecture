from flask import Flask, request, jsonify, Response
from pydantic import BaseModel, Field, UUID4
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
import logging
import random
from flask_httpauth import HTTPBasicAuth

# Initialize Flask app and auth
app = Flask(__name__)
auth = HTTPBasicAuth()

# Set up logging configuration
logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
audit_logger = logging.getLogger('audit')

# In-memory databases
users_database = {}
payments = []

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

# Routes

# Status route
@app.route('/apiStatus')
@auth.login_required
def status():
    return {"message": "API is up!"}

# Create a new payment
@app.route('/payments', methods=["POST"])
@auth.login_required
def initiatePayment():
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
@auth.login_required
def getPayments():
    return jsonify({"data": payments})

# Update a payment
@app.route('/payments/<transaction_id>', methods=["PUT"])
@auth.login_required
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
@auth.login_required
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

# Random path for testing
@app.route('/random', methods=["GET"])
def random_path():
    number = random.randint(1, 10)
    if number < 3:
        return jsonify({"message": "Sending 201"}), 201
    if number == 4:
        return jsonify({"message": "Sending 201"}), 403
    if number >= 5:
        return jsonify({"message": "Sending 201"}), 500
    else:
        return jsonify({"message": "Sending 201"}), 204

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)