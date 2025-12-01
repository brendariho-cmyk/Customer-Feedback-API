# 🟩 Serverless Feedback API (AWS API Gateway + Lambda + DynamoDB)

A fully serverless backend API that allows users to submit feedback securely and at scale.  
Designed using AWS Lambda, DynamoDB, and API Gateway — demonstrating modern cloud-native architecture with zero servers to manage.


---


## **1. Business Problem: Collecting User Feedback at Scale**

Small businesses and startups often need a simple way to collect customer feedback, but:

- They don’t want to maintain servers
- Traffic can be unpredictable (sometimes 2 submissions a day, sometimes 500)
- They need reliability without paying for unused resources
- Feedback must be stored securely for future review

Traditional backend servers are costly, fragile, and require constant maintenance.


---


## **2. Solution Overview**

This project provides a **fully serverless feedback submission API** using:

- **Amazon API Gateway** — public HTTPS endpoint  
- **AWS Lambda** — backend logic with automatic scaling  
- **Amazon DynamoDB** — NoSQL database for storing feedback  
- **IAM Roles & Policies** — secure service-to-service communication  

The architecture scales instantly from **0 to thousands of requests**, with zero maintenance.

---

## **3. Architecture Diagram**

*(Place your diagram image in `/architecture-diagram/diagram.png`)*





---

## **4. Components**

### **API Layer**
- **Amazon API Gateway**
  - POST /feedback endpoint
  - Validates input
  - Triggers Lambda function

### **Compute Layer**
- **AWS Lambda Function**
  - Python function
  - Parses request JSON
  - Writes data to DynamoDB
  - Returns API response

### **Database Layer**
- **DynamoDB Table: `Feedback`**
  - Partition Key: `feedbackId` (UUID)
  - Stores name, email, message, and timestamp

### **Security**
- **IAM Role for Lambda**
  - Attached policy: `dynamodb:PutItem` on Feedback table

---

## **5. How It Works (Flow)**

1. User submits feedback via HTTPS (webform or Postman).
2. API Gateway receives request.
3. API Gateway triggers the Lambda function.
4. Lambda validates JSON and inserts feedback into DynamoDB.
5. Lambda returns a success message back to the client.

---

## **6. Lambda Function Code**

```python
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Feedback')

def handler(event, context):
    body = json.loads(event['body'])
    
    item = {
        'feedbackId': str(uuid.uuid4()),
        'name': body.get('name'),
        'email': body.get('email'),
        'message': body.get('message'),
        'createdAt': datetime.utcnow().isoformat()
    }
    
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Feedback received!", "data": item})
    }

```
---
## **7. Infrastructure Details**

-**DynamoDB Table**
  -Name: Feedback
  -Partition key: feedbackId
  -Status: On-demand capacity mode
  -Region: eu-north-1 (Stockholm)

-**Lambda Function**
  -Runtime: Python 3.12+
  -Timeout: 10 seconds
  -Memory: 128 MB
  
-**API Gateway**
  -Method: POST
  -Content-Type: JSON
  -Integrated with Lambda proxy

---

## **8. Testing Performed**
-**1. lambda direct test**
  -Triggered manually with test JSON
  -Verified successful response

(Screenshots in /screenshots/lambda-tests/)

-**2. API Gateway test**
  -Used “Test” feature inside API Gateway
  -Sent JSON payload
  -Confirmed valid statusCode 200

(Screenshots in /screenshots/api-tests/)

-**3. DynamoDB verification**
  -Confirmed new items appear in console
  -Confirmed auto-generated UUIDs

(Screenshots in /screenshots/dynamodb/)

-**4. External request test**
  -Tested via Postman/ReqBin
  -Verified public endpoint
  -Received correct JSON response

(Screenshots in /screenshots/postman/)

---

## **9. Cost Considerations**

-Lambda: Charged per millisecond, free for first 1M requests/month
-API Gateway: Small per-request cost
-DynamoDB: On-demand mode ideal for small apps
-Total monthly cost in small usage: Under $1

---

## **10. What I Would Improve (Future Enhancements)**

-Add CORS to allow web apps to call API
-Add GET /feedback endpoint for retrieving data
-Add email notifications using AWS SNS
-Add schema validation using API Gateway models
-Add CloudWatch alarms for error tracking
-Add S3 + static site to build a simple frontend form
-Add Terraform/CDK to automate provisioning

---

## **11. How to Reproduce This Project**

-**Checklist:**
1. Create DynamoDB Table (Feedback)
2. Create Lambda Function + IAM Role
3. Add DynamoDB write permissions
4. Paste code
5. Create API Gateway REST API
6. Add POST /feedback route
7. Integrate Lambda
8. Deploy API to “prod”
9. Test with Postman / API Gateway

---

## **12. Conclusion**

This project demonstrates AWS serverless skills:

✔ Building secure, scalable APIs
✔ Writing Lambda functions
✔ Integrating DynamoDB
✔ Handling JSON requests
✔ Designing cloud-native backend architecture
