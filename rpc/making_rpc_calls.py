from jsonrpclib import Server

# Connect to the JSON-RPC server
server = Server('http://127.0.0.1:8000')

# Example: Check API status

status = server.api_status()
print("API Status:", status)

response = server.send_message("Alice", "Bob", "Hello, Bob!")
print("Send Message Response:", response)

response = server.create_group("Developers")
print("Create Group Response:", response)

response = server.join_group("Developers", "Alice")
print("Join Group Response:", response)

response = server.find_members_of_group("Developers")
print("Group Members:", response)
