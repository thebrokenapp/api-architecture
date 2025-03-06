from flask import Flask, request, jsonify
import threading
import time
import requests
import random
app = Flask(__name__)

# Simulated transaction processing function
def process_transaction(txn_id, payer_webhook):
    sleep_time = random.uniform(0.5, 1.0)
    time.sleep(sleep_time)  # Simulating processing delay (async behavior)
    transaction_status = {"txn_id": txn_id, "status": "SUCCESS"}
    
    # Call the Payer App's webhook to notify completion
    try:
        requests.post(payer_webhook, json=transaction_status, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Error notifying payer app: {e}")

@app.route("/payment", methods=["POST"])
def initiate_payment():
    data = request.json
    txn_id = data.get("txn_id")
    payer_webhook = "http://127.0.0.1:5002/payment-webhook"  # Webhook to notify payer app
    
    # Send immediate acknowledgment
    ack_response = {"txn_id": txn_id, "status": "ACCEPTED"}
    
    # Process the transaction asynchronously
    threading.Thread(target=process_transaction, args=(txn_id, payer_webhook)).start()

    return jsonify(ack_response), 202

if __name__ == "__main__":
    app.run(port=5001, debug=True)
