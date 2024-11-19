from locust import HttpUser, task, between
import random

class LoadTestUser(HttpUser):
    # Simulates a wait time between each request (in seconds)
    wait_time = between(0.1, 0.5)
    transaction_ids = []  # List to store transaction IDs


    @task(1)  # Weight of this task compared to others
    def get_payments(self):
        self.client.get("/payments")

    @task(1)  # Weight of this task compared to others
    def get_apistatus(self):
        self.client.get("/apiStatus")

    @task(2)  # Runs this task twice as often as get_payments
    def create_payment(self):
        response = self.client.post("/payments", json={
            "amount": random.randint(1000, 5000),
            "note": "Books",
            "payee_upi": "qwe-sbi",
            "payer_upi": "abx@okhdfc"
        })

        if response.status_code == 200:  # Assuming 201 is the success status
            # Extract transaction_id from the response
            transaction_id = response.json().get("transaction_id")
            if transaction_id:
                self.transaction_ids.append(transaction_id)
                print(f"Created transaction: {transaction_id}")
        else:
            print(f"Failed to create payment: {response.status_code}, {response.text}")

    @task(1)  # Weight for deleting payments
    def delete_payment(self):
        if self.transaction_ids:
            # Randomly pick a transaction ID to delete
            transaction_id = random.choice(self.transaction_ids)
            
            # Send DELETE request
            response = self.client.delete(f"/payments/{transaction_id}")
            
            if response.status_code == 204:
                print(f"Successfully deleted transaction: {transaction_id}")
                self.transaction_ids.remove(transaction_id)  # Remove from list after successful deletion
            elif response.status_code == 404:
                print(f"Transaction {transaction_id} not found")
            else:
                print(f"Unexpected response: {response.status_code}")
        else:
            print("No transactions available to delete.")

    @task(1)  # Weight for deleting payments
    def get_single_payment(self):
        if self.transaction_ids:
            # Randomly pick a transaction ID to delete
            transaction_id = random.choice(self.transaction_ids)
            
            # Send DELETE request
            response = self.client.get(f"/payments/{transaction_id}")
            
            if response.status_code == 200:
                print(f"Successfully fetched transaction: {transaction_id}")
            else:
                print(f"Unexpected response: {response.status_code}")
        else:
            print("No transactions available to fetch")

# locust -f locustfile.py --host=http://127.0.0.1:5000 --web-host=127.0.0.1 --web-port=8080
