## Create Group Function

#### Create groups table
```bash
sqlite3 messaging.db

CREATE TABLE groups (
    group_name TEXT UNIQUE,
    create_date TEXT
);
```

#### Add new function
```python

def create_group(group_name):
    status = "success"
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()  # use the function defined above to get a connection to DB
    cursor = conn.cursor()      # # Creates a cursor object to interact with the database.
    try:
        # Attempt to insert the new group
        cursor.execute('''INSERT INTO groups (group_name, create_date) VALUES (?, ?)''',(group_name, create_date))
        conn.commit()
        return {"txn_status": "success", "txn_timestamp": create_date, "notes": "group is created with name: " + group_name}
    except sqlite3.IntegrityError:
        # Handle the case where the group already exists
        return {"txn_status": "failed", "txn_timestamp": create_date, "notes": "group already exists: " + group_name}

```

### Register the function that you want to expose as API
```python
server.register_function(create_group)
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
| `method`  | `string` | **Required**. (apiStatus)   |
| `params`  | `list`   | **Required**. [group_name]  |
| `id    `  | `string` or `int` | **Required**      |
