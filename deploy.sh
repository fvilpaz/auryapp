#!/bin/bash
set -e
cd /home/fvilpaz/Data/coding/github/auryapp

if [ ! -f .env.deploy ]; then
  echo "ERROR: falta el archivo .env.deploy con las credenciales"
  exit 1
fi

source .env.deploy

gcloud run deploy auryapp --source . --region europe-west1 --allow-unauthenticated \
  --set-env-vars="DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY},DJANGO_DEBUG=false,DATABASE_URL=${DATABASE_URL},TZ=Europe/Madrid,GS_BUCKET_NAME=auryapp-media"
