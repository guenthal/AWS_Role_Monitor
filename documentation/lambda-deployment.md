# Lambda Function Deployment

This document outlines the steps to deploy the Lambda function for IAM role monitoring.

## Deployment Steps

1. Created an IAM role with necessary permissions
2. Installed Python dependencies locally
3. Created a ZIP deployment package
4. Deployed the Lambda function with configuration:
   - Runtime: Python 3.9
   - Handler: lambda_function.lambda_handler
   - Environment Variables:
     - SNS_TOPIC_ARN: The ARN of the SNS topic for notifications
   - Timeout: 30 seconds (CloudTrail logs can be large)

## Function Configuration

The Lambda function is configured with:
- Memory: 128 MB (default)
- Timeout: 30 seconds
- Environment Variables:
  - SNS_TOPIC_ARN: Points to the IAMRoleChangeAlerts SNS topic
