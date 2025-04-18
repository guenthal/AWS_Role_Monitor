# AWS IAM Role Monitoring

A GRC (Governance, Risk, and Compliance) solution that monitors IAM role assignments in AWS using CloudTrail logs and sends notifications via SNS.

## Project Objectives
- Monitor IAM role assignments using CloudTrail
- Process logs with Lambda to identify important changes
- Send notifications via SNS
- Document the entire process for learning purposes

## Components
- CloudTrail for capturing IAM events
- S3 bucket for log storage
- Lambda function for log processing
- SNS for notifications

## Implementation Steps
1. Set up CloudTrail
2. Configure S3 for logs
3. Create Lambda function
4. Configure SNS notifications

