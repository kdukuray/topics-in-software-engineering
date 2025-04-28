#!/bin/bash

# Usage: ./deploy.sh v1
# Example: ./deploy.sh v1

set -e

VERSION=$1
APP_NAME="django-app"          # Elastic Beanstalk app name
ENV_NAME="django-env"           # Elastic Beanstalk environment name
S3_BUCKET="terraform-state-ledgerpay-kdukuray-assignment-3"

ZIP_FILE="ledgerpay_deploy-${VERSION}.zip"

echo "Packaging Django application..."

# Clean up old zip
rm -f $ZIP_FILE

# 1. First cd into the ledgerpay/ folder where manage.py etc. are
cd ledgerpay

# 2. Create the zip
zip -r "../$ZIP_FILE" ledgerpay payments manage.py ../requirements.txt ../application.py \
  -x "*.git*" ".venv/*" "*.venv/*" "*.sqlite3" "*.orig" "*.pyc" "__pycache__/*" ".pytest_cache/*" "htmlcov/*" "terraform/*" "demo_app/*" "documentation/*"

# 3. Go back up
cd ..

echo "Uploading package to S3 bucket..."

aws s3 cp "$ZIP_FILE" s3://$S3_BUCKET

echo "Creating a new Elastic Beanstalk application version..."

aws elasticbeanstalk create-application-version \
  --application-name $APP_NAME \
  --source-bundle S3Bucket="$S3_BUCKET",S3Key="$ZIP_FILE" \
  --version-label "ver-$VERSION" \
  --description "Deploy version $VERSION" \
  --region "us-east-2"

echo "Updating Elastic Beanstalk environment..."

aws elasticbeanstalk update-environment \
  --environment-name $ENV_NAME \
  --version-label "ver-$VERSION" \
  --region "us-east-2"

echo "Deployment complete!"
