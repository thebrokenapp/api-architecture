## Join Group Function

#### Create groups table
```bash
sqlite3 messaging.db

CREATE TABLE group_members (
    group_name TEXT,
    member_name TEXT,
    join_date TEXT
);
```

#### Add new function
```python
def join_group(group_name, member_name):
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    cursor.execute('''INSERT INTO group_members (group_name, member_name, join_date) VALUES (?, ?, ?)''',(group_name, member_name, join_date))
    conn.commit()
    conn.close()

    return {"txn_status": "success", "txn_timestamp": join_date, "notes": member_name + " added to group " + group_name}
   return {"txn_status": "failed", "txn_timestamp": create_date, "notes": "group already exists: " + group_name}

```

### Register the function that you want to expose as API
```python
server.register_function(join_group)
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
| `method`  | `string` | **Required**. (join_group)   |
| `params`  | `list`   | **Required**. [group_name,member_name]  |
| `id    `  | `string` or `int` | **Required**      |
