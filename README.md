# 🌆 UrbanPulse AI

### From Citizen Reports to Smarter Urban Action

> **AI-powered civic intelligence for reporting, prioritising, mapping, and resolving urban infrastructure issues.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-Web%20Backend-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![SQL](https://img.shields.io/badge/Database-SQL-4479A1?logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![Deploy](https://img.shields.io/badge/Deploy-Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com/)

UrbanPulse AI is an SIH-style civic technology prototype that converts everyday citizen observations—**potholes, garbage, water leaks, drainage failures, damaged roads, and broken streetlights**—into structured, location-aware issues that can be prioritised and tracked through resolution.

## 🎯 The Problem

Urban issues are often reported through fragmented channels. Authorities may receive incomplete descriptions, duplicate complaints, poor location information, and little context about which problems need attention first.

**UrbanPulse AI creates one intelligent workflow:**

**Report → Understand → Prioritise → Map → Assign → Resolve**

## 💡 What the Platform Does

| Capability | Purpose |
|---|---|
| 📷 Civic reporting | Submit an issue with description, image, and location |
| 🧠 AI-assisted triage | Suggest issue category and priority |
| 📍 Geospatial mapping | Visualise reports and hotspots on a map |
| 👍 Community signals | Voting helps surface issues affecting more people |
| 🔁 Issue tracking | Follow progress from reported to resolved |
| 🏢 Admin workflow | Manage, assign, update, and verify issues |
| 📊 Civic analytics | Understand issue categories, status, and trends |
| 🔐 Secure accounts | Citizen/admin authentication and protected workflows |

## 🏗️ System Architecture

```text
┌──────────────────┐
│     CITIZEN      │
│ Web / Mobile UI  │
└────────┬─────────┘
         │ report + photo + location
         ▼
┌──────────────────┐
│   FLASK API      │
│ Validation/Auth  │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ AI-ASSISTED      │
│ TRIAGE            │
│ category/priority│
└────────┬─────────┘
         ▼
┌──────────────────┐       ┌──────────────────┐
│   SQL DATABASE   │◄─────►│ MAP / GEO DATA   │
│ users/issues/... │       │ Leaflet + OSM    │
└────────┬─────────┘       └──────────────────┘
         ▼
┌──────────────────┐
│ AUTHORITY        │
│ DASHBOARD        │
└────────┬─────────┘
         ▼
   ASSIGN → UPDATE → VERIFY → RESOLVE
```

## 🧑‍💻 Technology Stack

- **Backend:** Python + Flask + SQLAlchemy
- **Authentication:** Flask-Login + Werkzeug password hashing + CSRF protection
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Database:** SQLite for local/demo, PostgreSQL-compatible configuration for deployment
- **Maps:** Leaflet + OpenStreetMap
- **AI:** Optional Google Gemini integration
- **Deployment:** Vercel serverless Python runtime
- **DevOps:** GitHub + automated deployment

## ✨ Product Experience

The interface is designed as a modern civic-tech command centre rather than a conventional complaint portal:

- Responsive citizen experience
- Animated transitions and micro-interactions
- Dark/light visual support
- Interactive issue map
- Live issue board
- Animated statistics
- Guided reporting flow
- Authority management dashboard

## 👥 Example User Journey

**A citizen spots a dangerous pothole.**

1. Opens UrbanPulse AI
2. Captures/uploads a photo
3. Adds a short description
4. Location is attached
5. AI-assisted triage suggests category and urgency
6. Issue enters the civic database
7. Community can see and vote on the issue
8. Authority assigns the issue
9. Status progresses through the workflow
10. Resolution is recorded and visible to the citizen

## 🚀 Future Scope

UrbanPulse AI is designed to grow beyond a web prototype:

- Edge-AI pothole and road-crack detection
- ESP32/IoT sensor integration
- Smart waste-bin monitoring
- Water-flow anomaly and leakage detection
- Multilingual and voice-based reporting
- WhatsApp/chatbot reporting
- Predictive infrastructure maintenance
- Municipal API integration
- Automated hotspot detection
- Computer-vision assisted verification

## 🏆 SIH Positioning

UrbanPulse AI is built around a simple idea:

> **We are not building another complaint box. We are building an intelligent civic operating layer.**

The architecture combines **AI + civic participation + geospatial data + workflow automation + analytics**, making the concept suitable for extension into real municipal environments.

## 📂 Repository Structure

```text
citizen-voice/
├── api/                    # Vercel serverless entrypoint
├── static/                 # CSS, JavaScript, images and UI assets
├── templates/              # Flask/Jinja pages
│   ├── auth/               # Login and registration
│   ├── issues/             # Issue board/reporting views
│   └── ...
├── models.py               # SQLAlchemy data models
├── routes.py               # Main application routes
├── auth.py                 # Authentication routes
├── app.py                  # Flask application factory/configuration
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
├── render.yaml             # Optional Render deployment configuration
├── Dockerfile              # Container deployment option
└── README.md               # Project documentation
```

## ⚡ Run Locally

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

Health check: `http://localhost:5000/health`

## ☁️ Deploy to Vercel

1. Import this repository into Vercel.
2. Vercel uses `vercel.json` and `api/index.py` for the Flask serverless application.
3. Configure production environment variables such as `SECRET_KEY` and a managed PostgreSQL `DATABASE_URL`.
4. Deploy and verify `/health`.

> **Production note:** Vercel serverless instances do not provide durable local storage. For persistent production data, use managed PostgreSQL and object storage for uploaded files.

## 🔐 Security Notes

- Never commit `.env` files or credentials.
- Use a strong production `SECRET_KEY`.
- Validate uploads and enforce size/type limits.
- Use managed PostgreSQL and persistent object storage for production.

## 👨‍💻 Developer

**Arjune Priyan**  
ECE Student · **Sri Manakula Vinayagar Engineering College**  
Developer — UrbanPulse AI

---

### 🌍 Vision

**See the problem. Understand the signal. Prioritise the action. Improve the city.**

Built as an SIH internal hackathon prototype with a focus on practical civic impact, scalable architecture, and a strong citizen-to-authority feedback loop.
