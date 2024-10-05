#!/bin/bash

# Set Environment Variables
export PROJECT_ID=vegax-429008
export REGION=asia-northeast3
export IMAGE_URL="$REGION-docker.pkg.dev/$PROJECT_ID/file-drive/file-drive:v1.0"
export SERVICE_ACCOUNT="compute-engine@$PROJECT_ID.iam.gserviceaccount.com"
export DATABASE_URL='postgresql+psycopg2://admin:y7jHf&DNWG15@10.0.0.3:5030/main'

# create a secret using secret manager for the database URL
echo -n $DATABASE_URL | \
gcloud secrets versions add DATABASE_URL --data-file=-

# Deploy Cloud Run Service
gcloud run deploy demo-app \
  --image $IMAGE_URL \
  --platform managed \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT \
  --vpc-connector demo-app-connector \
  --allow-unauthenticated \