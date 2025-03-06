from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Webhook endpoint to receive payment confirmation from UPI API
@app.route("/payment-webhook", methods=["POST"])
def payment_webhook():
    data = request.json
    print(f"Received payment update: {data}")
    return jsonify({"message": "Acknowledged"}), 200

# Simulating a payment request from Payer App
@app.route("/make-payment", methods=["POST"])
def make_payment():
    upi_api_url = "http://127.0.0.1:5001/payment"
    txn_id = "txn_123456"
    payer_webhook = "http://127.0.0.1:5000/payment-webhook"  # This app's webhook
    
    payload = {"txn_id": txn_id, "payer_webhook": payer_webhook}
    
    response = requests.post(upi_api_url, json=payload)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(port=5000, debug=True)
