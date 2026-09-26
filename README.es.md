<div align="right">
  <a href="README.md"><img src="https://img.shields.io/badge/EN-555555?style=flat-square" alt="English"></a>
  &nbsp;<img src="https://img.shields.io/badge/ES-1a6fc4?style=flat-square" alt="Español">
</div>

# AuryApp

Aplicación web de gestión integral para beach club. Desarrollada con Django, diseño propio y orientada a uso real en entornos de hostelería y eventos.

**Desarrollado por [Fernando Vilas Paz](https://github.com/fvilpaz)**

---

## Funcionalidades

- **Dashboard** — Resumen del día: clima en vivo con previsión de las próximas 6 horas, eventos próximos, tareas del día, personal trabajando
- **Eventos** — Gestión completa de bodas, graduaciones, comuniones, galas y más. Con documentos adjuntos, editor visual de plano de mesas, rangos y camareros asignados, y papelera para restaurar eventos borrados
- **Plano de mesas** — Editor visual (Fabric.js) para diseñar la distribución de espacios de cada evento. Colocación por clic, selección múltiple con borrado y cambio de color en bloque, badge de pax en cada mesa, etiquetas de entradas/salidas siempre horizontales
- **Cuadrante** — Vista semanal de turnos por empleado, con color propio por empleado, horas de contrato y orden personalizable
- **Personal** — Fichas de empleados, roles, contratos y alertas de vencimiento
- **Horas extra** — Registro por empleado (redondeo a la media hora), agrupadas por mes, liquidación mensual y horas pendientes visibles en la lista de empleados
- **Espacios** — Asignación de empleados a cada espacio del día
- **Vacaciones y días sueltos** — Solicitudes, aprobación y seguimiento
- **Tareas** — Checklists de apertura/cierre por espacio, actualizables en tiempo real
- **Agenda** — Notas con prioridad (urgente / moderado / normal), resolución y dictado por voz
- **Pedidos** — Registro de artículos necesarios por punto de venta
- **Calendario** — Vista mensual de eventos con FullCalendar, sincronizado con el módulo de Eventos
- **Temas** — 6 temas visuales (Claro, Oscuro, Mint, Barbie, Drácula, Cyberpunk)
- **Alta de usuarios** — Solo staff crea cuentas nuevas (nombre, apellidos, usuario, email y contraseña) desde el menú de usuario → *Crear cuenta*; no hay registro público
- **Copia de seguridad** — Menú de usuario → *Descargar copia* (solo staff): un JSON con todos los datos (eventos con sus planos de mesas y el detalle de cada mesa, empleados, turnos, horas extra, ausencias, tareas, agenda y pedidos) y los usuarios **sin contraseñas**. Los documentos adjuntos de eventos están en Cloud Storage: la copia guarda su referencia, no el fichero
- **Panel de administración** — Acceso directo al admin de Django desde la navbar (solo staff)

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6.0.3 |
| Base de datos | PostgreSQL (Neon) en producción · SQLite en local |
| Frontend | CSS propio con variables, Tabler Icons, Fabric.js |
| Servidor | Gunicorn + WhiteNoise |
| Deploy | Google Cloud Run |
| Almacenamiento | Google Cloud Storage |
| Seguridad | django-axes (bloqueo tras 5 intentos fallidos) |

---

## Instalación local

```bash
git clone https://github.com/fvilpaz/auryapp.git
cd auryapp

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accede en `http://localhost:8000`

### Datos de ejemplo (opcional)

```bash
python data/personal.py
python data/eventos.py
python data/tareas.py
python data/turnos.py
```

> Los scripts de `data/` tienen la ruta del proyecto escrita dentro (`sys.path.insert(...)`): ajústala si clonas en otra carpeta.
> `data/import_turnos.py` importa el Excel `data/turnos.xlsx` (no está en el repositorio, datos confidenciales) y necesita `pip install openpyxl`.

### Tests

```bash
python manage.py test
```

### Copia de seguridad desde la terminal

```bash
python manage.py exportar_copia --carpeta ruta/destino
```

Guarda `auryapp-AAAA-MM-DD.json` de la base a la que apunte `DATABASE_URL` (SQLite si no está definida).

Usa una base de datos en memoria: no toca `db.sqlite3`.

---

## Variables de entorno (producción)

```env
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=false
DATABASE_URL=postgresql://usuario:password@host/db?sslmode=require
TZ=Europe/Madrid
GS_BUCKET_NAME=nombre-del-bucket

# Ubicación para el widget del clima (opcionales, estos son los valores por defecto)
CLUB_LATITUDE=39.47
CLUB_LONGITUDE=-0.38
CLUB_CITY=Benalmádena
```

Sin `DATABASE_URL` la app usa `db.sqlite3` en local.

---

## Despliegue en Google Cloud Run

El proyecto incluye `Dockerfile` y `deploy.sh`. Las credenciales se guardan en `.env.deploy` (local, nunca en el repositorio).

```bash
bash deploy.sh      # Linux / WSL
deploy.bat          # Windows (ejecuta deploy.sh dentro de WSL)
```

- Contenedor Python 3.12 slim
- Las migraciones se aplican solas al arrancar el contenedor (`migrate --noinput`)
- Archivos estáticos gestionados por WhiteNoise
- Archivos de usuario (documentos de eventos) en Google Cloud Storage
- Base de datos PostgreSQL serverless en Neon (Frankfurt)

---

## Seguridad

- Autenticación obligatoria en todas las rutas (middleware personalizado)
- Bloqueo automático tras 5 intentos de login fallidos (1 hora de cooldown)
- Sesión expira al cerrar el navegador y tras 8 horas máximo
- Protección CSRF, XSS y clickjacking activadas
- Cabeceras Content Security Policy (CSP), HSTS, Referrer-Policy y Permissions-Policy
- Validación de subida de ficheros: whitelist de extensiones + comprobación de magic bytes
- SSL obligatorio en producción

---

## Licencia

Proyecto privado. Todos los derechos reservados.  
© 2026 Fernando Vilas Paz
