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

ENV_VARS="DJANGO_DEBUG=false,TZ=Europe/Madrid,GS_BUCKET_NAME=auryapp-media"

# DATABASE_URL y DJANGO_SECRET_KEY NO se envían: Cloud Run conserva las que ya tiene (y que funcionan).
# Así un .env.deploy desactualizado en algún equipo no puede dejar la web sin base de datos ni
# cerrar la sesión de todos. Para cambiarlas a propósito: ENVIAR_CREDENCIALES=1 bash deploy.sh
if [ "${ENVIAR_CREDENCIALES:-}" = "1" ]; then
  echo "AVISO: se envían DATABASE_URL y DJANGO_SECRET_KEY de .env.deploy a Cloud Run"
  ENV_VARS="${ENV_VARS},DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY},DATABASE_URL=${DATABASE_URL}"
fi

# Clima: solo se envían si están en .env.deploy. Con --update-env-vars, si no se envían,
# Cloud Run conserva los valores que ya tenía (p. ej. los puestos desde el otro equipo).
for v in CLUB_LATITUDE CLUB_LONGITUDE CLUB_CITY; do
  [ -n "${!v}" ] && ENV_VARS="${ENV_VARS},${v}=${!v}"
done

# Copia de seguridad de PRODUCCIÓN antes de desplegar (el contenedor nuevo migra al arrancar).
# Se guarda en backups/ (ignorada por git y por Docker). Si la copia falla, no se despliega.
# Para desplegar sin copia (solo si sabes lo que haces): SIN_COPIA=1 bash deploy.sh
if [ "${SIN_COPIA:-}" != "1" ]; then
  PY=venv/bin/python
  [ -x "$PY" ] || PY=python3
  echo "Copia de seguridad de producción antes de desplegar..."
  # Hasta 3 intentos: si Neon está archivada por inactividad, la primera conexión puede fallar
  copia_ok=0
  for intento in 1 2 3; do
    # PGCONNECT_TIMEOUT: si la base no responde, el intento falla a los 15 s en vez de quedarse colgado
    if DATABASE_URL="$DATABASE_URL" PGCONNECT_TIMEOUT=15 "$PY" manage.py exportar_copia --carpeta backups; then
      copia_ok=1; break
    fi
    [ "$intento" -lt 3 ] && { echo "Intento $intento fallido; reintento en 15 s..."; sleep 15; }
  done
  if [ "$copia_ok" != "1" ]; then
    echo "ERROR: la copia de seguridad ha fallado; NO se despliega."
    exit 1
  fi
fi

echo "Desplegando desde: $(pwd)"
gcloud run deploy auryapp --project auryapp-prod --source . --region europe-west1 --allow-unauthenticated \
  --update-env-vars="${ENV_VARS}"
