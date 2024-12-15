import redis
import json
import sqlite3

# Redis Pub/Sub Setup
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = redis_client.pubsub()

# Function to update like count in SQLite
def update_like_count(post_id):
    # Connect to SQLite database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    # Increment the likes count by 1
    cursor.execute('''UPDATE posts SET likes = likes + 1 WHERE post_id = ?;''', (post_id,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()


pubsub.subscribe('new_post_channel')  # Subscribe to the relevant channel

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])  # Parse the JSON data
                # Extract post_id and interaction_type
        post_id = data.get('post_id')
        interaction_type = data.get('interaction_type')
        
        # Check if the interaction type is 'like'
        if interaction_type == 'like':

            update_like_count(post_id)  # Update like count in the database
            print(f"Post {post_id} like count incremented.")


