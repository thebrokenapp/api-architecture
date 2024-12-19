from flask import Flask, request, jsonify, Response
from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import redis
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import base64
#from prometheus_flask_exporter import PrometheusMetrics

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)



# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('upi.db')	# This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn





payments = []
users = dict()



class PaymentBody(BaseModel):
	amount : int = Field(gt=0, lt=1000000)
	payer_upi : str = Field(min_length = 5, max_length= 25)
	payee_upi: str = Field(min_length = 5, max_length= 25)
	note: str = ''

	class Config:
		extra = "forbid"

class Status(BaseModel):
	status: str



app = Flask(__name__)
auth = HTTPBasicAuth()
PrometheusMetrics(app)



users = {}



@auth.verify_password
def verify_password(username, password):
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT hashed_password FROM users WHERE user_name = ?', (username,))
	password_row = cursor.fetchone()
	retrieved_password = password_row["hashed_password"]
	print("password from sqlite3:",retrieved_password)
	print("password from Auth header", password)
	conn.close()
	if check_password_hash(retrieved_password, password):
		return username




def get_username():
    # Assuming the username is sent in the 'X-Username' header
    username = request.headers.get("X-Username")
    if not username:
        # If no username is provided, use IP
        return request.remote_addr
    return username




limiter = Limiter(
    key_func=get_username,
    app=app,
    default_limits=["200 per day", "50 per minute", "20 per second"],
    storage_uri="redis://localhost:6379/0",
)


# Set up logging configuration
logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
audit_logger = logging.getLogger('audit')

# Before request hook
@app.before_request
def before_request():
    # You can log every incoming request here (for audit, debugging, etc.)
    auth_header = request.headers.get('Authorization')
    request.username = "anonymous"
    if auth_header and auth_header.startswith('Basic '):
	    encoded_credentials = auth_header.split(' ')[1]
	    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
	    request.username, _ = decoded_credentials.split(':', 1)

    request.guid = str(uuid.uuid4())  # Store GUID in the request object
    audit_logger.info(f"User: {request.username} Request GUID: {request.guid} - Incoming request: {request.method} {request.path}")

# After request hook
@app.after_request
def after_request(response):
    try:
        # You can log the response or modify it here (e.g., log status codes, modify headers)
        response.headers['X-Request-GUID'] = request.guid    # Add GUID to the response headers
        audit_logger.info(f"User: {request.username} Response GUID: {request.guid} - Response: {response.status_code} for {request.method} {request.path}")
    except:
    	print("After request exception occured")
    return response









@app.route('/user', methods=["POST"])
def sign_up():
	data = request.get_json()				
	request_user_name= data["user_name"]
	request_password = data["password"]
	hashed_password = generate_password_hash(request_password)
	print(request_user_name, hashed_password)
	try:
		conn = get_db_connection()	# use the function defined above to get a connection to DB
		cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
		cursor.execute('''INSERT INTO users (user_name, hashed_password) VALUES (?, ?)''',(request_user_name, hashed_password))
		conn.commit()
		conn.close()
	except sqlite3.IntegrityError as e:
		return jsonify({"error": "Username already exists!"}), 400
	
	return {"message":"User created"},201



@app.route('/apiStatus', methods=['GET'])
@limiter.limit("5 per day")
@auth.login_required
def api_status():
	return {"message": "API is up!"}


@app.route('/payments', methods=['GET'])
@auth.login_required
def get_all_payments():
	status = request.args.get('status')
	if status is not None:
		return_list = []
		for txn in payments:
			if txn["status"] == status:
				return_list.append(txn)
		return {"transactions": return_list}

	return {"transactions": payments}


@app.route('/payments', methods=['POST'])
@validate()
def initiate_payment(body: PaymentBody):
	data = request.get_json()
	amount = data.get("amount")
	payer_upi = data.get("payer_upi")
	payee_upi = data.get("payee_upi")
	note = data.get("note")				
	transaction_id = str(uuid.uuid4())		
	timestamp = datetime.utcnow()			
	status = "initiated"
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO payments (transaction_id, amount, status, payer_upi, payee_upi, note, timestamp) VALUES (?, ?, ?,?, ?, ?,?)''',
	(transaction_id, amount, status, payer_upi, payee_upi, note, timestamp))
	conn.commit()
	conn.close()
 
	return {"message": "transaction created", "transaction_id": transaction_id},201


@app.route('/payments/<transaction_id>', methods=['GET'])
@validate()
def getPayment(transaction_id: UUID4):
	redis_key = str(transaction_id)

	cache_data = r.hgetall(redis_key)

	if cache_data:
		print("data came from redis")
		return jsonify(cache_data)
	else:
		print("data came from sqlite3")
		conn = get_db_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM payments WHERE transaction_id = ?', (str(transaction_id),))
		payment = cursor.fetchone()
		conn.close()
		if payment is None:
			return {"message": "Transaction not found"}, 404

		r.hset(redis_key, mapping = dict(payment))

	return dict(payment)



@app.route('/payments/<transaction_id>', methods = ["PATCH"])
@validate()
def updatePayment(transaction_id: UUID4, body: Status):
	data = request.get_json()
	status = data.get("status")
	transaction_id = str(transaction_id)
	timestamp = datetime.utcnow()							
	
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('''UPDATE payments SET status = ?, timestamp = ? WHERE transaction_id = ? ''', (status, timestamp, transaction_id))
	conn.commit()
	conn.close()

	if cursor.rowcount == 0:
		#conn.close()
		return jsonify({"message": "Transaction not found"}),404


	r.delete(transaction_id)
	return jsonify({"message": "Transaction updated"})


@app.route('/payments/<transaction_id>', methods = ["DELETE"])
def deletePayment(transaction_id):
	conn = get_db_connection()
	cursor = conn.cursor()

	cursor.execute('''DELETE FROM payments WHERE transaction_id = ?''', (transaction_id,))

	if cursor.rowcount == 0:
		conn.close()
		return jsonify({"message": "Transaction not found"}),404

	conn.commit()
	conn.close()

	return jsonify({"message": "Transaction deleted!"})




if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8000,debug=True)
