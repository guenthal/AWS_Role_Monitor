# IAM Role for Lambda Function

This document describes the IAM role and policies needed for the Lambda function.

## Role Overview

The Lambda function requires permissions to:
1. Read CloudTrail log files from the S3 bucket
2. Publish notifications to the SNS topic
3. Write logs to CloudWatch Logs

## Creating the Role

```bash
# Create the IAM role
aws iam create-role \
    --role-name IAMRoleMonitorLambda \
    --assume-role-policy-document file://policies/lambda-trust-policy.json

# Attach permissions policy
aws iam put-role-policy \
    --role-name IAMRoleMonitorLambda \
    --policy-name LambdaPermissions \
    --policy-document file://policies/lambda-permissions-policy.json
