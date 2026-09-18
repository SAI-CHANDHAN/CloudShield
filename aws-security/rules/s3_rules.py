"""Pure S3 CSPM rules."""

from typing import Any


def evaluate_s3_rules(resources: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Return rule violations for discovered S3 buckets."""
    violations = []
    for resource in resources:
        if not resource.get("public_access_blocked", False):
            violations.append(
                {"resource_id": resource["resource_id"], "rule_id": "CIS-S3-001", "title": "S3 bucket allows public access", "severity": "CRITICAL", "category": "DATA_PROTECTION"}
            )
        if not resource.get("encryption_enabled", False):
            violations.append(
                {"resource_id": resource["resource_id"], "rule_id": "CIS-S3-002", "title": "S3 bucket has server-side encryption disabled", "severity": "HIGH", "category": "DATA_PROTECTION"}
            )
        if not resource.get("versioning_enabled", False):
            violations.append(
                {"resource_id": resource["resource_id"], "rule_id": "CIS-S3-003", "title": "S3 bucket has versioning disabled", "severity": "MEDIUM", "category": "DATA_PROTECTION"}
            )
    return violations
