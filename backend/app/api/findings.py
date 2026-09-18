from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.finding import Finding
from ..schemas.finding import FindingCreate, FindingResponse
from ..services.risk_engine import score_finding

router = APIRouter(prefix="/api/findings", tags=["findings"])


def _to_model(payload: FindingCreate) -> Finding:
    data = payload.model_dump()
    data["risk_score"] = score_finding(payload.severity)
    return Finding(**data)


@router.get("", response_model=list[FindingResponse])
def list_findings(db: Session = Depends(get_db)) -> list[Finding]:
    return list(db.scalars(select(Finding).order_by(Finding.id)).all())


@router.post("", response_model=FindingResponse, status_code=status.HTTP_201_CREATED)
def create_finding(payload: FindingCreate, db: Session = Depends(get_db)) -> Finding:
    existing = db.scalar(select(Finding).where(Finding.finding_id == payload.finding_id))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Finding already exists")
    finding = _to_model(payload)
    db.add(finding)
    db.commit()
    db.refresh(finding)
    return finding


@router.get("/{finding_id}", response_model=FindingResponse)
def get_finding(finding_id: str, db: Session = Depends(get_db)) -> Finding:
    finding = db.scalar(select(Finding).where(Finding.finding_id == finding_id))
    if finding is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding
