# Data Engineering Architecture Notes

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  (APIs, Databases, Files, Logs)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │   Ingestion Layer            │
        │ (Python, AWS Lambda, Glue)  │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   Raw Data Zone              │
        │   (S3 - raw/)                │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   Processing Layer           │
        │ (PySpark, Pandas, Glue)     │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   Processed Data Zone        │
        │   (S3 - processed/)          │
        │   (Parquet format)           │
        └──────────┬───────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
   ┌─────────────┐     ┌──────────────────┐
   │  Athena     │     │  Data Warehouse  │
   │  (Querying) │     │  (Redshift/etc)  │
   └─────────────┘     └──────────────────┘
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   Analytics & BI              │
        │   (Dashboards, Reports)       │
        └──────────────────────────────┘
```

## Data Flow Patterns

### Batch ETL Pipeline
```
Source → Extract → Transform → Load → Serve
   ↓         ↓         ↓         ↓      ↓
 Daily    Schedule  Validation  S3   Queries
```

### Real-time Streaming
```
Source → Stream → Process → Store → Analytics
   ↓        ↓         ↓        ↓        ↓
Events   Kafka    Spark Streaming  Dashboards
```

## Data Zones (Medallion Architecture)

### Bronze (Raw)
- **Purpose**: Immutable copy of source data
- **Format**: Original format (CSV, JSON, Parquet)
- **Retention**: 30-90 days
- **Location**: `s3://bucket/bronze/`

### Silver (Cleaned)
- **Purpose**: Data cleaned and deduplicated
- **Format**: Parquet (snappy compressed)
- **Schema**: Standardized
- **Location**: `s3://bucket/silver/`

### Gold (Refined)
- **Purpose**: Business-ready data
- **Format**: Optimized Parquet
- **Aggregations**: Pre-computed
- **Location**: `s3://bucket/gold/`

## Partitioning Strategy

### Time-based Partitioning
```
s3://bucket/data/year=2024/month=01/day=15/hour=10/
```

### Location-based Partitioning
```
s3://bucket/data/region=US/state=CA/city=SF/
```

### Hybrid Partitioning
```
s3://bucket/data/source=api/year=2024/month=01/
```

## Quality Checks

### Ingestion Validation
- Schema validation
- Data type checking
- Required fields verification

### Processing Validation
- Null/missing value checks
- Outlier detection
- Duplicate detection

### Output Validation
- Row count checks
- Aggregation checks
- Referential integrity

## Monitoring and Alerting

### Key Metrics
- **Data Freshness**: Age of latest data
- **Pipeline Latency**: Time to process
- **Error Rate**: Failed transformations
- **Data Volume**: Records processed
- **Cost**: Compute and storage

### Alerting Rules
- Missing data (no updates > 2 hours)
- High error rate (> 5%)
- Performance degradation
- Cost threshold exceeded

## Storage Optimization

### Compression Ratio
- CSV → Parquet (Snappy): 80-90% reduction
- JSON → Parquet: 70-85% reduction

### Query Performance
- Partitioning: 10-100x speedup
- Columnar format: 2-10x speedup
- Compression: Depends on network

## Cost Optimization

### Storage Costs (US)
- S3 Standard: $0.023/GB
- S3 Intelligent-Tiering: $0.0125/GB
- S3 Glacier: $0.004/GB

### Query Costs (Athena)
- $6.25 per 1TB scanned
- Partitioning reduces scans
- Compression reduces size

### Example Savings
- Without partitions: 100GB scanned = $0.625
- With partitions: 10GB scanned = $0.0625 (90% savings)

## Security Considerations

### Data Encryption
- At-rest: S3 SSE-S3 or KMS
- In-transit: TLS/SSL
- Key rotation: Every 90 days

### Access Control
- Bucket policies: Restrict by role
- Row-level security: Database-level
- Column-level security: Application-level

### Audit Trail
- CloudTrail: Track API calls
- S3 access logs: Monitor access
- Query logs: Track Athena queries

## Disaster Recovery

### Backup Strategy
- Point-in-time snapshots
- Cross-region replication
- Version control for code

### Recovery Time Objective (RTO)
- Critical systems: < 1 hour
- Standard systems: < 4 hours
- Archive data: 24 hours

### Recovery Point Objective (RPO)
- Real-time systems: < 5 minutes
- Batch systems: Daily snapshots
- Archive: Weekly

## Scalability Patterns

### Horizontal Scaling
- Partition data for parallel processing
- Use distributed computing (PySpark)
- Independent processing per partition

### Vertical Scaling
- Increase machine resources
- Use higher DPU counts (Glue)
- Cluster instance types (EMR)

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Ingestion | Python, Lambda, Glue | Extract data |
| Storage | S3, Parquet | Store data |
| Querying | Athena, SQL | Query data |
| Processing | PySpark, Glue | Transform data |
| Orchestration | Airflow | Schedule jobs |
| Monitoring | CloudWatch | Track health |

## Typical Project Architecture

See projects/\* directories for reference implementations:
- **Project 1**: Simple ETL (CSV → SQL)
- **Project 2**: Cloud pipeline (API → S3 → Athena)
- **Project 3**: Complex pipeline (Multiple sources → ERP)
