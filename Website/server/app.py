
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import os
import sys
import uuid

'''current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)'''
from scripts.chatbot import query_business_chatbot
from scripts.chatbot import query_consumer_chatbot
#from model.scripts import embeddings

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)

Session(app)
CORS(app)

def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

@app.route('/chat_consumer', methods=['POST'])
def handle_message_consumer():
    data = request.json
    message = data.get('message', '')
    #print(f"Received message: {message}")
    session_id = get_session_id()
    query = message
    response_consumer = query_consumer_chatbot(query, session_id)
    full_return = "QUESTION: " + query + "\n\nAnswer: " + response_consumer
    print(full_return)
    return jsonify({"status": "success", "message": full_return})

@app.route('/chat_business', methods=['POST'])
def handle_message_business():
    data = request.json
    message = data.get('message', '')
    #print(f"Received message: {message}")
    query = message
    session_id = get_session_id()
    response_business = query_business_chatbot(query, session_id)
    full_return = "QUESTION: " + query + "\n\nAnswer: " + response_business
    print(full_return)
    return jsonify({"status": "success", "message": full_return})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
