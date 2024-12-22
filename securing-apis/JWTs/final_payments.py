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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import logging
import base64
from functools import wraps
import jwt
import datetime


r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
audit_logger = logging.getLogger('audit')
# Disable the defaul INFO level logging from Flask
# by setting Flask level logging to WARNING
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)


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
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200000 per day", "50000 per hour"],
    storage_uri="redis://localhost:6379/0",
)




app.config['SECRET_KEY'] = 'your_secret_key'




PrometheusMetrics(app)



@auth.verify_password
def verify_password(username, password):
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT hashed_password FROM users WHERE user_name = ?', (username,))
	password_row = cursor.fetchone()
	if password_row is None:
		return None
	retrieved_password = password_row["hashed_password"]
	conn.close()
	if check_password_hash(retrieved_password, password):
		return username


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

# After request hook
@app.after_request
def after_request(response):
	# You can log the response or modify it here (e.g., log status codes, modify headers)
	#response.headers['X-Request-GUID'] = request.guid    # Add GUID to the response headers
	audit_logger.info(f"Response -> User: {request.username} | Response GUID: {request.guid} | Result: {response.status_code}")
	return response


token_store = dict()


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
            return jsonify({"msg": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Invalid token"}), 401
    return wrapper


# Login route to authenticate and generate a token
@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    username = auth.current_user()  # Get the authenticated username
    # Generate a token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    token = jwt.encode({'username': username, 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200



@app.route('/user', methods=["POST"])
def sign_up():
	data = request.get_json()				
	request_user_name= data["user_name"]
	request_password = data["password"]
	hashed_password = generate_password_hash(request_password)
	
	conn = get_db_connection()	# use the function defined above to get a connection to DB
	cursor = conn.cursor()		# # Creates a cursor object to interact with the database.
	cursor.execute('''INSERT INTO users (user_name, hashed_password) VALUES (?, ?)''',(request_user_name, hashed_password))
	conn.commit()
	conn.close()
	#users[request_user_name] = hashed_password
	return {"message":"User created"}






@app.route('/apiStatus', methods=['GET'])
@limiter.limit("8000 per day")
@auth.login_required
def api_status():
	print("User is: ", auth.current_user())
	return {"message": "API is up!"}


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
	app.run(host="0.0.0.0", port= 8000, ssl_context=('server.crt', 'server.key'))
