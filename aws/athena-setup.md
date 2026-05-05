# AWS Athena Setup Guide

## Overview
Amazon Athena is a serverless query service for analyzing data in S3 using SQL.

## Prerequisites

1. **S3 Bucket** - Data source and results location
2. **IAM Permissions** - Athena, S3, and Glue permissions
3. **Glue Catalog** - Optional but recommended for schema management

## Initial Setup

### 1. Create Results Bucket
```bash
aws s3 mb s3://my-athena-results
```

### 2. Configure Athena

```bash
# Set query results location
aws athena start-query-execution \
    --query-string "SHOW DATABASES" \
    --query-execution-context Database=default \
    --result-configuration OutputLocation=s3://my-athena-results/
```

### 3. Create External Table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS my_data (
    id INT,
    name STRING,
    amount DOUBLE,
    date STRING
)
PARTITIONED BY (year STRING, month STRING, day STRING)
STORED AS PARQUET
LOCATION 's3://my-data-bucket/processed/'
TBLPROPERTIES ('has_encrypted_data'='false');
```

## Query Examples

### Basic Query
```sql
SELECT * FROM my_data LIMIT 10;
```

### With Partitions
```sql
SELECT COUNT(*) 
FROM my_data 
WHERE year='2024' AND month='01'
PARTITION (year='2024', month='01');
```

### Aggregations
```sql
SELECT 
    date,
    COUNT(*) as record_count,
    SUM(amount) as total_amount
FROM my_data
WHERE year='2024'
GROUP BY date
ORDER BY date DESC;
```

## Partition Management

### Add Partition
```sql
ALTER TABLE my_data 
ADD PARTITION (year='2024', month='01', day='15')
LOCATION 's3://my-data-bucket/processed/year=2024/month=01/day=15/';
```

### Add Multiple Partitions
```sql
MSCK REPAIR TABLE my_data;
```

## Performance Optimization

### 1. Use Partitions
- Query only necessary partitions
- Reduces data scanned and costs

### 2. Use Columnar Format
- Parquet or ORC formats
- Significant performance improvement

### 3. Compress Data
- Snappy, Gzip, or Brotli
- Reduces storage and transfer costs

### 4. Use Projection
- Project only needed columns
- Reduces bytes scanned

### Query Optimization Example
```sql
-- Good: Partition + Column selection + Limit
SELECT id, name
FROM my_data
WHERE year='2024' AND month='01'
LIMIT 100;

-- Bad: Full table scan + Multiple columns
SELECT * FROM my_data LIMIT 100;
```

## Cost Management

### Cost Estimation
- **Query Cost** = (Data Scanned in GB) × $6.25 / 1,000,000 queries
- **First 1GB per month**: Free
- **Example**: 100GB scanned = $0.625

### Cost Reduction Strategies
1. **Use Partitions** - Avoid scanning entire tables
2. **Use Projection** - Select only needed columns
3. **Compress Data** - Store as Parquet with compression
4. **Use Results Cache** - Reuse query results

## Monitoring Queries

```bash
# List recent queries
aws athena list-query-executions --max-results 10

# Get query details
aws athena get-query-execution \
    --query-execution-id <execution-id>

# Get query results
aws athena get-query-results \
    --query-execution-id <execution-id>
```

## Integration with Python

```python
import boto3
import pandas as pd

athena = boto3.client('athena')

response = athena.start_query_execution(
    QueryString='SELECT * FROM my_data LIMIT 10',
    QueryExecutionContext={'Database': 'default'},
    ResultConfiguration={'OutputLocation': 's3://my-athena-results/'}
)

# Get results
results = athena.get_query_results(
    QueryExecutionId=response['QueryExecutionId']
)

# Convert to DataFrame
df = pd.DataFrame(results['ResultSet']['Rows'][1:])
```

## Troubleshooting

### Common Issues

1. **Partition Not Found**
   - Run `MSCK REPAIR TABLE` to add new partitions

2. **Access Denied**
   - Check IAM permissions for S3 and Athena

3. **Slow Queries**
   - Use partitions and projection
   - Check data format (use Parquet)

4. **Invalid Column**
   - Verify schema matches data format
   - Check for schema drift
