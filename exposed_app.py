from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify(message="Hello, world!")

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
