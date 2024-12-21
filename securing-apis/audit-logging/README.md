## Add Logging To Your Payments API

#### Add Imports
```python
import logging
import base64
```

#### Set up logging configuration
```python
logging.basicConfig(
    filename='audit.log',  # Log to this file
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
audit_logger = logging.getLogger('audit')
```

#### Add `before_request` and `after_request`
```python
# Get executed Before request reaches the actual route 
@app.before_request
def before_request():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_header = auth_header.split(' ')
		encoded_credentials = auth_header[1]
		decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
		request.username = decoded_credentials.split(':')[0]
	else:
		request.username = "anonymous"
	
	if not request.headers.get('X-Request-GUID'):
		request.guid = str(uuid.uuid4())  # Store GUID in the request object
	else:
		request.guid = request.headers.get('X-Request-GUID')
	audit_logger.info(f"Request -> User: {request.username} | Request GUID: {request.guid} | Action: {request.method} | Resource: {request.path}")

# Gets executed after request is processed by the route
@app.after_request
def after_request(response):
	# You can log the response or modify it here (e.g., log status codes, modify headers)
	response.headers['X-Request-GUID'] = request.guid    # Add GUID to the response headers
	audit_logger.info(f"Response -> User: {request.username} | Response GUID: {request.guid} | Result: {response.status_code}")
	return response
```

#### Run file
```bash
python payments_audit.py
```

#### Check content of  audit.log file
```bash
cat audit.lgo
```
