#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-slack-financial-reporter}"
REGION="${REGION:-us-east1}"
SERVICE_NAME="slack-financial-reporter"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

if [[ "$PROJECT_ID" == "your-gcp-project-id" ]]; then
  echo "Set PROJECT_ID first: export PROJECT_ID=your-project-id"
  exit 1
fi

gcloud auth login

gcloud config set project "$PROJECT_ID"

gcloud builds submit --tag "$IMAGE" .

gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "TIMEZONE=America/New_York,MESSAGE_TIME=09:30" \
  --set-secrets "SLACK_BOT_TOKEN=slack-bot-token:latest,SLACK_CHANNEL_ID=slack-channel-id:latest"

echo "Deploy complete."
echo "Cloud Run URL:"
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format='value(status.url)'

echo "Next: create a Cloud Scheduler job that triggers this URL daily at 09:30 ET."
