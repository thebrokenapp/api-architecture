# file: orders/api/api.py

from datetime import datetime
from uuid import UUID
from starlette.responses import Response
from starlette import status
from orders.app import app


# We define an order object to return in our responses.
order = {
			'id': 'ff0f1355-e821-4178-9567-550dec27a373',
			'status': "delivered",
			'created': datetime.utcnow(),
			'order': [
						{
						'product': 'cappuccino',
						'size': 'medium',
						'quantity': 1
						}
					]
		}


# We register a GET endpoint for the /orders URL path
@app.get('/orders')
def get_orders():
	return {'orders': [orders]}


# We specify that the response’s status code is 201 (Created)
@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order():
	return order


# We define URL parameters, such as order_id, within curly brackets
@app.get('/orders/{order_id}')
def get_order(order_id: UUID):		# We capture the URL parameter 'order_id' as a function argument
	return order



@app.put('/orders/{order_id}')
def update_order(order_id: UUID):
	return order


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
	return Response(status_code=HTTPStatus.NO_CONTENT.value)	#We use HTTPStatus.NO_CONTENT.value to return an empty response.


@app.post('/orders/{order_id}/cancel')
def cancel_order(order_id: UUID):
	return order


@app.post('/orders/{order_id}/pay')
def pay_order(order_id: UUID):
	return order
