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


## Function 3: `create_group`
### Create a mock database as python dictionary
```python
groups = {}
```

### Add 3rd function `create_group()`
```python
def create_group(group_name, members):
    groups[group_name] = [members]
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
| `params`  | `list`   | **Required**. [group_name, members]  |
| `id    `  | `string` or `int` | **Required**      |



## Function 4: `add_members`
### Add 4th function `add_members()`
```python
def add_members(group_name, members):
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if group_name in groups:
        groups[group_name].append(members)
        return {"txn_status": status, "txn_timestamp": timestamp, "notes": "members added in the group: " + group_name}
    else:
        return {"txn_status": status, "txn_timestamp": timestamp, "notes": "group does not exist: " + group_name}
```


### Register the function that you want to expose as API
```python
server.register_function(add_members)
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
| `params`  | `list`   | **Required**. [group_name, members]  |
| `id    `  | `string` or `int` | **Required**      |



## Function 5: `find_group_members`
### Add 5th function `find_group_members()`
```python
members = groups.get(group_name)
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if members is not None:
        return {"txn_status": status, "txn_timestamp": timestamp, "members": members}
    else:
        return {"txn_status": status, "txn_timestamp": timestamp, "members": [], "notes": "group not found"}
```


### Register the function that you want to expose as API
```python
server.register_function(find_group_members)
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
| `params`  | `list`   | **Required**. [group_name]  |
| `id    `  | `string` or `int` | **Required**      |





## Function 6: `find_all_groups`
### Add 5th function `find_all_groups()`
```python
status = "success"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
return {"txn_status": status, "txn_timestamp": timestamp, "groups": list(groups.keys())}
```


### Register the function that you want to expose as API
```python
server.register_function(find_all_groups)
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

