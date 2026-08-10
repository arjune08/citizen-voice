# Citizen Voice / WardPulse AI

A full-stack civic issue reporting platform built with Flask. Citizens can report local problems with photos and GPS coordinates, vote on issues, track status, and use optional AI assistance. Ward officers and admins get a management dashboard.

## Highlights

- Citizen registration and secure login
- Civic issue reporting with image upload and GPS location
- AI-assisted category and priority detection
- Community voting and duplicate-issue handling
- Issue status tracking
- Interactive Leaflet/OpenStreetMap issue map
- Admin and ward-officer dashboard
- Excel/PDF exports
- Responsive UI with dark/light mode
- Optional Gemini AI and email integrations
- Production Gunicorn configuration
- Render Blueprint and Docker deployment files
- `/health` endpoint for deployment health checks

## Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Auth:** Flask-Login, Werkzeug password hashing, Flask-WTF CSRF
- **Frontend:** HTML, Tailwind CSS CDN, vanilla JavaScript
- **Database:** SQLite by default; PostgreSQL-compatible URI supported
- **Maps:** Leaflet + OpenStreetMap
- **AI:** Google Gemini API (optional)
- **Deployment:** Gunicorn, Docker, Render

## Run locally

### 1. Install

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env` and set at least a strong `SECRET_KEY`.

AI and email are optional. The application is designed to run without those credentials.

### 3. Start

```bash
python app.py
```

Open `http://localhost:5000`.

Health check: `http://localhost:5000/health`

### 4. Create an admin

```bash
flask --app app create-superadmin
```

Follow the prompts.

## Production deployment

### Render

This repository includes `render.yaml`. In Render, create a new Blueprint from the repository. The service installs dependencies and starts with Gunicorn.

Required/optional environment variables can be added in the Render dashboard:

- `SECRET_KEY` — required; use a long random value
- `DATABASE_URI` — defaults to SQLite for a simple demo
- `GEMINI_API_KEY` — optional AI features
- `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_RECEIVER` — optional email notifications

**Important:** SQLite on a typical cloud web service is suitable for a hackathon demo but is not durable storage across every redeploy/restart. For production, use a managed PostgreSQL database and set `DATABASE_URI` to its connection string.

### Docker

```bash
docker build -t citizen-voice .
docker run --rm -p 5000:5000 -e SECRET_KEY=change-me citizen-voice
```

The container uses Gunicorn and listens on the `PORT` environment variable.

## Repository layout

```text
app.py
models.py
routes.py
requirements.txt
.env.example
Procfile
render.yaml
Dockerfile
static/
templates/
uploads/
```

## Security notes

- Never commit `.env` or real API/email credentials.
- Use a strong production `SECRET_KEY`.
- Keep uploaded files restricted to the configured extensions and size limit.
- For production workloads, use PostgreSQL and persistent object/file storage.

## Hackathon positioning

**Citizen Voice** turns citizen reports into structured, location-aware civic issues that authorities can prioritize and resolve. It is designed as an SIH-style prototype combining civic technology, AI, geospatial visualization, and an administrative workflow.
