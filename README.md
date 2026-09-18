# CloudShield

Cloud Security Posture Management (CSPM) platform for a controlled AWS test environment.

## MVP pipeline

AWS Resource Discovery -> CSPM Security Scan -> Findings -> Risk Score -> React Dashboard -> Gemini + RAG -> Investigation Report

## Modules

- `aws-security/` — AWS discovery and CSPM rules
- `backend/` — FastAPI, PostgreSQL, risk engine, REST API
- `ai-rag/` — Gemini investigation and RAG pipeline
- `frontend/` — React dashboard

## Development

Keep `main` stable. Work in feature branches and merge through pull requests.

## Demo target

29 September 2026
