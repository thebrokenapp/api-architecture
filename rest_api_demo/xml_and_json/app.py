from flask import Flask, request, jsonify, make_response
import dicttoxml


app = Flask(__name__)

@app.route('/user', methods=['GET'])
def get_data():
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }

    content_type = request.headers.get('Content-Type')

    if content_type == 'application/xml':
        response = make_response(dicttoxml.dicttoxml(data))
        response.headers['Content-Type'] = 'application/xml'
    elif content_type == 'application/json':
        response = jsonify(data)
    else:
        response = jsonify({"error": "Unsupported Content-Type"})
        response.status_code = 400

    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# XML Request
# curl -H "Content-Type: application/xml" http://127.0.0.1:5000/data


# JSON Request
# curl -H "Content-Type: application/json" http://127.0.0.1:5000/data
