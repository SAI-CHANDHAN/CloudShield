from pydantic import BaseModel


class RiskSummary(BaseModel):
    overall_risk_score: int
    total_findings: int
    open_findings: int
    resolved_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
