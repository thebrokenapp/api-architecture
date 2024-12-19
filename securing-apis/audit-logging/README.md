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
# Before request hook
@app.before_request
def before_request():
    # You can log every incoming request here (for audit, debugging, etc.)
    auth_header = request.headers.get('Authorization')
    request.username = "anonymous"
    if auth_header and auth_header.startswith('Basic '):
	    encoded_credentials = auth_header.split(' ')[1]
	    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
	    request.username, _ = decoded_credentials.split(':', 1)

    request.guid = str(uuid.uuid4())  # Store GUID in the request object
    audit_logger.info(f"User: {request.username} Request GUID: {request.guid} - Incoming request: {request.method} {request.path}")

# After request hook
@app.after_request
def after_request(response):
    # You can log the response or modify it here (e.g., log status codes, modify headers)
    response.headers['X-Request-GUID'] = request.guid    # Add GUID to the response headers
    audit_logger.info(f"User: {request.username} Response GUID: {request.guid} - Response: {response.status_code} for {request.method} {request.path}")
```

#### Run file
```bash
python payments_audit.py
```

#### Check content of  audit.log file
```bash
cat audit.lgo
```
