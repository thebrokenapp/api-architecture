# Keep-Alive in Flask REST API

This repository demonstrates how to implement **Keep-Alive** in a Flask REST API and how a Python client can maintain a persistent connection.

## How Keep-Alive Works

### Server Responsibilities:
- The server decides whether to keep the connection open.
- It sends `Connection: keep-alive` and `Keep-Alive: timeout=X` headers.
- If no new request is received within `X` seconds, the server closes the connection.

### Client Responsibilities:
- The client must reuse the same connection (e.g., using `requests.Session()` in Python).
- If the client explicitly closes the connection, Keep-Alive is ineffective.

### Who Controls Keep-Alive?
- The **server** ultimately controls the timeout and whether to close the connection.
- The **client** can try to reuse the connection but cannot force the server to keep it open beyond the timeout.

## Flask API with Keep-Alive (5 Seconds)

Create a `app.py` file with the following Flask API:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/keep-alive', methods=['GET'])
def keep_alive():
    response = jsonify({"message": "Connection is kept alive for 5 seconds"})
    response.headers['Connection'] = 'keep-alive'
    response.headers['Keep-Alive'] = 'timeout=5'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Python Client with Keep-Alive Support

Create a `client.py` file to send multiple requests using persistent connections:

```python
import requests
import time

session = requests.Session()  # Maintains a persistent connection

url = "http://127.0.0.1:5000/keep-alive"

# Send multiple requests to test Keep-Alive
for i in range(3):
    response = session.get(url)
    print(f"Response {i+1}: {response.json()}")
    time.sleep(3)  # Sleep less than 5 seconds to keep the connection alive

session.close()  # Close session explicitly
```

## Expected Behavior
- The Flask API responds with `Keep-Alive: timeout=5`, keeping the connection alive for **5 seconds**.
- The Python client sends **3 requests, 3 seconds apart**, ensuring the connection remains active.
- If a request is made **after 5 seconds**, the server will close the connection, and a new one will be created.

## Running the Code

1. **Start the Flask API:**
   ```sh
   python app.py
   ```

2. **Run the Client:**
   ```sh
   python client.py
   ```

This will test the Keep-Alive behavior between the client and the Flask API.

## Notes
- This example uses Flask's built-in server (Werkzeug), which is not optimized for production.
- For production, use **Gunicorn** or **Nginx** to manage Keep-Alive settings.

Would you like help configuring Keep-Alive for a production server?

