"""Configuration and logging helpers for the AWS security scanner."""

import logging
import os

AWS_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
LOG_LEVEL = os.getenv("CLOUDSHIELD_LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
LOGGER = logging.getLogger("cloudshield.aws_security")

REQUIRED_READ_ONLY_PERMISSIONS = [
    "s3:ListAllMyBuckets",
    "s3:GetBucketLocation",
    "s3:GetPublicAccessBlock",
    "s3:GetEncryptionConfiguration",
    "s3:GetBucketVersioning",
    "ec2:DescribeInstances",
    "ec2:DescribeSecurityGroups",
    "iam:ListPolicies",
    "iam:GetPolicy",
    "iam:GetPolicyVersion",
]
