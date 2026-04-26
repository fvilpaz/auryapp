#!/bin/bash
cd /home/nando/code/github/auryapp
gcloud run deploy auryapp --source . --region europe-west1 --allow-unauthenticated \
  --set-env-vars="DJANGO_SECRET_KEY=hEcTbGDYB23V43XzLI709gz0iOOkKu7e0wKJDX9oWzcYakJMSxYxtvclaa-xIlhwz4s,DJANGO_DEBUG=false,DATABASE_URL=postgresql://neondb_owner:npg_Btm1PaJRECQ8@ep-small-dream-al3oqgs4.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require,TZ=Europe/Madrid"
