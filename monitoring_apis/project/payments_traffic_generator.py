import requests
import uuid
import random
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8001"

# Generate traffic for /apiStatus
def check_api_status():
    response = requests.get(f"{BASE_URL}/apiStatus")
    print("/apiStatus", response.status_code, response.json())

# Generate traffic for GET /payments
def get_all_payments():
    status = random.choice([None, "initiated", "completed", "failed"])
    params = {"status": status} if status else {}
    response = requests.get(f"{BASE_URL}/payments", params=params)
    print("/payments [GET]", response.status_code, response.json())

# Generate traffic for POST /payments
def create_payment():
    payload = {
        "amount": random.randint(1, 10000),
        "payer_upi": f"payer{random.randint(1, 100)}@upi",
        "payee_upi": f"payee{random.randint(1, 100)}@upi",
        "note": f"Payment for {random.choice(['groceries', 'rent', 'utilities'])}"
    }
    response = requests.post(f"{BASE_URL}/payments", json=payload)
    print("/payments [POST]", response.status_code, response.json())
    return response.json().get("transaction_id")

# Generate traffic for GET /payments/<transaction_id>
def get_payment(transaction_id):
    response = requests.get(f"{BASE_URL}/payments/{transaction_id}")
    print(f"/payments/{transaction_id} [GET]", response.status_code, response.json())

# Generate traffic for PATCH /payments/<transaction_id>
def update_payment(transaction_id):
    payload = {"status": random.choice(["completed", "failed"])}
    response = requests.patch(f"{BASE_URL}/payments/{transaction_id}", json=payload)
    print(f"/payments/{transaction_id} [PATCH]", response.status_code, response.json())

# Generate traffic for DELETE /payments/<transaction_id>
def delete_payment(transaction_id):
    response = requests.delete(f"{BASE_URL}/payments/{transaction_id}")
    print(f"/payments/{transaction_id} [DELETE]", response.status_code, response.json())

# Main traffic generator
def generate_traffic():
    check_api_status()

    for _ in range(random.randint(1, 5)):
        get_all_payments()

    transaction_ids = []

    for _ in range(random.randint(5, 10)):
        transaction_id = create_payment()
        if transaction_id:
            transaction_ids.append(transaction_id)

    for transaction_id in transaction_ids:
        get_payment(transaction_id)

    for transaction_id in transaction_ids[:5]:
        update_payment(transaction_id)

    for transaction_id in transaction_ids[5:]:
        delete_payment(transaction_id)

while True:
    generate_traffic()
    time.sleep(random.randint(1, 10))  # Adjust the sleep time as needed
