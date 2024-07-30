from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a more secure secret key

# Sample user credentials
users_db = {
    "ankit": "password"  # Example user, 'user' with password 'password'
}

@app.route('/token', methods=['POST'])
def get_token():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate username and password
    if username in users_db and users_db[username] == password:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing!'}), 403

    try:
        token = token.split(" ")[1]
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return jsonify({'message': f'Welcome {data["username"]}, you have access to this protected route!'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 403

if __name__ == '__main__':
    app.run(debug=True)
