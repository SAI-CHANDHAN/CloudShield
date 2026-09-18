"""Pure IAM CSPM rules."""

from typing import Any


def evaluate_iam_rules(resources: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Return findings for policies marked broad by IAM discovery."""
    return [
        {
            "resource_id": resource["resource_id"],
            "rule_id": "CIS-IAM-001",
            "title": "IAM policy contains overly broad permissions",
            "severity": "HIGH",
            "category": "IDENTITY_SECURITY",
        }
        for resource in resources
        if resource.get("broad_permissions", False)
    ]
