### Get All Users
```python
@app.route('/users', methods=['GET'])
def get_all_users():
	return users
```

### Get single user
```python
@app.route('/users/<user_name>', methods=['GET'])
def get_one_user(user_name):
	if user_name in users:
		return {"user_name": user_name, "password": users.get(user_name)}
	else:
		return {"message": "User not found"}, 404
```
