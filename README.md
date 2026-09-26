<div align="right">
  <img src="https://img.shields.io/badge/EN-1a6fc4?style=flat-square" alt="English">
  &nbsp;<a href="README.es.md"><img src="https://img.shields.io/badge/ES-555555?style=flat-square" alt="Español"></a>
</div>

# AuryApp

Full-stack Django web app built for a real beach club, actively used in production. Covers event management, staff scheduling, daily operations and more — with a custom design system.

**Developed by [Fernando Vilas Paz](https://github.com/fvilpaz)**

---

## Features

- **Dashboard** — Daily overview: live weather with a 6-hour forecast, upcoming events, today's tasks, active staff
- **Events** — Full event management (weddings, graduations, communions, galas and more) with file attachments, a visual floor plan editor, staff ranges and assigned waiters, and a recycle bin to restore deleted events
- **Floor Plan Editor** — Drag-and-drop visual layout builder (Fabric.js) per event. Click-to-place elements, multi-select with bulk delete and colour change, pax badge on each table, entrance/exit labels always horizontal
- **Schedule** — Weekly shift view per employee, with a colour per employee, contract hours and custom ordering
- **Staff** — Employee profiles, roles, contracts and expiry alerts
- **Overtime** — Per-employee overtime log (rounded to the half hour), grouped by month, monthly settlement and pending hours shown in the staff list
- **Venues** — Assign staff to each venue for the day
- **Time Off** — Holiday and day-off requests, approval and tracking
- **Tasks** — Opening/closing checklists per venue, updated in real time
- **Agenda** — Priority notes (urgent / moderate / normal), resolution and voice dictation
- **Orders** — Stock tracking per point of sale
- **Calendar** — Monthly event view with FullCalendar, synced with Events module
- **Themes** — 6 visual themes (Light, Dark, Mint, Barbie, Dracula, Cyberpunk)
- **User Registration** — Sign-up form with name, username, email and password
- **Admin Panel** — Direct access to Django admin from the navbar (staff only)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.3 |
| Database | PostgreSQL (Neon) in production · SQLite locally |
| Frontend | Custom CSS with variables, Tabler Icons, Fabric.js |
| Server | Gunicorn + WhiteNoise |
| Deploy | Google Cloud Run |
| Storage | Google Cloud Storage |
| Security | django-axes (lockout after 5 failed login attempts) |

---

## Local Setup

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

Access at `http://localhost:8000`

### Sample data (optional)

```bash
python data/personal.py
python data/eventos.py
python data/tareas.py
python data/turnos.py
```

> The `data/` scripts have the project path hard-coded (`sys.path.insert(...)`): adjust it if you clone elsewhere.
> `data/import_turnos.py` imports the Excel file `data/turnos.xlsx` (not in the repo, confidential data) and needs `pip install openpyxl`.

### Tests

```bash
python manage.py test
```

Uses an in-memory database: `db.sqlite3` is not touched.

---

## Environment Variables (production)

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=false
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
TZ=Europe/Madrid
GS_BUCKET_NAME=your-bucket-name

# Location for the weather widget (optional, these are the defaults)
CLUB_LATITUDE=39.47
CLUB_LONGITUDE=-0.38
CLUB_CITY=Benalmádena
```

Without `DATABASE_URL` the app uses a local `db.sqlite3`.

---

## Deployment (Google Cloud Run)

Includes `Dockerfile` and `deploy.sh`. Credentials are stored in `.env.deploy` (local only, never committed).

```bash
bash deploy.sh      # Linux / WSL
deploy.bat          # Windows (runs deploy.sh inside WSL)
```

- Python 3.12 slim container
- Migrations run automatically on container start (`migrate --noinput`)
- Static files served by WhiteNoise
- User uploads (event documents) stored in Google Cloud Storage
- Serverless PostgreSQL on Neon (Frankfurt)

---

## Security

- Login required on all routes (custom middleware)
- Automatic lockout after 5 failed login attempts (1-hour cooldown)
- Session expires on browser close and after 8 hours maximum
- CSRF, XSS and clickjacking protection enabled
- Content Security Policy (CSP), HSTS, Referrer-Policy and Permissions-Policy headers
- File upload validation: extension whitelist + magic bytes check
- SSL enforced in production

---

## License

Private project. All rights reserved.  
© 2026 Fernando Vilas Paz
