from unittest.mock import MagicMock

from discovery.iam import discover_policies
from rules.iam_rules import evaluate_iam_rules
from rules.s3_rules import evaluate_s3_rules
from rules.security_group_rules import evaluate_security_group_rules


def test_public_s3_bucket_generates_finding():
    findings = evaluate_s3_rules([{"resource_id": "bucket", "public_access_blocked": False, "encryption_enabled": True, "versioning_enabled": True}])
    assert [finding["rule_id"] for finding in findings] == ["CIS-S3-001"]


def test_private_s3_bucket_has_no_public_finding():
    findings = evaluate_s3_rules([{"resource_id": "bucket", "public_access_blocked": True, "encryption_enabled": True, "versioning_enabled": True}])
    assert not findings


def test_encryption_disabled_generates_finding():
    findings = evaluate_s3_rules([{"resource_id": "bucket", "public_access_blocked": True, "encryption_enabled": False, "versioning_enabled": True}])
    assert [finding["rule_id"] for finding in findings] == ["CIS-S3-002"]


def test_encryption_enabled_has_no_encryption_finding():
    findings = evaluate_s3_rules([{"resource_id": "bucket", "public_access_blocked": True, "encryption_enabled": True, "versioning_enabled": True}])
    assert not any(finding["rule_id"] == "CIS-S3-002" for finding in findings)


def test_versioning_disabled_generates_finding():
    findings = evaluate_s3_rules([{"resource_id": "bucket", "public_access_blocked": True, "encryption_enabled": True, "versioning_enabled": False}])
    assert [finding["rule_id"] for finding in findings] == ["CIS-S3-003"]


def test_ssh_open_generates_high_finding():
    resource = {"resource_id": "sg-1", "inbound_rules": [{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]}
    findings = evaluate_security_group_rules([resource])
    assert findings[0]["severity"] == "HIGH"


def test_ssh_restricted_has_no_finding():
    resource = {"resource_id": "sg-1", "inbound_rules": [{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRanges": [{"CidrIp": "10.0.0.0/8"}]}]}
    assert not evaluate_security_group_rules([resource])


def test_iam_wildcard_policy_generates_high_finding():
    client = MagicMock()
    client.get_paginator.return_value.paginate.return_value = [{"Policies": [{"Arn": "arn:policy", "PolicyName": "wild"}]}]
    client.get_policy.return_value = {"Policy": {"DefaultVersionId": "v1"}}
    client.get_policy_version.return_value = {"PolicyVersion": {"Document": {"Statement": {"Effect": "Allow", "Action": "*", "Resource": "*"}}}}
    findings = evaluate_iam_rules(discover_policies(client))
    assert findings[0]["severity"] == "HIGH"


def test_iam_restricted_policy_has_no_finding():
    client = MagicMock()
    client.get_paginator.return_value.paginate.return_value = [{"Policies": [{"Arn": "arn:policy", "PolicyName": "restricted"}]}]
    client.get_policy.return_value = {"Policy": {"DefaultVersionId": "v1"}}
    client.get_policy_version.return_value = {"PolicyVersion": {"Document": {"Statement": {"Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::private/*"}}}}
    assert not evaluate_iam_rules(discover_policies(client))
