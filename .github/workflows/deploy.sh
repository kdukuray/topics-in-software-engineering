#!/bin/bash

# Package application into a zip file
zip -r "ledgerpay_deploy-$1.zip" ./ledgerpay manage.py requirements.txt .ebextensions ledgerpay/wsgi.py
# Adjust files above based on your application's needs

# Upload zip to S3
aws s3 cp "ledgerpay_deploy-$1.zip" s3://terraform-state-ledgerpay-gizmo1547

# Create new application version
aws elasticbeanstalk create-application-version \
  --application-name ledgerpay \
  --source-bundle S3Bucket="terraform-state-ledgerpay-gizmo1547",S3Key="ledgerpay_deploy-$1.zip" \
  --version-label "ver-$1" \
  --description "commit-sha-$1" \
  --region us-east-1

# Deploy to Elastic Beanstalk environment
aws elasticbeanstalk update-environment \
  --environment-name Django-environment \
  --version-label "ver-$1" \
  --region us-east-1