# S3 Event Notification Setup

This document describes how to configure the S3 bucket to trigger the Lambda function when new CloudTrail logs arrive.

## Configuration Steps

1. Granted permission for the S3 bucket to invoke the Lambda function
2. Created a notification configuration to:
   - Trigger on all object creation events (`s3:ObjectCreated:*`)
   - Only for files ending with `.json.gz` (CloudTrail log format)
   - Invoke our IAMRoleMonitor Lambda function

## How It Works

1. CloudTrail writes logs to the S3 bucket in compressed JSON format (`.json.gz`)
2. The S3 bucket notification configuration detects these new files
3. S3 invokes the Lambda function, passing details about the new file
4. The Lambda function processes the log file and sends notifications if IAM role changes are detected
