# Lambda Function for IAM Role Monitoring

This document explains the Lambda function that processes CloudTrail logs to detect IAM role changes.

## Function Overview

The Lambda function:
1. Is triggered when new CloudTrail log files are added to the S3 bucket
2. Downloads and decompresses the CloudTrail log file
3. Parses the JSON contents
4. Filters for IAM role-related events
5. Extracts relevant information (who, what, when)
6. Sends notifications via SNS for each detected change

## Key Components

### Event Filtering
The function monitors these IAM role-related events:
- AttachRolePolicy: When a policy is attached to a role
- DetachRolePolicy: When a policy is detached from a role
- CreateRole: When a new IAM role is created
- DeleteRole: When an IAM role is deleted
- UpdateRole: When a role's description or max session duration is updated
- UpdateAssumeRolePolicy: When a role's trust relationship is modified
- PutRolePolicy: When an inline policy is added to a role
- DeleteRolePolicy: When an inline policy is removed from a role

### Information Extracted
For each event, the function extracts:
- Event time: When the change occurred
- Event name: What type of change was made
- Username: Who made the change
- Source IP: Where the change was made from
- Role name: Which role was affected
- Policy ARN: Which policy was involved (for policy-related events)
