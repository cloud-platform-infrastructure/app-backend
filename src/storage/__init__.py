from .dynamodb_storage import get_all_logs, save_log, delete_log

print("Using DynamoDB Storage")

__all__ = ['get_all_logs', 'save_log', 'delete_log']
