### Launch The Payment API

#### Before launching the API we need to make some changes

#### Install flaks-cors
```bash
pip install flask-cors
```

#### Add the following code in app.py
```python
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
```
