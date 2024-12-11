

#### Create payments table
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
