import json
import boto3
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('toys')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)

        new_product = {
            **body,
            'id': str(uuid.uuid4()),
            'created_at': datetime.now(ZoneInfo("America/El_Salvador")).strftime("%d/%m/%Y, %H:%M:%S")
        }
        
        table.put_item(Item=new_product)
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

        if 'price' in new_product and isinstance(new_product['price'], Decimal):
            new_product['price'] = float(new_product['price'])

        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps([new_product, {'message': 'Producto creado exitosamente'}])
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
    