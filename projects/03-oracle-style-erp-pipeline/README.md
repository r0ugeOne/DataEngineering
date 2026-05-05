# Project 3: ERP-Style Pipeline

## Overview
A complex data pipeline that integrates multiple data sources into a data warehouse following ERP patterns.

## Data Sources
- **Source 1**: Customer database (PostgreSQL)
- **Source 2**: Sales API (REST)
- **Source 3**: Inventory files (CSV)

## Processing Stages
1. **Extraction**: Pull from multiple sources
2. **Transformation**: Normalize and reconcile data
3. **Loading**: Load into warehouse
4. **Aggregation**: Pre-compute analytics

## Data Model
- **Dimension Tables**: Customers, Products, Time
- **Fact Tables**: Orders, OrderItems, Inventory

## Technical Stack
- **Orchestration**: Apache Airflow
- **Processing**: PySpark / Glue
- **Storage**: PostgreSQL + S3
- **Monitoring**: CloudWatch

## Key Features
- Error handling and retry logic
- Data quality checks
- Incremental load support
- Audit trail and lineage

## Running
```bash
# Start Airflow
airflow db init
airflow webserver -p 8080
airflow scheduler

# Trigger DAG
airflow dags trigger erp_pipeline
```
