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
        path_parameters = event.get('pathParameters') or {}
        toy_id = path_parameters.get('id')
        
        response = table.get_item(Key={'id': toy_id})
        toy = response.get('Item')
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
        
        if not toy:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Juguete no encontrado'})
            }
            
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(toy, cls=DecimalEncoder)
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}