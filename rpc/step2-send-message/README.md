## Send Message Function

### Install Sqlite3
We will use `sqlite3` database to store message information
```bash
sudo apt install sqlite3
```

Check if it's installed
```bash
sqlite3 --version
```


### Create messages table
#### Create a database
```bash
sqlite3 whatsapp.db
```

#### Create messages table
```sql
CREATE TABLE messages (
    message_from TEXT,
    message_to TEXT,
    message_text TEXT,
    message_time TEXT
);
```
