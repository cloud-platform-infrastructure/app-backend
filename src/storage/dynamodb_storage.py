import boto3
import os
from typing import List, Dict, Optional
from botocore.exceptions import ClientError

DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
REGION = os.environ.get('AWS_REGION', 'us-east-1')

def _get_table():
    if not DYNAMODB_TABLE:
        raise ValueError("DYNAMODB_TABLE environment variable is not set")
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    return dynamodb.Table(DYNAMODB_TABLE)

def get_all_logs() -> List[Dict]:
    try:
        table = _get_table()
        response = table.scan()
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error scanning DynamoDB table: {e}")
        raise

def save_log(log: Dict) -> List[Dict]:
    try:
        table = _get_table()
        table.put_item(Item=log)
        # DynamoDB put_item doesn't return the full list, so we scan again to return all logs
        # Note: In a real high-scale app, we wouldn't return all logs on every save.
        return get_all_logs()
    except ClientError as e:
        print(f"Error saving to DynamoDB: {e}")
        raise

def delete_log(log_id: str) -> tuple[List[Dict], Optional[Dict]]:
    try:
        table = _get_table()
        
        # First get the item to return it (and check if it exists)
        response = table.get_item(Key={'id': log_id})
        log_to_delete = response.get('Item')

        if log_to_delete:
            table.delete_item(Key={'id': log_id})
            
        return get_all_logs(), log_to_delete
    except ClientError as e:
        print(f"Error deleting from DynamoDB: {e}")
        raise
