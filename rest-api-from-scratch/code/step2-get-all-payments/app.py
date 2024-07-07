from flask import Flask

app = Flask(__name__)

@app.route('/apiStatus')
def status():
	return {"message": "API is running!"}

payments = []

@app.route('/payments')
def getPayments():
	return {"payments": payments}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port= 5000, debug=True)
