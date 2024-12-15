import redis
import json
import sqlite3

# Redis Pub/Sub Setup
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = redis_client.pubsub()


pubsub.subscribe('new_post_channel')  # Subscribe to the relevant channel

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])  # Parse the JSON data
                # Extract post_id and interaction_type
        user_id = data.get('user_id')
        interaction_type = data.get('interaction_type')
        
        # Check if the interaction type is 'like'
        if interaction_type == 'like':
            print(f"User {user_id} has liked your post!")


