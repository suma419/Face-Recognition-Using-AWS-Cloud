import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
bucket_name = 'your-upload-bucket'  # replace with your S3 bucket

def lambda_handler(event, context):
    try:
        # Decode the incoming image data (assumes base64)
        body = event['body']
        if event.get('isBase64Encoded'):
            image_data = base64.b64decode(body)
        else:
            image_data = body.encode('utf-8')

        # Generate unique filename
        file_name = f"{uuid.uuid4()}.jpg"

        # Upload image to S3 bucket
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=image_data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Image uploaded', 'file_name': file_name})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
