from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Severity(StrEnum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class FindingStatus(StrEnum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    SUPPRESSED = "SUPPRESSED"


class FindingCreate(BaseModel):
    finding_id: str = Field(min_length=1)
    resource_id: str = Field(min_length=1)
    resource_type: str = Field(min_length=1)
    title: str = Field(min_length=1)
    severity: Severity
    category: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    status: FindingStatus = FindingStatus.OPEN


class FindingResponse(FindingCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    risk_score: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
