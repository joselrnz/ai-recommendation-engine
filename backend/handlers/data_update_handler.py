import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserInteractions')

def lambda_handler(event, context):
    """
    Lambda function to update user interaction data in DynamoDB.
    """
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        item_id = body['item_id']
        timestamp = body['timestamp']

        table.put_item(
            Item={
                'user_id': str(user_id),
                'item_id': str(item_id),
                'timestamp': int(timestamp)
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User interaction updated successfully."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
