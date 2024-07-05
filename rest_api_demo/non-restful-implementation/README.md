# Sample Requests


### Make Payment

#### POST /upi
```javascript
{
    "action": "make_payment",
    "to": "ankit",
    "from": "rohit",
    "amount": "3100"
}
```
### Check Payment Status
#### POST /upi
```javascript
{
    "action": "check_status",
    "transaction_id": "de9e03a0-f84d-4c7b-992e-c62d97c8085b"
}
```
### Update Payment Status
#### POST /upi
```javascript
{
    "action": "update_status",
    "transaction_id": "de9e03a0-f84d-4c7b-992e-c62d97c8085b",
    "status": "complete"
}
```
