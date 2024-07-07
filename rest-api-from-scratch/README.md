
# REST API From Scratch
Before we begin, let's upderstand the API that we are building along with request URLs, methods, request body, response body, etc



## Fetch All Payments
#### Request Type
```http
GET /payments
```

#### Response
```javascript
[
  {
        "transaction_id":"95e44551-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 94371,
        "payer_upi": "ankit@okhdfc
        "payee_upi": "alex-sbi",
        "status": "processing",
        "note": "Lunch",
    },
    {
        "transaction_id": "45edfg1-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 12000,
        "payer_upi": "abx@okhdfc
        "payee_upi": "qwe-sbi",
        "status": "processing",
        "note": "Books",
    }
]
```

## Fetch one payment by transaction ID
#### Request Type
```http
GET payments/{transaction_id}
```
#### Response
```javascript
{
        "transaction_id": "95e44551-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 94371,
        "payer_upi": "ankit@okhdfc
        "payee_upi": "alex-sbi",
        "status": "processing",
        "note": "Fish",
    }
```


## Create UPI Transaction
```http
POST /payments
```
#### Request
```javascript
{
        "amount": 12000,
        "payer_upi": "abx@okhdfc
        "payee_upi": "qwe-sbi",
        "note": "Books",
    }
```

## Delete UPI Transaction
```http
DELETE /payments/{transaction_id}
```


## Update UPI Transaction
```http
PUT /payments/{transaction_id}
```

