# Add caching to your Payments API

## Install SQLite3 
```bash
sudo apt install sqlite3
```
Check if it's installed
```bash
sqlite3 --version
```


## Create payments table
```sql
CREATE TABLE payments (
    transaction_id TEXT PRIMARY KEY,
    amount TEXT NOT NULL,
    status TEXT NOT NULL,
    payer_upi TEXT NOT NULL,
    payee_upi TEXT NOT NULL,
    note TEXT,
    timestamp TEXT NOT NULL
);

```
