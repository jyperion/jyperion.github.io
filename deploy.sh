#!/bin/bash

# Set the project ID and bucket name
PROJECT_ID="coherent-surf-442516-q3"
BUCKET_NAME="personal.teach-ai.net"

# Ensure we're using the correct project
gcloud config set project ${PROJECT_ID}

# Deploy to Google Cloud Storage
echo "Deploying to ${BUCKET_NAME}..."
gsutil -m cp -r * gs://${BUCKET_NAME}/

# Set metadata for files
echo "Setting metadata for files..."
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" gs://${BUCKET_NAME}/*.html
gsutil -m setmeta -h "Cache-Control:public, max-age=86400" gs://${BUCKET_NAME}/*.{css,js}
gsutil -m setmeta -h "Cache-Control:public, max-age=2592000" gs://${BUCKET_NAME}/*.{png,jpg,jpeg,gif,ico}

# Configure website
echo "Configuring website settings..."
gsutil web set -m index.html -e 404.html gs://${BUCKET_NAME}

# Set CORS policy
echo "Setting CORS policy..."
gsutil cors set cors.json gs://${BUCKET_NAME}

echo "Deployment complete!"
echo "Your website should be available at: https://storage.googleapis.com/${BUCKET_NAME}/index.html"
echo "Once DNS is configured, it will be available at: https://${BUCKET_NAME}"
echo "Note: DNS changes may take up to 48 hours to propagate fully."
echo ""
echo "IMPORTANT: Please configure bucket permissions in the Google Cloud Console:"
echo "1. Go to Cloud Console > Storage > Buckets > ${BUCKET_NAME}"
echo "2. Click on 'PERMISSIONS'"
echo "3. Add a new principal with these settings:"
echo "   - Principal: allUsers"
echo "   - Role: Storage Object Viewer"
