"""Orchestration entry point for the read-only AWS security engine."""

from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config import AWS_REGION, LOGGER
from discovery.ec2 import discover_instances
from discovery.iam import discover_policies
from discovery.s3 import discover_buckets
from discovery.security_groups import discover_security_groups
from models.finding import Finding
from rules.iam_rules import evaluate_iam_rules
from rules.s3_rules import evaluate_s3_rules
from rules.security_group_rules import evaluate_security_group_rules


def _normalise_findings(violations: list[dict[str, str]]) -> list[dict[str, Any]]:
    findings = []
    for index, violation in enumerate(
        sorted(violations, key=lambda item: (item["resource_id"], item["rule_id"])), 1
    ):
        resource_type = "S3" if violation["rule_id"].startswith("CIS-S3") else (
            "Security Group" if violation["rule_id"].startswith("CIS-SG") else "IAM"
        )
        finding = Finding(
            finding_id=f"F-{index:03d}",
            resource_id=violation["resource_id"],
            resource_type=resource_type,
            title=violation["title"],
            severity=violation["severity"],
            category=violation["category"],
            rule_id=violation["rule_id"],
        )
        findings.append(finding.model_dump(mode="json"))
    return findings


def _discover_service(name: str, discover: Any, client: Any) -> tuple[list[dict[str, Any]], bool]:
    try:
        return discover(client), False
    except (BotoCoreError, ClientError) as error:
        LOGGER.error("Could not discover %s resources: %s", name, error)
        return [], True


def scan_aws_environment(session: Any | None = None) -> dict[str, Any]:
    """Discover AWS resources, evaluate CSPM rules, and return JSON-compatible findings.

    The function uses boto3's normal credential chain and performs no write calls.
    """
    session = session or boto3.Session(region_name=AWS_REGION)
    if session.get_credentials() is None:
        raise RuntimeError("AWS credentials unavailable; configure the normal boto3 credential chain")
    region = session.region_name or AWS_REGION
    if not region:
        raise RuntimeError("AWS region unavailable; set AWS_REGION or AWS_DEFAULT_REGION")

    clients = {
        "s3": session.client("s3", region_name=region),
        "ec2": session.client("ec2", region_name=region),
        "security_groups": session.client("ec2", region_name=region),
        "iam": session.client("iam", region_name=region),
    }
    s3, s3_error = _discover_service("S3", discover_buckets, clients["s3"])
    ec2, ec2_error = _discover_service("EC2", discover_instances, clients["ec2"])
    security_groups, sg_error = _discover_service(
        "security groups", discover_security_groups, clients["security_groups"]
    )
    iam, iam_error = _discover_service("IAM", discover_policies, clients["iam"])

    violations = evaluate_s3_rules(s3)
    violations.extend(evaluate_security_group_rules(security_groups))
    violations.extend(evaluate_iam_rules(iam))
    resources_scanned = len(s3) + len(ec2) + len(security_groups) + len(iam)
    had_errors = s3_error or ec2_error or sg_error or iam_error
    return {
        "scan_status": "COMPLETED_WITH_ERRORS" if had_errors else "COMPLETED",
        "resources_scanned": resources_scanned,
        "findings": _normalise_findings(violations),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(scan_aws_environment(), indent=2))
