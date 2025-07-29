# Face Recognition AWS

Built a real-time face recognition pipeline using Amazon S3, Step Functions, Lambda, and Rekognition to detect and identify faces from uploaded images. Recognition metadata is stored in DynamoDB for real-time querying and enriched recognition data is saved in S3. Auto Scaling Groups (ASG) with EC2 instances are used for optional high-throughput processing, achieving a 0.5-second refresh rate and reducing recognition response time by 40%. Monitoring is enabled via CloudWatch Logs and Athena queries.

---

## Step 1: Image Ingestion using Amazon S3

**Purpose:**  
To upload user or surveillance images and automatically trigger the face recognition pipeline.

**How it works:**  
- A user uploads an image to a designated S3 bucket (e.g., via mobile app, kiosk, or API).  
- The image is placed under the `input/` prefix (e.g., `s3://face-input-bucket/input/image1.jpg`).  
- An S3 EventBridge rule detects this and triggers a **Step Functions state machine**.

**Why use S3?**  
- Durable, scalable storage for large image files.  
- Native integration with EventBridge for event-driven architecture.  
- Easy integration with analytics tools like Athena, Glue.

**Output:**  
- A new image triggers a Step Function.  
- The Step Function begins sequential Lambda-based processing.

---

## Step 2: Step Function Orchestration (2 Lambda Functions)

The Step Function runs two Lambda functions in sequence:

---

### ✅ Lambda 1: Face Detection using Amazon Rekognition

**Purpose:**  
To detect faces and facial attributes in the uploaded image.

**What it does:**  
- Reads the uploaded image from S3 (bucket + key passed via Step Function input).  
- Calls `rekognition.detect_faces()` or `rekognition.search_faces_by_image()`.  
- Parses the response for:  
  - Number of faces  
  - Bounding boxes, confidence, emotions  
  - Matched FaceId and similarity %

**Output to Step Function:**  
- JSON object containing face metadata, image info, and timestamp.

---

### ✅ Lambda 2: Store Results in DynamoDB and Enriched S3

**Purpose:**  
To persist the recognition results for future queries and analytics.

**What it does:**  
- Receives face metadata from Lambda 1.  
- Writes each face result to `FaceRecognitionResults` DynamoDB table.  
- Stores enriched results as `.json` in the `/processed/` folder of S3.

**Stored Metadata Includes:**  
- `image_id`, `timestamp`, `face_id`, `bounding_box`, `confidence`, `emotions`

**Why use DynamoDB + S3?**  
- DynamoDB for real-time querying  
- S3 `/processed/` for long-term storage and Athena querying

---

## Step 3: Scalable Inference with EC2 + Auto Scaling Group (Optional)

**Purpose:**  
To support advanced, high-throughput face recognition use cases that Lambda and Rekognition alone cannot handle.

**How it works:**  
- Images or metadata are optionally forwarded to an EC2-based microservice API (Flask/FastAPI).  
- This compute backend is managed by an **Auto Scaling Group**:
  - Launch Template with Amazon Linux 2 + OpenCV/TensorFlow  
  - Scaling policies: CPU > 60%, queue length, or invocation rate  
  - Supports up to 20+ EC2 instances during peak usage

**Performance Results:**  
- Achieved **0.5-second refresh rate** in dashboard visualizations  
- Reduced latency by **40%** under high load  
- Enhanced control for advanced image analysis (frame stitching, etc.)

---

## Step 4: Face Enrollment (Optional)

**Purpose:**  
To index known faces into a Rekognition collection for future identity matching.

**How it works:**  
- Upload labeled image to a separate S3 `enroll/` path or via UI/API  
- A Lambda function triggered or manually invoked runs `rekognition.index_faces()`  
- Associates `ExternalImageId` (e.g., “John Doe”) for face identity  
- Face gets added to `my-face-collection`

**Output:**  
- Rekognition FaceId stored in collection  
- Searchable by Rekognition in future uploads

---

## Step 5: Visualization and Monitoring

**Purpose:**  
To monitor image processing and visualize recognition data.

### Options:

- **CloudWatch Logs**  
  - Step Function state transitions  
  - Lambda execution logs  
  - Rekognition responses and failures  
  - Auto Scaling EC2 lifecycle events

- **Athena + S3 (Optional)**  
  - Query enriched `/processed/` JSON files  
  - Create ad hoc reports or dashboards

- **Streamlit or Dash (Optional)**  
  - Load data from DynamoDB or API  
  - Display real-time recognition results  
  - Supports polling or WebSocket refresh every **0.5 seconds**

---

## Summary Table

| Step | Component                  | Trigger / Action                                | Output                                  |
|------|----------------------------|--------------------------------------------------|-----------------------------------------|
| 1    | S3 + EventBridge           | Upload image to `input/`                         | Triggers Step Function                  |
| 2.1  | Lambda 1 (Detect Face)     | Rekognition face detection                       | Face data passed to Step Function       |
| 2.2  | Lambda 2 (Store Results)   | Write to DynamoDB + save to S3 `/processed/`     | Metadata saved                          |
| 3    | EC2 + Auto Scaling Group   | (Optional) API-based batch or advanced processing| Low-latency, horizontally scaled backend|
| 4    | Rekognition Face Indexing  | Enroll known faces                               | Added to Rekognition collection         |
| 5    | CloudWatch / Athena / UI   | Monitor and visualize                            | Logs, dashboards, real-time updates     |

---

## Additional Notes

- Step Function Input Format:
```json
{
  "bucket": "face-input-bucket",
  "key": "input/image1.jpg"
}

