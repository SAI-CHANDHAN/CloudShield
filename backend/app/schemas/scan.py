from pydantic import BaseModel

from .finding import FindingResponse


class ScanResponse(BaseModel):
    scan_status: str
    resources_scanned: int
    findings_created: int
    findings: list[FindingResponse]
