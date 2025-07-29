import json
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

bucket_name = 'your-upload-bucket'  # replace with your bucket
collection_id = 'your-collection-id'  # replace with your Rekognition collection

def lambda_handler(event, context):
    try:
        file_name = event['file_name']

        response = rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_name
                }
            },
            MaxFaces=5,
            FaceMatchThreshold=80
        )

        face_matches = response.get('FaceMatches', [])

        results = []
        for match in face_matches:
            results.append({
                'FaceId': match['Face']['FaceId'],
                'Similarity': match['Similarity'],
                'ExternalImageId': match['Face'].get('ExternalImageId', 'N/A')
            })

        return {
            'statusCode': 200,
            'body': json.dumps({'face_matches': results})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
