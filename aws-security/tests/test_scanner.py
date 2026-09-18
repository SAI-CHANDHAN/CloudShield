from unittest.mock import MagicMock

from models.finding import Finding
from scanner import _normalise_findings


def test_normalised_finding_matches_contract():
    result = _normalise_findings(
        [{
            "resource_id": "cloudshield-public-test",
            "rule_id": "CIS-S3-001",
            "title": "S3 bucket allows public access",
            "severity": "CRITICAL",
            "category": "DATA_PROTECTION",
        }]
    )
    assert result == [{
        "finding_id": "F-001",
        "resource_id": "cloudshield-public-test",
        "resource_type": "S3",
        "title": "S3 bucket allows public access",
        "severity": "CRITICAL",
        "category": "DATA_PROTECTION",
        "rule_id": "CIS-S3-001",
        "status": "OPEN",
    }]
    Finding.model_validate(result[0])
