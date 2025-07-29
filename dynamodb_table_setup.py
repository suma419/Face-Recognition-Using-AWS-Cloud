import boto3

dynamodb = boto3.resource('dynamodb')

def create_table():
    table = dynamodb.create_table(
        TableName='FaceRecognitionResults',
        KeySchema=[
            {'AttributeName': 'FaceId', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'FaceId', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    print("DynamoDB table created")

if __name__ == "__main__":
    create_table()
