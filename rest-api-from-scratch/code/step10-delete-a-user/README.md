### Delete a user
```python
@app.route('/users/<user_name>', methods=['DELETE'])
def delete_user(user_name):
	if user_name in users:
		users.pop(user_name)
		return '',204
	else:
		return {"message": "User not found"}, 404
```
