import json
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from handlers import message_handler, logs_handler

def print_response(name, response):
    print(f"\n--- {name} ---")
    print(f"Status: {response['statusCode']}")
    print(f"Body: {response['body']}")

def test_backend():
    print("Testing Backend Handlers Locally...")

    # 1. Test POST /message
    print("\n1. Testing POST /message")
    post_event = {
        'body': json.dumps({'message': 'Hello from local Python test!'})
    }
    post_response = message_handler.handler(post_event, None)
    print_response("POST /message", post_response)

    if post_response['statusCode'] != 200:
        print("Failed to post message. Aborting.")
        return

    # 2. Test GET /logs
    print("\n2. Testing GET /logs")
    get_response = logs_handler.get_logs_handler({}, None)
    print_response("GET /logs", get_response)
    
    logs = json.loads(get_response['body'])
    if not logs:
        print("No logs found. Aborting.")
        return

    last_log_id = logs[-1]['id']
    print(f"\nLast Log ID: {last_log_id}")

    # 3. Test DELETE /log/{id}
    print(f"\n3. Testing DELETE /log/{last_log_id}")
    delete_event = {
        'pathParameters': {'id': last_log_id}
    }
    delete_response = logs_handler.delete_log_handler(delete_event, None)
    print_response(f"DELETE /log/{last_log_id}", delete_response)

    # 4. Verify Deletion
    print("\n4. Verifying Deletion (GET /logs)")
    final_get_response = logs_handler.get_logs_handler({}, None)
    print_response("GET /logs (After Delete)", final_get_response)

if __name__ == "__main__":
    test_backend()
