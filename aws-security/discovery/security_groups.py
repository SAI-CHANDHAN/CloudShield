"""Read-only security group discovery."""

from typing import Any


def discover_security_groups(client: Any) -> list[dict[str, Any]]:
    """Discover security groups and their inbound/outbound permissions."""
    resources = []
    paginator = client.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for group in page.get("SecurityGroups", []):
            resources.append(
                {
                    "resource_id": group["GroupId"],
                    "resource_type": "Security Group",
                    "group_name": group.get("GroupName"),
                    "vpc_id": group.get("VpcId"),
                    "inbound_rules": group.get("IpPermissions", []),
                    "outbound_rules": group.get("IpPermissionsEgress", []),
                }
            )
    return resources
