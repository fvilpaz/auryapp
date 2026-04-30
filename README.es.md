<div align="right">
  <a href="README.md">EN</a> &nbsp;|&nbsp; <a href="README.es.md"><strong>ES</strong></a>
</div>

# AuryApp

Aplicación web de gestión integral para beach club. Desarrollada con Django, diseño propio y orientada a uso real en entornos de hostelería y eventos.

**Desarrollado por [Fernando Vilas Paz](https://github.com/fvilpaz)**

---

## Funcionalidades

- **Dashboard** — Resumen del día: clima en vivo, eventos próximos, tareas del día, personal trabajando
- **Eventos** — Gestión completa de bodas, graduaciones, comuniones, galas y más. Con documentos adjuntos y editor visual de plano de mesas
- **Plano de mesas** — Editor visual (Fabric.js) para diseñar la distribución de espacios de cada evento
- **Cuadrante** — Vista semanal de turnos por empleado con drag & drop
- **Personal** — Fichas de empleados, roles, contratos y alertas de vencimiento
- **Vacaciones y días sueltos** — Solicitudes, aprobación y seguimiento
- **Tareas** — Checklists de apertura/cierre por espacio, actualizables en tiempo real
- **Agenda** — Notas con prioridad (urgente / moderado / normal), resolución y dictado por voz
- **Pedidos** — Registro de artículos necesarios por punto de venta
- **Calendario** — Vista mensual de eventos con FullCalendar, sincronizado con el módulo de Eventos
- **Temas** — 6 temas visuales (Claro, Oscuro, Mint, Barbie, Drácula, Cyberpunk)
- **Registro de usuarios** — Formulario de alta con nombre, apellidos, usuario, email y contraseña
- **Panel de administración** — Acceso directo al admin de Django desde la navbar (solo staff)

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Backend | Django 6.0.3 |
| Base de datos | PostgreSQL (Neon) |
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

---

## Variables de entorno (producción)

```env
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=false
DATABASE_URL=postgresql://usuario:password@host/db?sslmode=require
TZ=Europe/Madrid
GS_BUCKET_NAME=nombre-del-bucket
```

---

## Despliegue en Google Cloud Run

El proyecto incluye `Dockerfile` y `deploy.sh`. Las credenciales se guardan en `.env.deploy` (local, nunca en el repositorio).

```bash
bash deploy.sh
```

- Contenedor Python 3.12 slim
- Archivos estáticos gestionados por WhiteNoise
- Archivos de usuario (documentos de eventos) en Google Cloud Storage
- Base de datos PostgreSQL serverless en Neon (Frankfurt)

---

## Seguridad

- Autenticación obligatoria en todas las rutas (middleware personalizado)
- Bloqueo automático tras 5 intentos de login fallidos (1 hora de cooldown)
- Protección CSRF, XSS y clickjacking activadas
- SSL recomendado en producción

---

## Licencia

Proyecto privado. Todos los derechos reservados.  
© 2026 Fernando Vilas Paz
