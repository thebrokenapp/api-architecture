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
