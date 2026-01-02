import uuid
from datetime import datetime
import sys
import os

# Add src to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services import slack_service
from storage import save_log # Use abstraction

def handle_message(body):
    try:
        message = body.get('message')
        if not message:
            return {'error': 'Message is required'}, 400

        # 1. Send to Slack
        slack_response = slack_service.post_message(message)

        # 2. Create Log Object
        log = {
            'id': str(uuid.uuid4()),
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
            'slack_message_ts': slack_response.get('ts'),
        }

        # 3. Save to Storage
        updated_logs = save_log(log)

        # 4. Return updated list
        return updated_logs, 200

    except Exception as e:
        print(f"Error in message handler: {e}")
        return {'error': 'Internal Server Error'}, 500
