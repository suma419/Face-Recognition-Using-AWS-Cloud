import boto3

s3 = boto3.client('s3')
bucket_name = 'your-upload-bucket'  # Replace with your bucket name

def create_bucket():
    region = s3.meta.region_name
    if region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    print(f"S3 bucket '{bucket_name}' created.")

if __name__ == "__main__":
    create_bucket()
