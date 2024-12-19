#### Download the file `rate-limiter-per-endpoint.py`

#### Installation
```bash
pip install Flask-Limiter
```

#### Import Libraries
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
```

#### Add Rate Limiting Logic
```python
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per day", "5 per second"],
    storage_uri="memory://",
)
```

#### Run the code
```bash
python payments.py
```

#### Test different endpoints from Postman
```bash
GET /apiStatus
GET /makePayment
GET /fetchPayment
GET /checkBalance
```
