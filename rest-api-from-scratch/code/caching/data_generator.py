import csv
import random
from datetime import datetime, timedelta
import uuid

csv_file_path = 'payments.csv'
status_options = ['initiated', 'completed', 'pending', 'failed']

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['transaction_id', 'amount', 'status', 'payer_upi', 'payee_upi', 'note', 'timestamp'])
    
    for i in range(1, 50001):
        transaction_id = str(uuid.uuid4())
        amount = f"{random.uniform(10.0, 1000.0):.2f}"
        status = random.choice(status_options)
        payer_upi = f"payer{i}@upi"
        payee_upi = f"payee{i}@upi"
        note = f"Payment {i} for services"
        timestamp = str(datetime.utcnow())
        
        writer.writerow([transaction_id, amount, status, payer_upi, payee_upi, note, timestamp])
