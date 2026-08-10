# Citizen Voice

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
- Vercel serverless deployment configuration
- `/health` endpoint for deployment checks

## Stack

- **Backend:** Python, Flask, SQLAlchemy
- **Auth:** Flask-Login, Werkzeug password hashing, Flask-WTF CSRF
- **Frontend:** HTML, Tailwind CSS CDN, vanilla JavaScript
- **Database:** SQLite for local/demo; PostgreSQL-compatible URI supported
- **Maps:** Leaflet + OpenStreetMap
- **AI:** Google Gemini API (optional)
- **Deployment:** Vercel, with Render/Docker configs also retained

## Deploy to Vercel

1. Push this repository to GitHub.
2. In Vercel, choose **Add New → Project** and import `arjune08/citizen-voice`.
3. Vercel will detect `vercel.json` and use `api/index.py` as the Python serverless entrypoint.
4. Add environment variables in the Vercel project settings:

   - `SECRET_KEY` — use a long random value
   - `DATABASE_URL` or `DATABASE_URI` — recommended PostgreSQL connection string
   - `GEMINI_API_KEY` — optional
   - `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_RECEIVER` — optional
   - `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS` — optional

5. Deploy.
6. Verify `https://YOUR-DOMAIN/health` returns `{"status":"ok","service":"citizen-voice"}`.

### Vercel storage note

Vercel serverless functions do **not** provide durable local storage. If no database URL is configured, the app falls back to SQLite under `/tmp` only to keep a hackathon demo running. Data can disappear between serverless instances/redeployments.

For a real deployment, use managed PostgreSQL and persistent object storage for uploaded images. Do not rely on `/tmp` for permanent files.

## Run locally

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
python app.py
```

Open `http://localhost:5000`.

Health check: `http://localhost:5000/health`

Create an admin:

```bash
flask --app app create-superadmin
```

## Security

- Never commit `.env` or real API/email credentials.
- Use a strong production `SECRET_KEY`.
- Keep uploads restricted by extension and size.
- For production, use PostgreSQL and persistent object/file storage.

## Hackathon positioning

**Citizen Voice** turns citizen reports into structured, location-aware civic issues that authorities can prioritize and resolve. It is an SIH-style prototype combining civic technology, AI, geospatial visualization, and an administrative workflow.
