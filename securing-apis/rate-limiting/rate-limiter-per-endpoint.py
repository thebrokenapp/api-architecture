from flask import Flask

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "5 per hour"],
    storage_uri="memory://",
)

# rate of 8 per day and default limit is not applied
@app.route("/apiStatus")
@limiter.limit("8 per day")
def apiStatus():
    return "API is up"

# Rate of 1 request per second and default limit is also applied
@app.route("/makePayment")
@limiter.limit("1/second", override_defaults=False)
def makePayment():
    return "Payment Done"

# default limit is applied
@app.route("/fetchPayment")
def fast():
    return "Payment Fetched"

# no limit is applied
@app.route("/checkBalance")
@limiter.exempt
def ping():
    return "Balance is Rs.100"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port= 5000, debug=True)
