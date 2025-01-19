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


def create_group(group_name):
    status = "success"
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    try:
        # Attempt to insert the new group
        cursor.execute('''INSERT INTO groups (group_name, create_date) VALUES (?, ?)''',(group_name, create_date))
        conn.commit()
        return {"txn_status": "success", "txn_timestamp": create_date, "notes": "group is created with name: " + group_name}
    except sqlite3.IntegrityError:
        # Handle the case where the group already exists
        return {"txn_status": "failed", "txn_timestamp": create_date, "notes": "group already exists: " + group_name}


host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
server.register_function(send_message)
server.register_function(create_group)
print("Started RCPC Server!")
server.serve_forever()
