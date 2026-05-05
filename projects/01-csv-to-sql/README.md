# Project 1: CSV to SQL Pipeline

## Overview
This project demonstrates loading CSV data into a PostgreSQL database with validation and quality checks.

## Requirements
- Python 3.10+
- pandas, sqlalchemy, psycopg2
- PostgreSQL (local or Docker)

## Steps
1. Load CSV file using pandas
2. Validate data quality
3. Connect to PostgreSQL
4. Create schema if not exists
5. Insert data with error handling
6. Verify data integrity

## Running
```bash
python pipeline.py --input data.csv --database warehouse
```

## Output
- Logs in logs/
- Data in PostgreSQL warehouse.public.* tables
