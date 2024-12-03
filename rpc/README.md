# Implementing Messaging App via RPCs

## Setup
Make sure python is installed. in your terminal, type `python` or `python3` and see if you get the following output
```bash
terminal$ python
Python 3.10.12 (main, Nov  6 2024, 20:22:13) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Install required libraries
```bash
pip install jsonrpclib
```

## Create a file by the name `whatsapp_rpc.py`

## Function 1: `apiStatus`
### Import RPC libraries
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
```

### Add first route `apiStatus`
```python
def api_status():
    # do some checks
    return { "notes": "API is up!"}
```

### Specify the `host` and `port` on which you want to run the RPC
```python
host = '127.0.0.1'
port = 8000
```

### Create server object
```python
server = SimpleJSONRPCServer((host, port))
```

### Register the function that you want to expose as API
```python
server.register_function(api_status)
```

### Launch RPC API Server
```python
print("Starting server on", host +":"+ str(port))
server.serve_forever()
```

### So far your entire code should look like this
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def api_status():
    # do some checks
    return { "notes": "API is up!"}

host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)

server.serve_forever()
```

### Launch your API
```bash
python whatsapp_rpc.py
```

### Test using Postman
```http
POST http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method`  | `string` | **Required**. (apiStatus)   |
| `params`  | `list`   | []                          |
| `id    `  | `string` or `int` | **Required**      |


## Function 2: `send_message`
### Add one addition import statement
```python
from datetime import datetime
```
### Add second function `send_message()`
```python
def send_message(message_from, message_to, message):
    # do some logic
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"txn_status": status, "send_time": timestamp, "notes": "message has been sent to " + message_to}
```

### Note 
```bash
First difference you should note that this function accepts three parameters: `message_from`, `message_to` and `message`.
Also, the order of these parameters are importanct!
```

### Register the function that you want to expose as API
```python
server.register_function(send_message)
```

### So far your entire code should look like this
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def api_status():
    # do some checks
    return { "notes": "API is up!"}

def send_message(message_from, message_to, message):
    # do some logic
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"txn_status": status, "send_time": timestamp, "notes": "message has been sent to " + message_to}

host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
server.register_function(send_message)
server.serve_forever()
```


### Launch your API
```bash
python whatsapp_rpc.py
```

### Test using Postman
```http
POST http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method`  | `string` | **Required**. (apiStatus)   |
| `params`  | `list`   | [message_from, message_to, message]  |
| `id    `  | `string` or `int` | **Required**      |



## Function 3: `create_group`
### Create a mock database as python dictionary
```python
groups = {}
```

### Add 3rd function `create_group()`
```python
def create_group(group_name, members):
    groups[group_name] = members
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"txn_status": status, "txn_timestamp": timestamp, "notes": "group is created with name: " + group_name}
```


### Register the function that you want to expose as API
```python
server.register_function(create_group)
```

### Launch your API
```bash
python whatsapp_rpc.py
```

### Test using Postman
```http
POST http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method`  | `string` | **Required**. (apiStatus)   |
| `params`  | `list`   | [group_name, members]  |
| `id    `  | `string` or `int` | **Required**      |

