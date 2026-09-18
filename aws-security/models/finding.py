"""Normalized CSPM finding model."""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class FindingSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Finding(BaseModel):
    """Stable JSON-compatible shape used by the scanner and future API."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str
    resource_id: str
    resource_type: str
    title: str
    severity: FindingSeverity
    category: str
    rule_id: str
    status: str = "OPEN"
