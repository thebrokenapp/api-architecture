from flask import Flask, request, jsonify, make_response
import dicttoxml
import uuid


app = Flask(__name__)
transactions = []
order_id = 0
@app.route('/upi', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':
        data = request.get_json()
        if data['action'] == 'make_payment':
            transaction_id = str(uuid.uuid4())
            transaction = {"transaction_id": transaction_id, "from": data.get("from"), "to": data.get("to"), "amount": data.get("amount"), "status": "initiated"}
            transactions.append(transaction)
            return transaction
        elif data['action'] == 'check_status':
            transaction_id = data.get("transaction_id")
            for transaction in transactions:
                print(transaction_id)
                print(transaction.get("transaction_id"))
                if transaction.get("transaction_id") == transaction_id:
                    return transaction
            return jsonify({"message": "transaction does not exist"})


        elif data['action'] == 'update_status':
            transaction_id = data.get("transaction_id")
            status = data.get("status")
            for transaction in transactions:
                if transaction.get("transaction_id") == transaction_id:
                    transaction["status"] = status
                    return transaction
            return jsonify({"message": "transaction does not exist"})

        elif data['action'] == 'check_balance':
            return jsonify({"balance": "Rs100"})
    else:
        return jsonify({"message": "Only POST method allowed"})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
