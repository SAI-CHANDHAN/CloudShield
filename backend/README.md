# CloudShield Backend

## Purpose

This FastAPI service receives normalized AWS CSPM resources and findings, stores them in SQLAlchemy, and exposes deterministic risk data for the future React dashboard.

## Architecture

- `app/api/`: REST endpoints and request handling
- `app/models/`: SQLAlchemy persistence models
- `app/schemas/`: Pydantic request and response validation
- `app/services/risk_engine.py`: pure severity and environment-risk calculations
- `app/services/scanner_service.py`: isolated adapter for the existing `aws-security/scanner.py`
- `app/database.py`: SQLAlchemy engine and session configuration

The default database is local SQLite. Any PostgreSQL-compatible SQLAlchemy URL can be supplied with `DATABASE_URL`.

## Setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set another database when needed:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://user:password@localhost/cloudshield"
```

Install the matching PostgreSQL driver separately when using PostgreSQL. SQLite needs no extra driver.

## Run

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; Swagger UI is at `/docs`.

## Tests

```powershell
$env:PYTHONPATH = "."
pytest tests -v
```

All tests use isolated temporary SQLite databases and mock the AWS scanner.

## Endpoints

- `GET /api/health`
- `GET /api/resources`
- `GET /api/findings`
- `POST /api/findings`
- `GET /api/findings/{finding_id}`
- `POST /api/scan`
- `GET /api/risk/summary`

Example requests:

```powershell
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/findings
curl http://127.0.0.1:8000/api/risk/summary
curl -X POST http://127.0.0.1:8000/api/scan
```

## MVP risk calculation

A finding receives a direct severity score: CRITICAL 90, HIGH 70, MEDIUM 40, LOW 20, or INFO 5. The environment score uses only OPEN findings:

`100 * (1 - product(1 - finding_score / 100))`

The result is clamped to 0-100 and rounded to the nearest integer. Counts include all stored findings, while resolved and suppressed findings do not contribute to overall risk.
