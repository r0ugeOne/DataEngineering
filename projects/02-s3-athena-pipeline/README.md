# Project 2: S3 to Athena Pipeline

## Overview
Build a serverless data pipeline that ingests data from S3 and makes it queryable via Athena.

## Architecture
```
S3 (raw) → AWS Glue → S3 (processed) → Athena
```

## Components
- **S3 Bucket**: Data source and processed data storage
- **AWS Glue**: ETL jobs for transformation
- **Athena**: SQL querying engine
- **Glue Catalog**: Metadata management

## Key Tasks
1. Set up S3 bucket structure
2. Create Glue crawler to discover schema
3. Write Glue ETL job
4. Create Athena external tables
5. Set up partition management

## Costs
- S3 Storage: ~$0.023/GB
- Athena Queries: $6.25 per 1TB scanned

## Scaling Considerations
- Partition by date/region
- Use columnar format (Parquet)
- Implement data retention policies
