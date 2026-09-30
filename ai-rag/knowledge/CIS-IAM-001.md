# CIS-IAM-001: IAM policy contains overly broad permissions

Severity: HIGH. Category: IDENTITY_SECURITY.

## What it means
A customer-managed IAM policy has an Allow statement with `*` in its actions or resources. Anything attached to it can do far more than its job requires.

## Attack scenario
If a user, role or access key with this policy is compromised, the attacker inherits the wildcard permissions and can read data, change configuration or create new credentials across the account.

## Evidence to check
- The policy document: `aws iam get-policy-version --policy-arn <arn> --version-id <v>`
- Which users, groups and roles it is attached to: `aws iam list-entities-for-policy`
- IAM Access Advisor last-accessed data to see what is actually used
- CloudTrail for unusual API calls by those principals

## Related controls
CIS AWS Foundations 1.16, least privilege, IAM Access Analyzer policy generation, permission boundaries, service control policies.

## Remediation
Replace wildcards with the specific actions and resource ARNs needed. Use Access Analyzer to generate a policy from real usage. Detach the broad policy once the replacement is attached.
