
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def handle_message():
    data = request.json
    message = data.get('message', '')
    #print(f"Received message: {message}")
    query = message
    return jsonify({"status": "success", "message": message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
