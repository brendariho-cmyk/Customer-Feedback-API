import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Feedback')

def handler(event, context):
    body = json.loads(event['body'])
    
    item = {
        'feedbackId': str(uuid.uuid4()),
        'name': body.get('name'),
        'email': body.get('email'),
        'message': body.get('message'),
        'createdAt': datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Feedback received!", "data": item})
    }

