from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, UUID4
from flask_pydantic import validate

app = Flask(__name__)
payments_db = []

class PaymentBody(BaseModel):
	user_name: str
	amount : int = Field(gt=0, lt=100000)
	payer_upi : str = Field(min_length=8, max_length=20)
	payee_upi: str = Field(min_length=8, max_length=20)
	note: str = ''
	class Config:
		extra = "forbid"


class UpdatePaymentBody(BaseModel):
	status: str
	class Config:
		extra = "forbid"

class UserNameModel(BaseModel):
    user_name: str = Field(..., min_length=10, max_length=20)

@app.route('/apiStatus', methods=["GET"])
def api_status():
	return {"message": "Payments API is up!"}


@app.route('/payments', methods=["POST"])
@validate()
def initiate_payment(body:PaymentBody):
	request_data = request.get_json()

	transaction_id = str(uuid.uuid4())
	status = "initiated"
	timestamp = datetime.utcnow()

	request_data["txn_id"] = transaction_id
	request_data["status"] = status
	request_data["txn_time"] = timestamp

	payments_db.append(request_data)

	return {"txn_id": transaction_id, "status": status, "txn_time": timestamp, "message": "Payment initiated" }


@app.route('/payments/<txn_id>', methods=["PATCH"])
@validate()
def update_payment(body: UpdatePaymentBody,txn_id: UUID4):
	request_data = request.get_json()
	timestamp = datetime.utcnow()

	for payment in payments_db:
		if txn_id == payment["txn_id"]:
			payment["status"] = request_data.get("status")
			payment["timestamp"] = timestamp

			return {"message": "Transaction updated", "txn_id": txn_id}

	return {"message": "Transaction not found"},404



@app.route('/payments/<txn_id>', methods=["DELETE"])
def delete_payment(txn_id):
	for index, payment in enumerate(payments_db):
		if payment["txn_id"] == txn_id:
			payments_db.pop(index)
			return {"message": "Transaction id deleted"}

	return {"message": "Transaction not found"},404




@app.route('/payments/<user_name>', methods=["GET"])
def get_payments_for_one_user(user_name: str):
	status = request.args.get('status','initiated')
	print(status)
	payment_list = []
	for txn in payments_db:
		if user_name == txn["user_name"]:
			if txn["status"] == status:
				payment_list.append(txn)

	return {"payments": payment_list}



@app.route('/payments/transaction/<txn_id>', methods=["GET"])
@validate()
def get_payment_by_txn_id(txn_id: UUID4):
	for payment in payments_db:
		if str(txn_id) == payment["txn_id"]:
			return payment

	return {"message": "Transaction not found"},404


















# Custom error handler for 405
@app.errorhandler(405)
def method_not_allowed_error(error):
	return {"error": "Method Not Allowed!"},405


# Custom error handler for 405
@app.errorhandler(404)
def resource_not_found_error(error):
	return {"error": "Resource Not found!"},404

if __name__ == "__main__":
	app.run(host="0.0.0.0", port= 8001, debug=True)
