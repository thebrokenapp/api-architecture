## Send Message Function

### Install Sqlite3
We will use `sqlite3` database to store message information
```bash
sudo apt install sqlite3
```

Check if it's installed
```bash
sqlite3 --version
```


### Create messages table
#### Create a database
```bash
sqlite3 messaging.db
```

#### Create messages table
```sql
CREATE TABLE messages (
    message_from TEXT,
    message_to TEXT,
    message_text TEXT,
    status TEXT,
    message_time TEXT
);
```

#### Add import statements
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from datetime import datetime
import sqlite3
```

#### DB Connection Logic
```python
def get_db_connection():
    conn = sqlite3.connect('messaging.db')    # This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn
```


#### Add DB connection logic to your python file
```python
def send_message(message_from, message_to, message_text):
    status = "success"
    message_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    cursor.execute('''INSERT INTO messages (message_from, message_to, message_text, status, message_time) VALUES (?, ?, ?,?, ?)''',
    (message_from, message_to, message_text, status, message_time))
    conn.commit()
    conn.close()
    return {"txn_status": status, "send_time": message_time, "notes": "message has been sent to " + message_to}
```

#### Note
```python
First difference you should note that this function accepts three parameters: `message_from`, `message_to` and `message_text`.
Also, the order of these parameters are importanct!
```

#### Register the function that you want to expose as API
```python
server.register_function(send_message)
```

#### Final Code
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from datetime import datetime
import sqlite3

# Function to connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('messaging.db')    # This opens the connection to the database.
    conn.row_factory = sqlite3.Row  # Allow fetching rows as dictionaries
    return conn



def api_status():
    # do some checks
    return { "notes": "RPC API is up!"}

def send_message(message_from, message_to, message_text):
    status = "success"
    message_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    cursor.execute('''INSERT INTO messages (message_from, message_to, message_text, status, message_time) VALUES (?, ?, ?,?, ?)''',
    (message_from, message_to, message_text, status, message_time))
    conn.commit()
    conn.close()
    return {"txn_status": status, "send_time": message_time, "notes": "message has been sent to " + message_to}

host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
server.register_function(send_message)
print("Started RCPC Server!")
server.serve_forever()
```

### Launch your API
```bash
python messaging.py
```

### Test using Postman
```http
POST http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method`  | `string` | **Required**. (apiStatus)   |
| `params`  | `list`   | **Required**. [message_from, message_to, message_text]  |
| `id    `  | `string` or `int` | **Required**      |
