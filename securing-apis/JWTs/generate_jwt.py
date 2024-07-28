import jwt


hmac_api_secret_key = "mysecret"

encoded_jwt = jwt.encode(
							{"iss": "www.thebrokenapp.in", "sub": "ankit", "exp": 1723188965},
							hmac_api_secret_key,
							algorithm="HS256"
						)

print(encoded_jwt)
