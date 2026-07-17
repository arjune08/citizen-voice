# WardPulse AI – Local Issue Voting Board

A production-ready, full-stack civic complaint platform built with Flask, SQLite, and Tailwind CSS. Citizens can register, report local issues with photos, vote on complaints, and get AI assistance. Ward officers/admins manage complaints through a powerful dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![AI](https://img.shields.io/badge/AI-Gemini-purple)

---

## Features

### Citizens
- ✅ Register & Login with secure password hashing
- ✅ Report issues with photos, GPS location, and detailed descriptions
- ✅ AI-powered category and priority detection
- ✅ Vote on community issues
- ✅ Track complaint status (Pending → Verified → Assigned → Resolved)
- ✅ AI Chatbot for assistance on every page
- ✅ Real-time notifications
- ✅ Profile management with complaint history

### Admin Dashboard
- ✅ Comprehensive dashboard with charts and metrics
- ✅ Manage complaints (view, update status, delete)
- ✅ User management (search, enable/disable, delete)
- ✅ Admin management with role-based access (Super Admin only)
- ✅ Export reports (Excel & PDF)
- ✅ AI-generated analytics and summaries
- ✅ Ward-wise leaderboard

### Platform
- ✅ Interactive map with color-coded markers (Leaflet + OpenStreetMap)
- ✅ Dark/Light mode toggle
- ✅ Responsive design (Desktop, Tablet, Mobile)
- ✅ Email notifications via Gmail SMTP
- ✅ QR codes for each complaint
- ✅ Glassmorphism UI with animations
- ✅ Search, filter, and sort functionality
- ✅ Duplicate issue detection

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python Flask 3.0 |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML5 + Tailwind CSS (CDN) + Vanilla JS |
| Auth | Flask-Login |
| Email | Flask-Mail (Gmail SMTP) |
| AI | Google Gemini API |
| Maps | Leaflet.js + OpenStreetMap |
| Charts | Chart.js |
| Icons | Font Awesome 6 |
| Export | openpyxl (Excel), reportlab (PDF) |

---

## Quick Start

### 1. Install Dependencies

```bash
cd win
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy and edit the environment file
copy .env.example .env

# Edit .env with your settings:
# - SECRET_KEY: Generate a random string
# - MAIL_USERNAME: Your Gmail address
# - MAIL_PASSWORD: Gmail App Password (not regular password)
# - GEMINI_API_KEY: From https://aistudio.google.com/app/apikey
```

### 3. Create Super Admin

```bash
flask create-superadmin
# Follow prompts to enter name, email, and password
```

### 4. Run the Application

```bash
python app.py
# OR
flask run --debug
```

### 5. Open in Browser

```
http://localhost:5000
```

---

## Project Structure

```
win/
├── app.py              # Flask app factory, config, CLI
├── models.py           # SQLAlchemy models
├── routes.py           # All route blueprints
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── uploads/            # Uploaded images
├── static/
│   ├── css/
│   │   └── style.css   # Custom design system
│   ├── js/
│   │   ├── main.js     # Core JS (theme, toasts, animations)
│   │   ├── auth.js     # Auth forms
│   │   ├── issues.js   # Voting
│   │   ├── dashboard.js
│   │   ├── admin.js    # AI summary
│   │   ├── map.js      # Map utilities
│   │   └── chatbot.js  # AI chatbot
│   └── images/
├── templates/
│   ├── base.html       # Base layout
│   ├── landing.html    # Landing page
│   ├── auth/           # Login, Register, Admin Login
│   ├── user/           # Dashboard, Report, Profile
│   ├── issues/         # Board, Detail, Map
│   └── admin/          # Dashboard, Complaints, Users, Admins
└── README.md
```

---

## Admin Roles

| Role | Permissions |
|------|------------|
| Super Admin | Full access: manage admins, users, complaints, analytics |
| Ward Officer | Manage complaints, view users, export reports |
| Moderator | View and update complaint status |

---

## Email Configuration

To enable email notifications:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: Google Account → Security → App Passwords
3. Set in `.env`:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

---

## AI Configuration

To enable AI features (chatbot, category detection, priority detection, summaries):

1. Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set in `.env`:
   ```
   GEMINI_API_KEY=your-api-key
   ```

**Note:** All AI features gracefully degrade with helpful fallback responses if no API key is configured.

---

## License

Built for Smart City Hackathon. All rights reserved.
