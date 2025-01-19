from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def api_status():
    # do some checks
    return { "notes": "RPC API is up!"}

host = '127.0.0.1'
port = 8000
server = SimpleJSONRPCServer((host, port))
server.register_function(api_status)
print("Started RCPC Server!")
server.serve_forever()
