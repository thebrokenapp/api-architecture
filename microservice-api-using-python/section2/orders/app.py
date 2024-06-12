# file: orders/app.py

from fastapi import FastAPI
from orders.api import api

app = FastAPI(debug=True)
