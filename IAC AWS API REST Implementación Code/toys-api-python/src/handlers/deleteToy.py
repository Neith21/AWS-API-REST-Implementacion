import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iac_toys')

def lambda_handler(event, context):
    try:
        path_parameters = event.get('pathParameters') or {}
        toy_id = path_parameters.get('id')
        
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

        table.delete_item(Key={'id': toy_id})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Registro eliminado exitosamente'})
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}