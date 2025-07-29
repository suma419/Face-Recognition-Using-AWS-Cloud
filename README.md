# Face-Recognition-Using-AWS-Cloud
Real-time face recognition system built on AWS with Python and JavaScript. Auto-scaling infrastructure supports 20+ instances for fast, reliable performance. Achieves a 40% improvement in response times for seamless user experience.
Face-Recognition-AWS
Built a real-time face recognition pipeline using Amazon S3, Lambda, and Rekognition to detect and identify faces from uploaded images. Stored recognition metadata in DynamoDB for real-time querying and saved enriched recognition data in S3. Enabled monitoring through CloudWatch Logs and supported future analytics through processed S3 output.

Step 1: Image Ingestion using Amazon S3
Purpose:
To upload user or surveillance images and initiate the face recognition process automatically.

How it works:
• A user uploads an image to a designated S3 bucket (e.g., via mobile app, kiosk, surveillance system, or API).
• The image is placed under the input/ prefix (e.g., s3://face-input-bucket/input/image1.jpg).
• The S3 bucket is configured to trigger a Lambda function on each new image upload.

Why use S3?
• Durable, scalable storage for large image files.
• Native event triggering for Lambda functions.
• Easy integration with analytics tools like Athena, Glue.

Output:
• A new image gets uploaded to S3.
• Automatically triggers the recognition Lambda function.

Step 2: Lambda Function — Face Detection and Recognition
Triggered by:
S3 ObjectCreated event on new image uploads in the input/ folder.

Step-by-Step Breakdown of What This Lambda Does:
1. Read Image from S3
• Extracts bucket name and object key from the S3 event.
• Loads the image content using the boto3 S3 client.

2. Detect Faces using Amazon Rekognition
• Calls rekognition.detect_faces() or rekognition.search_faces_by_image()
• Receives response with:
o Number of faces detected
o Bounding boxes and facial landmarks
o Confidence score
o Emotions (if enabled)
o Matched FaceId and similarity % (if using face collection)

3. Store Recognition Result in DynamoDB (Table: FaceRecognitionResults)
• For each face or match found, creates a new record with fields:

image_id: The image filename

timestamp: Processing time

face_id (if matched from collection)

confidence: Match or detection confidence

bounding_box: Face location in the image

emotions (optional): Top 1 or top 3 emotions
• Why use DynamoDB?
o Real-time query support
o Scalable and low-latency
o Filter by user/face, time, or status

4. Store Enriched Metadata in S3 /processed/ Folder
• A .json file is created per image under:
s3://face-input-bucket/processed/image1.json
• Contains:
o File metadata (name, time, etc.)
o Detected faces and confidence
o Emotions and landmarks
o Face IDs (if applicable)

Output of this Lambda:
• ✅ Recognition metadata stored in DynamoDB
• ✅ Enriched .json stored in /processed/
• ✅ Logs available in CloudWatch for monitoring and debugging

Step 3 (Optional): Face Enrollment for Rekognition Face Collection
Purpose:
To enroll known individuals into an Amazon Rekognition face collection for future matching.

How it works:
• Upload a labeled image (e.g., john_doe.jpg) to an enrollment S3 path or via API.
• Lambda function uses rekognition.index_faces() to register face.
• Metadata such as ExternalImageId (e.g., "John Doe") is associated.
• Faces are added to a collection like my-face-collection.

Why enroll faces?
• Enables identification (not just detection) of known individuals.
• Useful for employee attendance, VIP detection, etc.

Output:
• New face indexed in Rekognition with a FaceId.
• Logs stored in CloudWatch.
• Indexed faces searchable by similarity.

Step 4: Visualization and Monitoring
Purpose:
To view logs, recognition outcomes, or monitor face detection trends.

Options:
• CloudWatch Logs
o Lambda execution logs
o Rekognition API responses
o Errors or failures
o Latency metrics

• Athena + S3 (Optional)
o Query processed S3 JSON files
o Build dashboards on top of them

• Streamlit/Dash App (Optional)
o Load data from DynamoDB
o Display faces detected, emotions, timestamps, etc.
o Filter by person or upload time

Summary Table
Step	Service/Component	Action/Trigger	Output/Next Step
1	Amazon S3	Image uploaded to input/	Triggers Lambda
2	Lambda (S3 Trigger)	Detects face(s) using Rekognition	Stores results in DynamoDB, S3
3	Rekognition Face Indexing	Enroll known faces (optional)	Stored in Rekognition collection
4	CloudWatch / Athena	View logs, run queries	Debugging / analytics / dashboard
