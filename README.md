# Face Recognition AWS

Built a real-time face recognition pipeline using Amazon S3, Lambda, and Rekognition to detect and identify faces from uploaded images. Recognition metadata is stored in DynamoDB for real-time querying and enriched recognition data is saved in S3. Monitoring is enabled through CloudWatch Logs and future analytics are supported via processed S3 output.

---

## Step 1: Image Ingestion using Amazon S3

**Purpose:**  
To upload user or surveillance images and initiate the face recognition process automatically.

**How it works:**  
- A user uploads an image to a designated S3 bucket (e.g., via mobile app, kiosk, surveillance system, or API).  
- The image is placed under the `input/` prefix (e.g., `s3://face-input-bucket/input/image1.jpg`).  
- The S3 bucket is configured to trigger a Lambda function on each new image upload.

**Why use S3?**  
- Durable, scalable storage for large image files.  
- Native event triggering for Lambda functions.  
- Easy integration with analytics tools like Athena and Glue.

**Output:**  
- A new image gets uploaded to S3.  
- Automatically triggers the recognition Lambda function.

---

## Step 2: Lambda Function — Face Detection and Recognition

**Triggered by:**  
S3 `ObjectCreated` event on new image uploads in the `input/` folder.

**Step-by-Step Breakdown of What This Lambda Does:**  

1. **Read Image from S3**  
   - Extracts bucket name and object key from the S3 event.  
   - Loads the image content using the boto3 S3 client.  

2. **Detect Faces using Amazon Rekognition**  
   - Calls `rekognition.detect_faces()` or `rekognition.search_faces_by_image()`.  
   - Receives response with:  
     - Number of faces detected  
     - Bounding boxes and facial landmarks  
     - Confidence score  
     - Emotions (if enabled)  
     - Matched FaceId and similarity % (if using a face collection)  

3. **Store Recognition Result in DynamoDB (Table: `FaceRecognitionResults`)**  
   - For each face or match found, creates a new record with fields:  
     - `image_id`: The image filename  
     - `timestamp`: Processing time  
     - `face_id` (if matched from collection)  
     - `confidence`: Match or detection confidence  
     - `bounding_box`: Face location in the image  
     - `emotions` (optional): Top 1 or top 3 emotions  

   **Why use DynamoDB?**  
   - Real-time query support  
   - Scalable and low-latency  
   - Filter by user/face, time, or status  

4. **Store Enriched Metadata in S3 `/processed/` Folder**  
   - A `.json` file is created per image under:  
     `s3://face-input-bucket/processed/image1.json`  
   - Contains:  
     - File metadata (name, time, etc.)  
     - Detected faces and confidence  
     - Emotions and landmarks  
     - Face IDs (if applicable)  

**Output of this Lambda:**  
- ✅ Recognition metadata stored in DynamoDB  
- ✅ Enriched `.json` stored in `/processed/`  
- ✅ Logs available in CloudWatch for monitoring and debugging

---

## Step 3 (Optional): Face Enrollment for Rekognition Face Collection

**Purpose:**  
To enroll known individuals into an Amazon Rekognition face collection for future matching.

**How it works:**  
- Upload a labeled image (e.g., `john_doe.jpg`) to an enrollment S3 path or via API.  
- Lambda function uses `rekognition.index_faces()` to register face.  
- Metadata such as `ExternalImageId` (e.g., "John Doe") is associated.  
- Faces are added to a collection like `my-face-collection`.

**Why enroll faces?**  
- Enables identification (not just detection) of known individuals.  
- Useful for employee attendance, VIP detection, etc.

**Output:**  
- New face indexed in Rekognition with a FaceId.  
- Logs stored in CloudWatch.  
- Indexed faces searchable by similarity.

---

## Step 4: Visualization and Monitoring

**Purpose:**  
To view logs, recognition outcomes, or monitor face detection trends.

**Options:**  
- **CloudWatch Logs**  
  - Lambda execution logs  
  - Rekognition API responses  
  - Errors or failures  
  - Latency metrics  

- **Athena + S3 (Optional)**  
  - Query processed S3 JSON files  
  - Build dashboards on top of them  

- **Streamlit/Dash App (Optional)**  
  - Load data from DynamoDB  
  - Display faces detected, emotions, timestamps, etc.  
  - Filter by person or upload time  

---

## Summary Table

| Step | Service/Component          | Action / Trigger                              | Output / Next Step                              |
|-------|--------------------------|----------------------------------------------|------------------------------------------------|
| 1     | Amazon S3                 | Image uploaded to `input/`                    | Triggers Lambda                                |
| 2     | Lambda (S3 Trigger)       | Detects face(s) using Rekognition             | Stores results in DynamoDB and S3               |
| 3     | Rekognition Face Indexing | Enroll known faces (optional)                  | Stored in Rekognition collection                 |
| 4     | CloudWatch / Athena       | View logs, run queries                         | Debugging, analytics, dashboards                 |

---

## Additional Notes

- Ensure proper IAM roles and policies are assigned to Lambda for access to S3, DynamoDB, and Rekognition.  
- Configure S3 event notifications to trigger Lambda on specific prefixes like `input/`.  
- Adjust DynamoDB table schema based on your application's querying needs.  
- Monitor CloudWatch logs regularly for failures or throttling.  
- Use Step Functions if chaining multiple Lambdas or for enhanced workflow orchestration.

---

Feel free to enhance this README with deployment instructions, architecture diagrams, or sample API requests based on your repo/project needs.

---

**Happy face recognizing!** 😃

