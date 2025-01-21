## Making Request to an API via Code

#### GET Request
```python
import requests

url = "http://127.0.0.1:8001/apiStatus"
response = requests.get(url)
print(response.status_code, response.json())
```

#### POST Request
```python
import requests
import json

request_body ={
    "user_name":"yash",
    "amount": 2000,
    "payer_upi": "abx@okhdfc",
    "payee_upi": "qwe-sbi",
    "note": "dinner"
}
headers = {"Content-Type": "application/json"}
url = "http://127.0.0.1:8001/payments"
response = requests.post(url, data=json.dumps(request_body), headers=headers)
print(response.status_code, response.text)

```
