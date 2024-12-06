from flask import Flask, request, jsonify
import sqlite3
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/likes', methods=['POST'])
def add_like():
    data = request.get_json()
    channel = "likes-channel"
    redis_client.publish(channel, str(data))

    return jsonify({"message": "Like added successfully"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8001, debug=True)
