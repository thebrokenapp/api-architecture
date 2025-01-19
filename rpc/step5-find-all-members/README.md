## Find All Members

#### Add new function
```python
def find_members_of_group(group_name):
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    cursor.execute('''SELECT member_name from group_members WHERE group_name=?''',(group_name,))
    members = cursor.fetchall()
    member_names = [row[0] for row in members]
    return { "members": member_names, "group_name":group_name}

```

### Register the function that you want to expose as API
```python
server.register_function(find_members_of_group))
```

### Launch your API
```bash
python messaging.py
```

### Test using Postman
```http
POST http://127.0.0.1:8000
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method`  | `string` | **Required**. (find_members_of_group)   |
| `params`  | `list`   | **Required**. [group_name]  |
| `id    `  | `string` or `int` | **Required**      |
