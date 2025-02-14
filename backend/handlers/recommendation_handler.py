import json
import boto3

# Initialize Amazon Personalize runtime client
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    """
    Lambda function to fetch recommendations for a given user from Amazon Personalize.
    """
    try:
        user_id = event['pathParameters']['user_id']
        
        response = personalize_runtime.get_recommendations(
            campaignArn="arn:aws:personalize:us-east-1:123456789012:campaign/MyCampaign",
            userId=str(user_id)
        )

        recommendations = [item['itemId'] for item in response['itemList']]

        return {
            "statusCode": 200,
            "body": json.dumps({"recommendations": recommendations})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
