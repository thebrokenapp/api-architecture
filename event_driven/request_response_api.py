from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/likes', methods=['POST'])
def add_like():
    data = request.get_json()
    post_id = data.get('post_id')
    interaction_type = data.get('interaction_type')
    user_id = data.get('user_id')

    if not post_id or not interaction_type or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    # Connect to database
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Insert interaction
    cursor.execute("""
    INSERT INTO interactions (post_id, interaction_type, interaction_by, timestamp)
    VALUES (?, ?, ?, datetime('now'))
    """, (post_id, interaction_type, user_id))

    # Get post details
    cursor.execute("SELECT likes, popularity_score FROM posts WHERE post_id = ?", (post_id,))
    post = cursor.fetchone()

    if not post:
        connection.close()
        return jsonify({"error": "Post not found"}), 404

    likes, popularity_score = post
    new_likes = likes + 1
    new_popularity_score = popularity_score + 1.0

    # Update post details
    cursor.execute("""
    UPDATE posts
    SET likes = ?, popularity_score = ?
    WHERE post_id = ?
    """, (new_likes, new_popularity_score, post_id))

    connection.commit()
    connection.close()

    return jsonify({"message": "Like added successfully", "likes": new_likes, "popularity_score": new_popularity_score}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8000, debug=True)
