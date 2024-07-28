import jwt

hmac_api_secret_key = "mysecret"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ3d3cudGhlYnJva2VuYXBwLmluIiwic3ViIjoiYW5raXQiLCJleHAiOjE3MjMxODg5NjV9.4jojx1VOhT_e0CAum1gXMgNr6vepZbD4gU-MzbgHQpY"
decoded = jwt.decode(token, key=hmac_api_secret_key, algorithms='HS256')

print(decoded)
