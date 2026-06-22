import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iac_toys')

def lambda_handler(event, context):
    try:
        response = table.scan()
        toys = response.get('Items', [])
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(toys, cls=DecimalEncoder)
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}