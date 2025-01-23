import redis
import json
import random

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Subscribe to the payment channel
pubsub = redis_client.pubsub()
pubsub.subscribe("initiate_payment_channel")

print("Listening for payment messages...")

# Listen for messages and process them
for message in pubsub.listen():
    if message['type'] == 'message':
        # Parse the message data
        payment_data = json.loads(message['data'])
        # Randomly decide if it's fraud or not
        if random.choice([True, False]):
            fraud_status = "fraud"
        else:
            fraud_status = "not fraud"
        
        # Print the result
        print("Payment ID:", payment_data['transaction_id'], " Status:", fraud_status)
