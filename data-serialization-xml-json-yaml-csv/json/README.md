# Sample UPI JSON


### Install Node JS
```bash
Download nodeJS and double click to install
```
### Install json-server
```bash
npm install -g json-server
```

### Sample Transaction Data
```bash
{
    "transaction_id": "txn_1234567890",
    "timestamp": "2024-07-04T10:15:30Z",
    "status": "SUCCESS",
    "amount": {
        "currency": "INR",
        "value": 500
    },
    "sender": {
        "name": "Alice",
        "upi_id": "alice@bank"
    },
    "recipient": {
        "name": "Bob",
        "upi_id": "bob@bank"
    },
    "remarks": "Payment for dinner",
    "transaction_type": "P2P",
    "reference_id": "ref_9876543210",
    "bank_response_code": "00",
    "bank_transaction_id": "bank_txn_112233",
    "additional_info": {
        "device_id": "device_abcdefg12345",
        "geo_location": {
            "latitude": 12.9715987,
            "longitude": 77.594566
        }
    }
}

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
