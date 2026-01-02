import sys
import os

# Add src to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services import slack_service
from storage import get_all_logs, delete_log as delete_log_storage # Use abstraction

def get_logs():
    try:
        logs = get_all_logs()
        return logs, 200
    except Exception as e:
        print(f"Error getting logs: {e}")
        return {'error': 'Internal Server Error'}, 500

def delete_log(log_id):
    try:
        if not log_id:
            return {'error': 'ID is required'}, 400

        # 1. Delete from Storage
        updated_logs, deleted_log = delete_log_storage(log_id)

        # 2. Delete from Slack if applicable
        if deleted_log and deleted_log.get('slack_message_ts'):
            slack_service.delete_message(deleted_log.get('slack_message_ts'))

        return updated_logs, 200

    except Exception as e:
        print(f"Error deleting log: {e}")
        return {'error': 'Internal Server Error'}, 500
