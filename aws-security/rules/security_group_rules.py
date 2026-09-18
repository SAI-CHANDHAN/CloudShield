"""Pure security group CSPM rules."""

from typing import Any


def _ssh_is_open(rule: dict[str, Any]) -> bool:
    protocol = rule.get("IpProtocol")
    from_port = rule.get("FromPort")
    to_port = rule.get("ToPort")
    is_ssh = protocol == "-1" or (from_port is not None and from_port <= 22 <= (to_port or from_port))
    return is_ssh and any(item.get("CidrIp") == "0.0.0.0/0" for item in rule.get("IpRanges", []))


def evaluate_security_group_rules(resources: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Return findings for unrestricted inbound SSH access."""
    violations = []
    for resource in resources:
        if any(_ssh_is_open(rule) for rule in resource.get("inbound_rules", [])):
            violations.append(
                {"resource_id": resource["resource_id"], "rule_id": "CIS-SG-001", "title": "Security group allows SSH from the public internet", "severity": "HIGH", "category": "NETWORK_SECURITY"}
            )
    return violations
