# UPI JSON Data - Hands On


### Install Node JS - Windows
```bash
Download nodeJS and double click to install (Windows)
```
### Install Node JS - Ubuntu
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
nvm install node
nvm use node
node -v
```

### Install json-server
```bash
npm install -g json-server
```

### Sample Transaction Data
```bash
{
      "transactionId": "9e8d1223-c25a-4845-a37d-1a24f1e96d86",
      "timestamp": "2024-07-07T16:00:55.393Z",
      "amount": 67218,
      "currency": "EUR",
      "payer": {
        "bank": "idfc",
        "name": "Esther",
        "mobile": "(883) 652-4890 x791"
      },
      "payerUpiId": "Esther-idfc",
      "payee": {
        "bank": "hdfc",
        "name": "Clotilde",
        "mobile": "431.577.5699 x51412"
      },
      "payeeUpiId": "Clotilde-hdfc",
      "status": "processing",
      "note": "Shirt",
      "metadata": {
        "latitude": 41.9584,
        "longitude": -168.9186,
        "ip": "94.177.133.63"
      }
    }

```



### JSON Generator Tool
```bash
https://www.jsongenerator.io/
```
### JSON Generator Template
```bash
{
  "upi":[
    "repeat(10)",
    {
      "transactionId": "guid()",
      "timestamp": "date(2024-07-01, 2024-07-10)",
      "amount": "int(10,100000)",
      "currency": "enum(INR,USD,EUR)",
      
      "payer":{
        "bank": "enum(hdfc,sbi,idfc,axis)",
        "name": "firstName()",
        "mobile": "phoneNumber()"
      },
      "payerUpiId": "this.payer.name-this.payer.bank",
      "payee":{
        "bank": "enum(hdfc,sbi,idfc,axis)",
        "name": "firstName()",
        "mobile": "phoneNumber()"
      },
      "payeeUpiId": "this.payee.name-this.payee.bank",
      "status": "enum(initiated, processing, success, failed)",
      "note": "product()",
      "metadata":{
        "latitude": "latitude()",
        "longitude": "longitude()",
        "ip": "ipv4()"
      }

    }
  ]
}

```






### Start json-server
```bash
json-server -p 5000 ./db.json
```



# API Reference
Details of API usage: including request body (payload), request type, headers, etc


## Get All Transactions
#### Request Type
```http
  GET /upi
```

#### Response
```javascript
[
  {
        "transactionId": "95e44551-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 94371,
        "currency": "USD",
        "payer": {
            "bank": "axis",
            "name": "Lisa",
            "mobile": "(898) 511-6727"
        },
        "payerUpiId": "Lisa-axis",
        "payee": {
            "bank": "sbi",
            "name": "Kurt",
            "mobile": "475.211.8942 x1002"
        },
        "payeeUpiId": "Kurt-sbi",
        "status": "processing",
        "note": "Fish",
        "metadata": {
            "latitude": 75.4021,
            "longitude": 18.3344,
            "ip": "215.235.229.18"
        },
        "id": "1b90"
    }
]
```

## Get one transaction by JSON ID
#### Request Type
```http
  GET /upi/{id}
```
#### Response
```javascript
[
  {
        "transactionId": "95e44551-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 94371,
        "currency": "USD",
        "payer": {
            "bank": "axis",
            "name": "Lisa",
            "mobile": "(898) 511-6727"
        },
        "payerUpiId": "Lisa-axis",
        "payee": {
            "bank": "sbi",
            "name": "Kurt",
            "mobile": "475.211.8942 x1002"
        },
        "payeeUpiId": "Kurt-sbi",
        "status": "processing",
        "note": "Fish",
        "metadata": {
            "latitude": 75.4021,
            "longitude": 18.3344,
            "ip": "215.235.229.18"
        },
        "id": "1b90"
    }
]
```


## Get one transaction using URL parameter
#### Request Type
```http
  GET /upi?{transactionId}
```
```http
  GET /upi?{payerUpiId}
```
#### Response
```javascript
[
    {
        "transactionId": "95e44551-8801-4e7b-8f84-51dc8f4fccc1",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 94371,
        "currency": "USD",
        "payer": {
            "bank": "axis",
            "name": "Lisa",
            "mobile": "(898) 511-6727"
        },
        "payerUpiId": "Lisa-axis",
        "payee": {
            "bank": "sbi",
            "name": "Kurt",
            "mobile": "475.211.8942 x1002"
        },
        "payeeUpiId": "Kurt-sbi",
        "status": "processing",
        "note": "Fish",
        "metadata": {
            "latitude": 75.4021,
            "longitude": 18.3344,
            "ip": "215.235.229.18"
        },
        "id": "1b90"
    }
]
```


## Create UPI Transaction
```http
  POST /upi
```
#### Response
```javascript
{
        "transactionId": "my_transaction_id",
        "timestamp": "2024-07-02T10:42:36.340Z",
        "amount": 130,
        "currency": "INR",
        "payer": {
            "bank": "axis",
            "name": "Ankit",
            "mobile": "9940330141"
        },
        "payerUpiId": "ankit-axis",
        "payee": {
            "bank": "sbi",
            "name": "Kurt",
            "mobile": "475.211.8942 x1002"
        },
        "payeeUpiId": "Kurt-sbi",
        "status": "processing",
        "note": "Fish",
        "metadata": {
            "latitude": 75.4021,
            "longitude": 18.3344,
            "ip": "215.235.229.18"
        },
        "id": "1b90"
    }
```

## Delete UPI Transaction
```http
  DELETE /upi/{jsonId}
```


## Update UPI Transaction
```http
  PUT /upi/{jsonId}
```

