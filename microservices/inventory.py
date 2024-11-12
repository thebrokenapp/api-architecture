# inventory_service.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample inventory data
inventory = {
    "item1": {"name": "Widget A", "stock": 50},
    "item2": {"name": "Widget B", "stock": 0},
}

# Check stock for a given item
@app.route('/inventory/<item_id>', methods=['GET'])
def check_stock(item_id):
    item = inventory.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"item_id": item_id, "name": item["name"], "stock": item["stock"]})

# Update stock after an order is placed
@app.route('/inventory/<item_id>', methods=['PUT'])
def update_stock(item_id):
    item = inventory.get(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json()
    quantity = data.get("quantity")
    if quantity is None or quantity < 0:
        return jsonify({"error": "Invalid quantity"}), 400

    item["stock"] -= quantity
    return jsonify({"item_id": item_id, "new_stock": item["stock"]})

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Inventory service runs on port 5001
