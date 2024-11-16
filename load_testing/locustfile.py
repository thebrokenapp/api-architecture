from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    # Simulates a wait time between each request (in seconds)
    wait_time = between(1, 5)

    @task(1)  # Weight of this task compared to others
    def get_payments(self):
        self.client.get("/payments")

    @task(2)  # Runs this task twice as often as get_payments
    def create_payment(self):
        self.client.post("/payments", json={
            "amount": 12000,
            "note": "Books",
            "payee_upi": "qwe-sbi",
            "payer_upi": "abx@okhdfc"
        })
