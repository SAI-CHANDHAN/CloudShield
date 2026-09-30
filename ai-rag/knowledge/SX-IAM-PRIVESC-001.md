# SX-IAM-PRIVESC-001: IAM permissions allow privilege escalation

Severity: HIGH, CRITICAL when the path reaches administrator access. Category: IDENTITY_SECURITY.

## What it means
An identity holds IAM permissions that let it raise its own or another principal's privileges without going through an approval. Common combinations:
- `iam:CreatePolicyVersion` or `iam:SetDefaultPolicyVersion` on a policy attached to itself
- `iam:AttachUserPolicy`, `iam:AttachRolePolicy`, `iam:AttachGroupPolicy` or `iam:PutUserPolicy` / `iam:PutRolePolicy`
- `iam:PassRole` together with `ec2:RunInstances`, `lambda:CreateFunction` or `cloudformation:CreateStack`
- `iam:CreateAccessKey` or `iam:UpdateLoginProfile` for another user
- `iam:UpdateAssumeRolePolicy` on a more privileged role

## Attack scenario
An attacker who controls a low-privilege identity with one of these permissions gives themselves the AdministratorAccess policy, launches a compute resource with an admin role and reads its credentials, or takes over an admin user's keys. The result is full account control.

## Evidence to check
- Effective permissions of the identity, including inline, group and boundary policies
- Whether the resources in the statement are `*` or limited to specific ARNs
- Whether `iam:PassRole` is limited with `iam:PassedToService` conditions
- CloudTrail for `CreatePolicyVersion`, `AttachUserPolicy`, `CreateAccessKey`, `UpdateAssumeRolePolicy` calls
- Recently created access keys, policy versions or instances with attached roles

## Related controls
Least privilege, permission boundaries, service control policies, IAM Access Analyzer, CloudTrail alerts on IAM changes.

## Remediation
Remove the escalating permissions or scope them to exact resource ARNs. Add a permission boundary to identities that manage IAM. Restrict `iam:PassRole` with resource and `iam:PassedToService` conditions. Rotate credentials of any identity that may have been abused and review CloudTrail for changes made through the path.
