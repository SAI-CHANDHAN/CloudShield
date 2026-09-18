# CloudShield AWS Security Engine

A small, read-only AWS Cloud Security Posture Management (CSPM) scanner for the CloudShield project. It discovers AWS resources, evaluates fixed security rules, validates findings with Pydantic, and returns a stable JSON-compatible result.

## Architecture

- `discovery/` calls boto3 read APIs and returns plain resource dictionaries.
- `rules/` contains pure functions that evaluate discovered data. Rules never call AWS.
- `models/finding.py` defines the normalized finding contract.
- `scanner.py` creates boto3 clients, orchestrates discovery and evaluation, and assigns deterministic finding IDs.

## Supported services

- S3 buckets
- EC2 instances
- EC2 security groups
- Customer-managed IAM policies

## Rules

| Rule | Check | Severity | Category |
| --- | --- | --- | --- |
| CIS-S3-001 | S3 public access block is not fully enabled | CRITICAL | DATA_PROTECTION |
| CIS-S3-002 | S3 server-side encryption is absent | HIGH | DATA_PROTECTION |
| CIS-S3-003 | S3 versioning is not enabled | MEDIUM | DATA_PROTECTION |
| CIS-SG-001 | Inbound SSH is open to `0.0.0.0/0` | HIGH | NETWORK_SECURITY |
| CIS-IAM-001 | An Allow statement contains `*` in actions or resources | HIGH | IDENTITY_SECURITY |

IAM inspection is conservative: only customer-managed policies are inspected, and a policy is flagged when an Allow statement contains a wildcard action or resource. This is not a complete IAM privilege analysis.

## Setup

Use Python 3.11 or newer:

```powershell
cd aws-security
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Credentials are never stored in this project. boto3 uses its normal credential chain, such as environment variables, an AWS profile, or an attached IAM role. A region must be available through `AWS_REGION`, `AWS_DEFAULT_REGION`, or the boto3 session.

The scanner needs read-only permissions for:

```text
s3:ListAllMyBuckets
s3:GetBucketLocation
s3:GetPublicAccessBlock
s3:GetEncryptionConfiguration
s3:GetBucketVersioning
ec2:DescribeInstances
ec2:DescribeSecurityGroups
iam:ListPolicies
iam:GetPolicy
iam:GetPolicyVersion
```

## Run

From this directory, run:

```powershell
python scanner.py
```

Or integrate the function into another Python application:

```python
from scanner import scan_aws_environment

result = scan_aws_environment()
```

Example output:

```json
{
  "scan_status": "COMPLETED",
  "resources_scanned": 4,
  "findings": [
    {
      "finding_id": "F-001",
      "resource_id": "cloudshield-public-test",
      "resource_type": "S3",
      "title": "S3 bucket allows public access",
      "severity": "CRITICAL",
      "category": "DATA_PROTECTION",
      "rule_id": "CIS-S3-001",
      "status": "OPEN"
    }
  ]
}
```

Finding IDs are deterministic within a scan: findings are sorted by resource ID and rule ID before numbering.

## Tests

Tests use mocked AWS responses and never make real AWS calls:

```powershell
python -m pytest -q
```

## Security limitations

This module is strictly read-only. It never changes or deletes AWS resources, creates resources, changes bucket policies, changes encryption or versioning, modifies security groups, or modifies IAM. S3 public-access detection currently evaluates the Public Access Block configuration and does not inspect bucket policies or ACLs. The scanner logs service-level AWS failures and continues with other services where possible; a partial scan returns `COMPLETED_WITH_ERRORS`.
