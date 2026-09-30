import json
from unittest.mock import MagicMock, patch

import pytest

import investigator
from investigator import _build_prompt, _parse_report, investigate_finding, retrieve_knowledge

FINDING = {
    "finding_id": "F-001",
    "resource_id": "sg-001",
    "resource_type": "Security Group",
    "title": "SSH is public",
    "severity": "HIGH",
    "category": "NETWORK_SECURITY",
    "rule_id": "CIS-SG-001",
}
REPORT = {
    "root_cause": "Port 22 is open to the internet.",
    "potential_attack_scenario": "Brute force against SSH.",
    "evidence_to_check": ["Security group rules"],
    "related_security_controls": ["Session Manager"],
    "remediation": "Restrict the CIDR.",
}


def _client(text):
    client = MagicMock()
    client.models.generate_content.return_value.text = text
    return client


def test_retrieve_knowledge_returns_doc_for_rule():
    assert "CIS-SG-001" in retrieve_knowledge("CIS-SG-001")


def test_retrieve_knowledge_covers_privesc_rule():
    assert "PassRole" in retrieve_knowledge("SX-IAM-PRIVESC-001")


def test_retrieve_knowledge_unknown_rule_is_empty():
    assert retrieve_knowledge("CIS-NOPE-999") == ""


def test_prompt_contains_finding_and_knowledge():
    prompt = _build_prompt(FINDING, "some knowledge")
    assert "sg-001" in prompt
    assert "some knowledge" in prompt


def test_prompt_without_knowledge_says_so():
    assert "None available" in _build_prompt(FINDING, "")


def test_parse_report_accepts_complete_report():
    assert _parse_report(json.dumps(REPORT)) == REPORT


def test_parse_report_rejects_invalid_json():
    with pytest.raises(ValueError):
        _parse_report("not json")


def test_parse_report_rejects_missing_field():
    with pytest.raises(ValueError, match="remediation"):
        _parse_report(json.dumps({k: v for k, v in REPORT.items() if k != "remediation"}))


def test_investigate_finding_returns_report_contract():
    with patch.object(investigator, "GEMINI_API_KEY", "test-key"), patch.object(
        investigator.genai, "Client", return_value=_client(json.dumps(REPORT))
    ):
        report = investigate_finding(FINDING)
    assert set(report) == {
        "severity", "root_cause", "potential_attack_scenario", "evidence_to_check",
        "related_security_controls", "remediation", "generated_by", "model",
    }
    assert report["severity"] == "HIGH"
    assert report["generated_by"] == "gemini"


def test_investigate_finding_sends_knowledge_to_gemini():
    client = _client(json.dumps(REPORT))
    with patch.object(investigator, "GEMINI_API_KEY", "test-key"), patch.object(
        investigator.genai, "Client", return_value=client
    ):
        investigate_finding(FINDING)
    assert "CIS-SG-001" in client.models.generate_content.call_args.kwargs["contents"]


def test_investigate_finding_requires_api_key():
    with patch.object(investigator, "GEMINI_API_KEY", None):
        with pytest.raises(RuntimeError):
            investigate_finding(FINDING)
