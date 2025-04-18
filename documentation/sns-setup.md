# SNS Topic Setup for Notifications

This document describes the setup of an Amazon SNS topic to receive notifications about IAM role changes.

## Steps Performed

1. Created an SNS topic named 'IAMRoleChangeAlerts'
2. Subscribed an email address to receive notifications
3. Confirmed the subscription via the email link

## How Notifications Work

1. The Lambda function (to be created) will detect IAM role changes in CloudTrail logs
2. When a change is detected, the Lambda function will publish a message to the SNS topic
3. SNS will send an email to subscribers
4. The email will contain details about the IAM role change

## Managing Subscriptions

To add more email subscribers:
aws sns subscribe 
--topic-arn <your-topic-arn> 
--protocol email 
--notification-endpoint another-email@example.com

To list existing subscriptions:
aws sns list-subscriptions-by-topic --topic-arn <your-topic-arn>
