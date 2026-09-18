from collections.abc import Iterable
from math import prod

from ..models.finding import Finding, FindingStatus, Severity

SEVERITY_SCORES: dict[Severity, int] = {
    Severity.CRITICAL: 90,
    Severity.HIGH: 70,
    Severity.MEDIUM: 40,
    Severity.LOW: 20,
    Severity.INFO: 5,
}


def score_finding(severity: Severity | str) -> int:
    return SEVERITY_SCORES[Severity(severity)]


def build_risk_summary(findings: Iterable[Finding]) -> dict[str, int]:
    finding_list = list(findings)
    open_findings = [finding for finding in finding_list if finding.status == FindingStatus.OPEN]
    risk_factors = [1 - finding.risk_score / 100 for finding in open_findings]
    overall_risk = 100 * (1 - prod(risk_factors)) if risk_factors else 0

    counts = {severity.value.lower() + "_count": 0 for severity in Severity}
    for finding in finding_list:
        key = f"{Severity(finding.severity).value.lower()}_count"
        counts[key] += 1

    return {
        "overall_risk_score": max(0, min(100, round(overall_risk))),
        "total_findings": len(finding_list),
        "open_findings": len(open_findings),
        "resolved_findings": sum(finding.status == FindingStatus.RESOLVED for finding in finding_list),
        **counts,
    }
