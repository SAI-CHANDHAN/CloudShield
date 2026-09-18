import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.finding import Finding
from ..models.resource import Resource
from ..schemas.finding import FindingCreate
from ..schemas.scan import ScanResponse
from ..services import scanner_service
from ..services.risk_engine import score_finding

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["scan"])


def _upsert_resource(db: Session, data: dict[str, Any]) -> Resource:
    resource_id = data["resource_id"]
    provider = data.get("provider", "AWS")
    resource = db.scalar(select(Resource).where(Resource.resource_id == resource_id, Resource.provider == provider))
    if resource is None:
        resource = Resource(resource_id=resource_id, resource_type=data["resource_type"], provider=provider)
        db.add(resource)
    for field in ("resource_type", "region", "name"):
        if field in data:
            setattr(resource, field, data[field])
    return resource


def _upsert_finding(db: Session, data: dict[str, Any]) -> Finding:
    payload = FindingCreate.model_validate(data)
    finding = db.scalar(select(Finding).where(Finding.finding_id == payload.finding_id))
    values = payload.model_dump()
    values["risk_score"] = score_finding(payload.severity)
    if finding is None:
        finding = Finding(**values)
        db.add(finding)
    else:
        for field, value in values.items():
            setattr(finding, field, value)
    return finding


@router.post("/scan", response_model=ScanResponse)
def run_scan(db: Session = Depends(get_db)) -> dict[str, Any]:
    try:
        result = scanner_service.scan_aws()
        resources = [_upsert_resource(db, item) for item in result["resources"]]
        findings = [_upsert_finding(db, item) for item in result["findings"]]
        db.commit()
        for finding in findings:
            db.refresh(finding)
        return {
            "scan_status": "COMPLETED",
            "resources_scanned": len(resources),
            "findings_created": len(findings),
            "findings": findings,
        }
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("AWS scan failed")
        raise HTTPException(status_code=500, detail="Scan failed") from exc
