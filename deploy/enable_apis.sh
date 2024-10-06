# Enable the necessary APIs for the project
gcloud services enable cloudbuild.googleapis.com \
  cloudfunctions.googleapis.com \
  run.googleapis.com logging.googleapis.com \
  storage-component.googleapis.com \
  aiplatform.googleapis.com