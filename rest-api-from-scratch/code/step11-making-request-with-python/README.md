## Making Request to an API via Code

#### Install Library
```bash
pip install requests
```

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

#### PATCH request
```python
import requests

# URL to send the PATCH request to
url = "https://example.com/api/resource"

# Data to be sent in the PATCH request (usually a partial update)
data = {
    "field1": "new_value",
    "field2": "updated_value"
}

# Send the PATCH request
response = requests.patch(url, json=data)

# Check the response status and content
if response.status_code == 200:
    print("Update successful:", response.json())
else:
    print("Failed to update. Status code:", response.status_code)

```
