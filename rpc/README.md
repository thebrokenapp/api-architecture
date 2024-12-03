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

## Import RPC libraries
```python
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
```

## Add first route `apiStatus`
```python
def api_status():
    # do some checks
    return { "notes": "API is up!"}
```

## Specify the `host` and `port` on which you want to run the RPC
```python
host = '127.0.0.1'
port = 8000
```

## Create server object
```python
server = SimpleJSONRPCServer((host, port))
```

## Register the function that you want to expose as API
```python
server.register_function(api_status)
```

## Launch RPC API Server
```python
print("Starting server on", host +":"+ str(port))
server.serve_forever()
```

## So far your entire code should look like this
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

## Launch your API
```bash
python whatsapp_rpc.py
```
