# CIS-SG-001: Inbound SSH is open to 0.0.0.0/0

Severity: HIGH. Category: NETWORK_SECURITY.

## What it means
A security group allows TCP port 22 from any IPv4 address. Any host on the internet can attempt to connect to SSH on instances using this group.

## Attack scenario
Attackers run password guessing and credential stuffing against SSH, or exploit an unpatched SSH service. A compromised instance gives them its instance profile credentials through the metadata service, which they can use against the AWS account.

## Evidence to check
- `aws ec2 describe-security-groups --group-ids <id>` for the ingress rule
- Which instances and network interfaces use the group
- Whether those instances have public IPs and what instance profile they hold
- `/var/log/auth.log` or `/var/log/secure` for failed or unknown logins
- VPC Flow Logs for port 22 traffic from unknown sources

## Related controls
CIS AWS Foundations 5.2, AWS Systems Manager Session Manager, EC2 Instance Connect, bastion host, IMDSv2.

## Remediation
Remove the 0.0.0.0/0 rule. Restrict SSH to known admin CIDR ranges, or use Session Manager and close port 22 entirely. Require key-based authentication and IMDSv2 on the instances.
