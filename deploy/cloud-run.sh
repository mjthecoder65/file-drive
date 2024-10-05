#!/bin/bash

# Set Environment Variables
export PROJECT_ID=vegax-429008
export REGION=asia-northeast3
export IMAGE_URL="$REGION-docker.pkg.dev/$PROJECT_ID/file-drive/file-drive:v1.0"
export SERVICE_ACCOUNT="compute-engine@$PROJECT_ID.iam.gserviceaccount.com"

# Deploy Cloud Run Service
gcloud run deploy demo-app \
  --image $IMAGE_URL \
  --platform managed \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT \
  --vpc-connector demo-app-connector \
  --allow-unauthenticated \