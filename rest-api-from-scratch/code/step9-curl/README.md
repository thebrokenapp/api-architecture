## Making API requests will curl

#### GET Request
```bash
curl -X GET http://127.0.0.1:8001/apiStatus
```

#### Adding Headers
```bash
curl -X GET -H "Content-Type:application/json" http://127.0.0.1:8001/apiStatus
```


#### POST Request
```bash
curl -X POST -H "Content-Type:application/json" http://127.0.0.1:8001/payments -d '{
    "user_name":"yash",
    "amount": 2000,
    "payer_upi": "abx@okhdfc",
    "payee_upi": "qwe-sbi",
    "note": "dinner"
}'
```
