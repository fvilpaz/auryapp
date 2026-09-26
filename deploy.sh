#!/bin/bash
# Despliega en Cloud Run. Funciona desde cualquier carpeta y en cualquier equipo
# (WSL Arch del PC y el Linux del otro sitio): trabaja en la carpeta donde está este script.
# Desde Windows: doble clic en deploy.bat (llama a este mismo script dentro de WSL).
set -e
cd "$(dirname "$(readlink -f "$0")")"

if [ ! -f .env.deploy ]; then
  echo "ERROR: falta el archivo .env.deploy con las credenciales"
  exit 1
fi

source .env.deploy

for v in DJANGO_SECRET_KEY DATABASE_URL; do
  if [ -z "${!v}" ]; then
    echo "ERROR: $v está vacía en .env.deploy"
    exit 1
  fi
done

# gcloud puede no estar en el PATH si el script se lanza sin terminal interactiva
if ! command -v gcloud >/dev/null && [ -x "$HOME/google-cloud-sdk/bin/gcloud" ]; then
  export PATH="$HOME/google-cloud-sdk/bin:$PATH"
fi
command -v gcloud >/dev/null || { echo "ERROR: no encuentro gcloud"; exit 1; }

ENV_VARS="DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY},DJANGO_DEBUG=false,DATABASE_URL=${DATABASE_URL},TZ=Europe/Madrid,GS_BUCKET_NAME=auryapp-media"

# Clima: solo se envían si están en .env.deploy. Con --update-env-vars, si no se envían,
# Cloud Run conserva los valores que ya tenía (p. ej. los puestos desde el otro equipo).
for v in CLUB_LATITUDE CLUB_LONGITUDE CLUB_CITY; do
  [ -n "${!v}" ] && ENV_VARS="${ENV_VARS},${v}=${!v}"
done

echo "Desplegando desde: $(pwd)"
gcloud run deploy auryapp --project auryapp-prod --source . --region europe-west1 --allow-unauthenticated \
  --update-env-vars="${ENV_VARS}"
