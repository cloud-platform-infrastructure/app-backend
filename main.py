from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from handlers import message_handler, logs_handler

app = Flask(__name__)
CORS(app)

@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json(silent=True) or {}
    response, status_code = message_handler.handle_message(data)
    return jsonify(response), status_code

@app.route('/logs', methods=['GET'])
def handle_get_logs():
    response, status_code = logs_handler.get_logs()
    return jsonify(response), status_code

@app.route('/log/<id>', methods=['DELETE'])
def handle_delete_log(id):
    response, status_code = logs_handler.delete_log(id)
    return jsonify(response), status_code

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
