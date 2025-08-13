#!/usr/bin/env bash
set -euo pipefail

gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/eob-backend ./backend
gcloud run deploy eob-backend --image gcr.io/$GCP_PROJECT_ID/eob-backend --region=$GCP_REGION --allow-unauthenticated

gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/eob-frontend ./frontend
gcloud run deploy eob-frontend --image gcr.io/$GCP_PROJECT_ID/eob-frontend --region=$GCP_REGION --allow-unauthenticated
