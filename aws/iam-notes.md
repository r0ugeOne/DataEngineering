# AWS IAM Setup Notes

## Overview
Setting up proper IAM roles and policies for data engineering workloads.

## Key Concepts

### IAM User
- Individual accounts with access credentials
- Use for application or personal access

### IAM Role
- For EC2, Lambda, and other AWS services
- Temporary security credentials

### IAM Policy
- Defines permissions (allow/deny)
- JSON format

## Essential Policies for Data Engineering

### S3 Access
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ]
        }
    ]
}
```

### Athena Access
```json
{
    "Effect": "Allow",
    "Action": [
        "athena:StartQueryExecution",
        "athena:GetQueryResults",
        "athena:StopQueryExecution"
    ],
    "Resource": "*"
}
```

## Best Practices

1. **Principle of Least Privilege** - Grant only necessary permissions
2. **Use Roles for Services** - Avoid storing credentials
3. **Enable MFA** - Multi-factor authentication for important accounts
4. **Audit Access** - Use CloudTrail for logging
5. **Rotate Keys** - Regular credential rotation
6. **Use Tags** - For organizing and managing resources

## AWS CLI Configuration

```bash
aws configure
# Enter:
# AWS Access Key ID
# AWS Secret Access Key
# Default region (e.g., us-east-1)
# Default output format (e.g., json)
```

## Verification

Test your setup:
```bash
aws sts get-caller-identity
aws s3 ls
aws athena list-work-groups
```
