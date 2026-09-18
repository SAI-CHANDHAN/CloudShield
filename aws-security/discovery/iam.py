"""Read-only IAM policy discovery.

The first implementation inspects customer-managed policies only. AWS-managed
policies are intentionally excluded because they are not owned by the account.
"""

from typing import Any
from urllib.parse import unquote


def _policy_is_broad(document: dict[str, Any]) -> bool:
    statements = document.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    for statement in statements:
        if statement.get("Effect") != "Allow":
            continue
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])
        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]
        if "*" in actions or "*" in resources:
            return True
    return False


def discover_policies(client: Any) -> list[dict[str, Any]]:
    """Return customer-managed IAM policies and their broad-permission flag."""
    resources = []
    paginator = client.get_paginator("list_policies")
    for page in paginator.paginate(Scope="Local"):
        for policy in page.get("Policies", []):
            arn = policy["Arn"]
            try:
                metadata = client.get_policy(PolicyArn=arn)["Policy"]
                version_id = metadata["DefaultVersionId"]
                version = client.get_policy_version(
                    PolicyArn=arn, VersionId=version_id
                )["PolicyVersion"]
                document = version.get("Document", {})
                if isinstance(document, str):
                    import json

                    document = json.loads(unquote(document))
                broad = _policy_is_broad(document)
            except (KeyError, ValueError, TypeError):
                broad = False
            resources.append(
                {
                    "resource_id": arn,
                    "resource_type": "IAM",
                    "policy_name": policy.get("PolicyName"),
                    "broad_permissions": broad,
                }
            )
    return resources
