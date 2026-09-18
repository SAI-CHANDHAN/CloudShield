from unittest.mock import patch


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_finding_creation_and_retrieval(client, finding_payload):
    created = client.post("/api/findings", json=finding_payload)
    assert created.status_code == 201
    assert created.json()["risk_score"] == 70

    response = client.get("/api/findings/F-001")
    assert response.status_code == 200
    assert response.json()["finding_id"] == "F-001"


def test_unknown_finding_returns_404(client):
    assert client.get("/api/findings/unknown").status_code == 404


def test_finding_severity_validation(client, finding_payload):
    finding_payload["severity"] = "URGENT"
    response = client.post("/api/findings", json=finding_payload)
    assert response.status_code == 422


def test_risk_summary_for_one_high_finding(client, finding_payload):
    client.post("/api/findings", json=finding_payload)
    summary = client.get("/api/risk/summary")
    assert summary.status_code == 200
    assert summary.json()["overall_risk_score"] == 70
    assert summary.json()["high_count"] == 1


def test_risk_summary_for_multiple_findings(client, finding_payload):
    client.post("/api/findings", json=finding_payload)
    for finding_id, severity in (("F-002", "MEDIUM"), ("F-003", "MEDIUM")):
        payload = {**finding_payload, "finding_id": finding_id, "severity": severity}
        client.post("/api/findings", json=payload)

    summary = client.get("/api/risk/summary").json()
    assert summary["overall_risk_score"] == 89
    assert summary["total_findings"] == 3


def test_resolved_findings_are_excluded_from_risk(client, finding_payload):
    resolved = {**finding_payload, "status": "RESOLVED"}
    client.post("/api/findings", json=resolved)
    summary = client.get("/api/risk/summary").json()
    assert summary["overall_risk_score"] == 0
    assert summary["resolved_findings"] == 1


def test_scan_uses_mocked_scanner_and_persists_results(client):
    scanner_result = {
        "resources": [{"resource_id": "sg-001", "resource_type": "Security Group", "region": "us-east-1"}],
        "findings": [{
            "finding_id": "F-003",
            "resource_id": "sg-001",
            "resource_type": "Security Group",
            "title": "SSH is public",
            "severity": "HIGH",
            "category": "NETWORK_SECURITY",
            "rule_id": "CIS-SG-001",
            "status": "OPEN",
        }],
    }
    with patch("app.api.scan.scanner_service.scan_aws", return_value=scanner_result):
        response = client.post("/api/scan")

    assert response.status_code == 200
    assert response.json()["scan_status"] == "COMPLETED"
    assert response.json()["resources_scanned"] == 1
    assert response.json()["findings_created"] == 1
    assert client.get("/api/findings/F-003").status_code == 200
