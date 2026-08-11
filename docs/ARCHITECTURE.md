# UrbanPulse AI — Architecture & Hackathon Guide

## 1. Product statement

UrbanPulse AI converts citizen observations into structured, location-aware civic issues that can be prioritised and managed through a transparent resolution workflow.

## 2. Core flow

```text
Citizen
  ↓
Report / Photo / Location
  ↓
Validation + Authentication
  ↓
AI-assisted Classification & Priority
  ↓
SQL Persistence
  ↓
Map + Community Signals
  ↓
Authority Assignment
  ↓
Status Updates
  ↓
Resolution / Verification
```

## 3. Primary personas

### Citizen
- Create an account
- Report an issue
- Add evidence and location
- View nearby issues
- Vote on community issues
- Track resolution

### Ward officer / authority
- Review incoming issues
- Prioritise and assign work
- Update status
- Monitor geographic hotspots
- Export operational data

### Administrator
- Manage users and authorities
- Review platform activity
- Configure operational workflows
- Access higher-level analytics

## 4. Hackathon demo path

For a 3–5 minute jury demonstration:

1. Start on the UrbanPulse AI landing page.
2. Open the issue board and show live civic signals.
3. Create/login as a citizen.
4. Submit a sample pothole or waste issue with location.
5. Show how the issue enters the database and appears in the map/board.
6. Switch to the authority workflow.
7. Demonstrate priority, assignment, and status progression.
8. End on the dashboard and explain future IoT/edge-AI expansion.

## 5. Differentiation

UrbanPulse AI is intentionally broader than a complaint portal. Its value comes from combining:

- citizen participation
- structured issue data
- AI-assisted triage
- geospatial visibility
- community signals
- operational workflow
- resolution transparency

## 6. Engineering principles

- Keep secrets in environment variables.
- Use PostgreSQL for persistent production data.
- Treat uploaded files as object-storage assets in production.
- Keep AI assistance optional so core reporting remains functional.
- Keep the citizen and authority workflows independently understandable.
- Prefer measurable operational signals over invented claims.
