from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from datetime import datetime


groups = {}

def api_status():
    # do some checks
    return { "notes": "API is up!"}


def send_message(message_from, message_to, message):
    # do some logic
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"txn_status": status, "send_time": timestamp, "notes": "message has been sent to " + message_to}


def create_group(group_name, members):
    groups[group_name] = members
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {"txn_status": status, "txn_timestamp": timestamp, "notes": "group is created with name: " + group_name}


def add_members(group_name, members):
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if group_name in groups:
        groups[group_name].append(members)
        return {"txn_status": status, "txn_timestamp": timestamp, "notes": "members added in the group: " + group_name}
    else:
        return {"txn_status": status, "txn_timestamp": timestamp, "notes": "group does not exist: " + group_name}
    

def find_group_members(group_name):
    members = groups.get(group_name)
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if members is not None:
        return {"txn_status": status, "txn_timestamp": timestamp, "members": members}
    else:
        return {"txn_status": status, "txn_timestamp": timestamp, "members": [], "notes": "group not found"}


def find_all_groups():
    status = "success"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"txn_status": status, "txn_timestamp": timestamp, "groups": list(groups.keys())}


host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
server.register_function(send_message)
server.register_function(create_group)
server.register_function(add_members)
server.register_function(find_group_members)
server.register_function(find_all_groups)
print("Starting server on", host +":"+ str(port))
server.serve_forever()


