## Add a user or Sign Up

### Few things we are adding
For creation of users we are using appropriate response code of `201`.

Similary, if user already exists we are using `409` which is `conflict`

```python
users = dict()


@app.route('/users', methods=['POST'])
def create_user():
	data = request.get_json()				# extract the request body and store it in variable "data"
	user_name = data.get("user_name")		# extract user name from request body
	password = data.get("password")			# extract password from request body
	
	if user_name in users:					# check is username already exists in users DB
		return {"message": "user already exists"}, 409
	
	users[user_name] = password
	return data, 201
```
