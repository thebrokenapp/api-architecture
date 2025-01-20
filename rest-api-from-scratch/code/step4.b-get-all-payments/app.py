from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments/<user_name>')
def getPayments(user_name):
	payment_list = []
	for payment in payments:
		if payment["user_name"] == user_name:
			payment_list.append(payment)
	return {"payments": payment_list}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
