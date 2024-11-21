import uuid
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Dummy user data (username: password)
users_db = {
    'Ankit': 'admin123',
    'Piyush': 'user123'
}




# Token store (In-memory for this example)
token_store = {}


# A simple decorator to check token in the request
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization').split("Bearer ")[1]
        print("From header: ", token)
        if not token or token not in token_store:
            abort(401, description="Unauthorized: Invalid or missing token")

        # Optional: You can access user info from token
        username = token_store[token]

        return f(username, *args, **kwargs)
    return wrapper

# Protected route that requires a valid token
@app.route('/dashboard')
@token_required
def dashboard(username):
    return jsonify({"message": "Welcome to your dashboard, " + username})



# Login route to authenticate and generate a token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Check if credentials are valid
    if username in users_db and users_db[username] == password:
        # Generate a token (for simplicity, using a random UUID)
        token = str(uuid.uuid4())
        
        # Store the token in the token store (you could use expiry logic too)
        token_store[token] = username
        print(token_store)
        
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000) 
