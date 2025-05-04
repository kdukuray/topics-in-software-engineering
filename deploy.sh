#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Navigate to the script directory (should be project root)
cd "$(dirname "$0")"

# Run database migrations
echo "Running Django migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Name of the output zip file
ZIP_FILE="ledgerpay-deploy.zip"

# Remove any existing zip file
rm -f $ZIP_FILE

# Create a zip archive of the project directory, excluding unnecessary files
echo "Creating deployment zip file..."
zip -r $ZIP_FILE . \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "__pycache__/*" \
    -x "*.sqlite3" \
    -x ".DS_Store" \
    -x "venv/*" \
    -x "staticfiles/*" \
    -x "media/*" \
    -x "tests/*" \
    -x "*/migrations/*" \
    -x "*.log" \
    -x "*.env" \
    -x "$ZIP_FILE"

echo "✅ Deployment zip created successfully: $ZIP_FILE"
