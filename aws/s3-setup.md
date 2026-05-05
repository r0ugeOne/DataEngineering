# AWS S3 Setup Guide

## Overview
Simple Storage Service (S3) is the foundation of data lakes and data warehousing.

## Bucket Creation

### Via AWS CLI
```bash
# Create bucket
aws s3 mb s3://my-data-bucket

# Create with region
aws s3 mb s3://my-data-bucket --region us-west-2

# List buckets
aws s3 ls
```

## Bucket Configuration

### Versioning
```bash
aws s3api put-bucket-versioning \
    --bucket my-data-bucket \
    --versioning-configuration Status=Enabled
```

### Server-Side Encryption
```bash
aws s3api put-bucket-encryption \
    --bucket my-data-bucket \
    --server-side-encryption-configuration '{
        "Rules": [{
            "ApplyServerSideEncryptionByDefault": {
                "SSEAlgorithm": "AES256"
            }
        }]
    }'
```

### Lifecycle Policy
```bash
# Archive old data to Glacier
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-data-bucket \
    --lifecycle-configuration '{
        "Rules": [{
            "Id": "Archive rule",
            "Status": "Enabled",
            "Transitions": [{
                "Days": 90,
                "StorageClass": "GLACIER"
            }]
        }]
    }'
```

## File Organization Pattern

Recommended structure:
```
s3://my-data-bucket/
├── raw/
│   ├── source1/
│   │   └── year=2024/month=01/day=15/
│   └── source2/
│       └── year=2024/month=01/day=15/
├── processed/
│   ├── analytics/
│   │   └── year=2024/month=01/
│   └── reporting/
│       └── year=2024/month=01/
└── logs/
    └── year=2024/month=01/day=15/
```

## Data Upload

### Single File
```bash
aws s3 cp local_file.parquet s3://my-data-bucket/processed/
```

### Directory (Recursive)
```bash
aws s3 cp data/processed/ s3://my-data-bucket/processed/ --recursive
```

### With Parallelization
```bash
aws s3 sync data/processed/ s3://my-data-bucket/processed/ \
    --include "*.parquet" \
    --no-progress
```

## Best Practices

1. **Use Partitioning** - Organize by date/type for better performance
2. **Enable Versioning** - Protect against accidental deletions
3. **Set Lifecycle Policies** - Archive old data to reduce costs
4. **Use Encryption** - Secure sensitive data
5. **Enable Access Logging** - Monitor access patterns
6. **Use Tags** - For cost allocation and governance
7. **Block Public Access** - Prevent accidental exposure

## Costs

- **Storage**: ~$0.023 per GB/month (Standard)
- **Requests**: ~$0.0004 per 1,000 PUT/COPY/POST/LIST requests
- **Data Transfer**: First 1GB/month free, then varies by destination

## Monitoring

```bash
# List bucket contents
aws s3 ls s3://my-data-bucket/ --recursive

# Get bucket size
aws s3 ls s3://my-data-bucket/ --recursive --summarize --human-readable

# List by date
aws s3 ls s3://my-data-bucket/ --recursive --human-readable | sort
```
