from locust import HttpUser, task, between, events
from flask import Flask, request, jsonify
import random
import threading
import time
import uuid
import time
# Create a Flask webhook server inside Locust to capture async UPI responses
webhook_app = Flask(__name__)
received_transactions = {}
payment_initiated = 0
webhooks_received = 0
total_delay = 0
transaction_start_ts = {}
@webhook_app.route("/payment-webhook", methods=["POST"])
def payment_webhook():
    """Receives transaction status updates from UPI API."""
    data = request.json
    txn_id = data.get("txn_id")
    status = data.get("status")
    global webhooks_received
    global total_delay
    if txn_id:
        start_ts = transaction_start_ts[txn_id]
        current_ts = int(time.time() * 1000)
        delay = current_ts - start_ts
        total_delay += delay
        webhooks_received += 1
        print(f"Webhook received: {txn_id} -> {status}")
    
    return jsonify({"message": "Webhook received"}), 200

# Run webhook server in a separate thread
def run_webhook_server():
    webhook_app.run(port=5002, debug=False, use_reloader=False)

threading.Thread(target=run_webhook_server, daemon=True).start()

#Load Test User for UPI API
class LoadTestUser(HttpUser):
    wait_time = between(0.001, 0.005)

    @task(1)
    def create_payment(self):
        """Simulate payment initiation request to the UPI API"""
        txn_id = str(uuid.uuid4()) 
        #global payment_initiated
        response = self.client.post("/payment", json={
            "txn_id": txn_id
        })

        if response.status_code == 202:  # Accepted but processing async
            global payment_initiated
            payment_initiated += 1
            transaction_start_ts[txn_id] = int(time.time() * 1000)
            print(f"Sent transaction: {txn_id}")
        else:
            print(f"Failed to create payment: {response.status_code}, {response.text}")

    @task(1)
    def check_webhook_responses(self):
        print("Payments Accepted", payment_initiated)
        print("Payments complete", webhooks_received)

# Hook to Stop Locust When Done
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Prints summary after test stops"""
    print("Payments Accepted: ", payment_initiated)
    print("Payments complete: ", webhooks_received)
    print("Avg Latency in millisec: ", total_delay/webhooks_received)
