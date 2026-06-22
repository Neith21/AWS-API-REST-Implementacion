import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iac_toys')

def lambda_handler(event, context):
    try:
        path_parameters = event.get('pathParameters') or {}
        toy_id = path_parameters.get('id')
        body = json.loads(event.get('body', '{}'), parse_float=Decimal)
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
        
        result = table.get_item(Key={'id': toy_id})
        if 'Item' not in result:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Registro no encontrado'})
            }

        if not body:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'No se enviaron datos para actualizar'})
            }

        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}
        
        for key, value in body.items():
            if key == 'id': continue 
            update_expression += f"#{key} = :{key}, "
            expression_attribute_names[f"#{key}"] = key
            expression_attribute_values[f":{key}"] = value
            
        update_expression = update_expression.rstrip(", ")
        
        table.update_item(
            Key={'id': toy_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Registro actualizado exitosamente'})
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}