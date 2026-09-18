"""Read-only EC2 instance discovery."""

from typing import Any


def discover_instances(client: Any) -> list[dict[str, Any]]:
    """Discover running and stopped instances from all reservations."""
    resources = []
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    ):
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                resources.append(
                    {
                        "resource_id": instance["InstanceId"],
                        "resource_type": "EC2",
                        "state": instance.get("State", {}).get("Name"),
                        "instance_type": instance.get("InstanceType"),
                        "security_group_ids": [
                            group["GroupId"] for group in instance.get("SecurityGroups", [])
                        ],
                        "subnet_id": instance.get("SubnetId"),
                        "vpc_id": instance.get("VpcId"),
                    }
                )
    return resources
