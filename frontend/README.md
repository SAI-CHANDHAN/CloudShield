# CloudShield Frontend

Phase 3 React dashboard for CloudShield CSPM. It consumes the existing FastAPI backend and does not contain AWS credentials or hardcoded findings.

## Architecture

- Vite + React + TypeScript
- Tailwind CSS for layout and styling
- React Router for dashboard, findings, detail, and resources routes
- Recharts for the API-backed severity distribution
- `src/services/api.ts` is the single API boundary
- `src/types/cloudshield.ts` contains backend response contracts

## Setup

```powershell
cd frontend
npm install
npm run dev
```

The Vite server runs at `http://127.0.0.1:5173`. Start the backend separately:

```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Set a different backend URL with `VITE_API_BASE_URL` before starting Vite. The default is `http://127.0.0.1:8000`.

```powershell
$env:VITE_API_BASE_URL = "http://127.0.0.1:8000"
```

## Routes

- `/dashboard` security overview, risk score, severity mix, recent findings, scan action
- `/findings` searchable and filterable findings table
- `/findings/:findingId` finding details and Phase 4 AI placeholder
- `/resources` searchable resource inventory

## Commands

- `npm run dev` start local development server
- `npm run build` type-check and create a production build
- `npm run preview` preview the production build

The current backend has no historical scan endpoint, so the dashboard presents a clear empty state for trends instead of fabricating historical data.
