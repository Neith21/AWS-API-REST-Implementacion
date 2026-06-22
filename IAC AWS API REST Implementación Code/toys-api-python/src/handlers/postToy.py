import json
import boto3
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
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
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)
        
        new_toy = {
            **body,
            'id': str(uuid.uuid4()),
            'created_at': datetime.now(ZoneInfo("America/El_Salvador")).strftime("%d/%m/%Y, %H:%M:%S")
        }
        
        table.put_item(Item=new_toy)
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps([new_toy, {'message': 'Juguete creado exitosamente'}], cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}