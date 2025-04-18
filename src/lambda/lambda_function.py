import json
import boto3
import gzip
import logging
from io import BytesIO
import os

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Get SNS topic ARN from environment variable
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

# List of IAM events to monitor
IAM_ROLE_EVENTS = [
    "AttachRolePolicy", 
    "DetachRolePolicy",
    "CreateRole",
    "DeleteRole",
    "UpdateRole",
    "UpdateAssumeRolePolicy",
    "PutRolePolicy",
    "DeleteRolePolicy"
]

def lambda_handler(event, context):
    """
    Lambda function handler to process CloudTrail logs for IAM role assignments
    """
    logger.info('Processing CloudTrail event')
    
    # Get the S3 bucket and object key from the event
    try:
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_object_key = event['Records'][0]['s3']['object']['key']
        logger.info(f'Processing file {s3_object_key} from bucket {s3_bucket}')
        
        # Only process CloudTrail logs
        if not s3_object_key.endswith('.json.gz'):
            logger.info(f'Skipping non-CloudTrail file: {s3_object_key}')
            return {
                'statusCode': 200,
                'body': json.dumps('Not a CloudTrail log file')
            }
        
        # Get the object from S3
        response = s3_client.get_object(
            Bucket=s3_bucket,
            Key=s3_object_key
        )
        
        # Read the compressed data
        compressed_data = response['Body'].read()
        
        # Decompress the data
        with gzip.GzipFile(fileobj=BytesIO(compressed_data)) as gzipfile:
            json_data = gzipfile.read()
        
        # Parse the JSON data
        cloudtrail_events = json.loads(json_data)
        
        # Check if 'Records' exists in the CloudTrail events
        if 'Records' not in cloudtrail_events:
            logger.info('No Records found in CloudTrail events')
            return {
                'statusCode': 200,
                'body': json.dumps('No Records in CloudTrail events')
            }
        
        # Process each event in the CloudTrail log
        iam_role_changes = []
        for record in cloudtrail_events['Records']:
            event_name = record.get('eventName', '')
            
            # Check if this is an IAM role-related event we're interested in
            if event_name in IAM_ROLE_EVENTS:
                event_time = record.get('eventTime', 'Unknown time')
                source_ip = record.get('sourceIPAddress', 'Unknown IP')
                user_identity = record.get('userIdentity', {})
                
                username = user_identity.get('userName', 'Unknown user')
                if username == 'Unknown user' and 'arn' in user_identity:
                    # Extract username from ARN if possible
                    arn_parts = user_identity.get('arn', '').split('/')
                    if len(arn_parts) > 1:
                        username = arn_parts[-1]
                
                # Get affected resources from the request parameters
                request_parameters = record.get('requestParameters', {})
                role_name = request_parameters.get('roleName', 'Not specified')
                policy_arn = request_parameters.get('policyArn', 'Not specified')
                
                # Build message
                message = {
                    'eventTime': event_time,
                    'eventName': event_name,
                    'username': username,
                    'sourceIPAddress': source_ip,
                    'roleName': role_name,
                    'policyArn': policy_arn
                }
                
                iam_role_changes.append(message)
        
        # If we found IAM role changes, send SNS notifications
        if iam_role_changes:
            for change in iam_role_changes:
                subject = f"IAM Role Change Alert: {change['eventName']} by {change['username']}"
                message_body = json.dumps(change, indent=2)
                
                logger.info(f"Sending notification: {subject}")
                
                # Send the notification
                response = sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=subject,
                    Message=message_body
                )
                
                logger.info(f"SNS publish response: {response}")
        else:
            logger.info("No IAM role changes found in this CloudTrail log")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Processed {len(iam_role_changes)} IAM role changes')
        }
        
    except Exception as e:
        logger.error(f'Error processing CloudTrail log: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
