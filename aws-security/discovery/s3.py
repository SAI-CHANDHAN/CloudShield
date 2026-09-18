"""Read-only S3 bucket discovery."""

from typing import Any

from botocore.exceptions import ClientError


def _has_public_access_block(client: Any, bucket_name: str) -> bool:
    try:
        configuration = client.get_public_access_block(Bucket=bucket_name).get(
            "PublicAccessBlockConfiguration", {}
        )
        return all(
            configuration.get(key, False)
            for key in (
                "BlockPublicAcls",
                "IgnorePublicAcls",
                "BlockPublicPolicy",
                "RestrictPublicBuckets",
            )
        )
    except ClientError:
        return False


def _has_encryption(client: Any, bucket_name: str) -> bool:
    try:
        configuration = client.get_bucket_encryption(Bucket=bucket_name)
        return bool(configuration.get("ServerSideEncryptionConfiguration", {}).get("Rules"))
    except ClientError:
        return False


def _versioning_enabled(client: Any, bucket_name: str) -> bool:
    try:
        return client.get_bucket_versioning(Bucket=bucket_name).get("Status") == "Enabled"
    except ClientError:
        return False


def discover_buckets(client: Any) -> list[dict[str, Any]]:
    """Return bucket posture data, continuing when an individual API call fails."""
    buckets = []
    for bucket in client.list_buckets().get("Buckets", []):
        name = bucket["Name"]
        region = None
        try:
            location = client.get_bucket_location(Bucket=name).get("LocationConstraint")
            region = location or "us-east-1"
        except ClientError:
            pass
        buckets.append(
            {
                "resource_id": name,
                "resource_type": "S3",
                "name": name,
                "region": region,
                "public_access_blocked": _has_public_access_block(client, name),
                "encryption_enabled": _has_encryption(client, name),
                "versioning_enabled": _versioning_enabled(client, name),
            }
        )
    return buckets
