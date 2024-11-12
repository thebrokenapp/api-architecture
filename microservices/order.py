# order_service.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Endpoint to create an order
@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    item_id = data.get("item_id")
    quantity = data.get("quantity")

    # Verify if item exists and has enough stock
    inventory_url = f"http://localhost:5001/inventory/{item_id}"
    inventory_response = requests.get(inventory_url)

    if inventory_response.status_code != 200:
        return jsonify({"error": "Item not found in inventory"}), 404

    item_data = inventory_response.json()
    if item_data["stock"] < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    # Update inventory after placing order
    update_response = requests.put(inventory_url, json={"quantity": quantity})
    if update_response.status_code != 200:
        return jsonify({"error": "Failed to update inventory"}), 500

    return jsonify({
        "message": "Order placed successfully",
        "item_id": item_id,
        "quantity": quantity,
        "remaining_stock": update_response.json().get("new_stock")
    })

if __name__ == '__main__':
    app.run(port=5002, debug=True)  # Order service runs on port 5002
