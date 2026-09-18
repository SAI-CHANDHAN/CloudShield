from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.finding import Finding
from ..schemas.risk import RiskSummary
from ..services.risk_engine import build_risk_summary

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/summary", response_model=RiskSummary)
def risk_summary(db: Session = Depends(get_db)) -> dict[str, int]:
    findings = db.scalars(select(Finding)).all()
    return build_risk_summary(findings)
