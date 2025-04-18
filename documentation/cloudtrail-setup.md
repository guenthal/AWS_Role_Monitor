# CloudTrail Setup

This document outlines the steps taken to set up CloudTrail for monitoring IAM activity.

## Steps Performed

1. Created an S3 bucket to store CloudTrail logs
2. Enabled versioning on the bucket for added security
3. Applied a bucket policy to allow CloudTrail to write logs to the bucket
4. Created a CloudTrail trail named 'IAMActivityTrail' configured to:
   - Monitor all regions
   - Validate log file integrity
   - Store logs in the specified S3 bucket
5. Started logging with the trail

This trail captures all management events (API calls) related to IAM resources, including:
- Role creation and deletion
- Policy attachments
- Permission changes
- Trust relationship modifications

The logs are stored in the S3 bucket in the following structure:
`s3://your-unique-bucket-name/AWSLogs/[account-id]/CloudTrail/[region]/[year]/[month]/[day]/`
