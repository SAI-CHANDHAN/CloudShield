from types import SimpleNamespace

from app.services.risk_engine import build_risk_summary, score_finding


def test_severity_scores_are_deterministic():
    assert score_finding("CRITICAL") == 90
    assert score_finding("HIGH") == 70
    assert score_finding("INFO") == 5


def test_multiple_open_findings_use_combined_risk_formula():
    findings = [
        SimpleNamespace(status="OPEN", severity="HIGH", risk_score=70),
        SimpleNamespace(status="OPEN", severity="MEDIUM", risk_score=40),
        SimpleNamespace(status="OPEN", severity="MEDIUM", risk_score=40),
    ]
    assert build_risk_summary(findings)["overall_risk_score"] == 89
