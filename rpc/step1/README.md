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
    return { "notes": "RPC API is up!"}

host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
print("Starting RPC server!)
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
