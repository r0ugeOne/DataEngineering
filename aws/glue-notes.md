# AWS Glue Setup Notes

## Overview
AWS Glue is a fully managed Extract, Transform, and Load (ETL) service.

## Key Components

### 1. Glue Catalog
- Centralized metadata repository
- Database, table, and column information
- Integrated with Athena, Redshift, EMR

### 2. Glue Jobs
- Serverless ETL jobs
- Run Python or Scala code
- Automatic scaling

### 3. Glue Crawlers
- Automatically discover schema
- Create/update tables in Glue Catalog

### 4. Glue DataBrew
- Visual data preparation
- Data quality and profiling

## Creating a Crawler

### Via AWS CLI
```bash
aws glue create-crawler \
    --name my-s3-crawler \
    --role arn:aws:iam::ACCOUNT_ID:role/GlueServiceRole \
    --database-name my_database \
    --s3-target-paths s3://my-data-bucket/raw/
```

### Run Crawler
```bash
aws glue start-crawler --name my-s3-crawler

# Check status
aws glue get-crawler --name my-s3-crawler
```

## Creating a Glue Job

### Python Script Example
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="my_database",
    table_name="my_table",
    transformation_ctx="source"
)

# Transform
df = dyf.toDF()
df_transformed = df.filter(df.age > 21)

# Write output
output_dyf = DynamicFrame.fromDF(df_transformed, glueContext, "output")
glueContext.write_dynamic_frame.from_options(
    frame=output_dyf,
    connection_type="s3",
    connection_options={"path": "s3://my-data-bucket/processed/"},
    format="parquet"
)

job.commit()
```

### Create Job via CLI
```bash
aws glue create-job \
    --name my-etl-job \
    --role arn:aws:iam::ACCOUNT_ID:role/GlueServiceRole \
    --command Name=glueetl,ScriptLocation=s3://my-scripts/my_job.py
```

## Triggers for Automation

### Schedule Trigger
```bash
aws glue create-trigger \
    --name daily-etl \
    --type SCHEDULED \
    --schedule "cron(0 2 * * ? *)" \
    --actions CrawlerName=my-s3-crawler
```

### Event Trigger
```bash
aws glue create-trigger \
    --name s3-event-trigger \
    --type CONDITIONAL \
    --trigger-updates DependentJobNames=my-etl-job \
    --start-on-creation
```

## Best Practices

1. **Use Dynamic Frames** - Better handling of semi-structured data
2. **Partition Output** - Improve query performance
3. **Error Handling** - Implement try-catch blocks
4. **Logging** - Use CloudWatch for monitoring
5. **Bookmark** - Use job bookmarks to process only new data
6. **Version Control** - Keep scripts in version control

## Monitoring and Troubleshooting

### View Job Runs
```bash
aws glue list-job-runs --job-name my-etl-job
```

### Get Job Run Details
```bash
aws glue get-job-run \
    --job-name my-etl-job \
    --run-id jr_XXXXXXXXX
```

### CloudWatch Logs
```bash
aws logs tail /aws-glue/jobs/my-etl-job --follow
```

## Cost Optimization

1. **Use Glue Version 2.0+** - Better performance per DPU
2. **Right-size DPUs** - Use minimum required (0.0625 DPU minimum)
3. **Use Job Bookmarks** - Process only new data
4. **Schedule Efficiently** - Run during off-peak hours

## Typical Glue Workflow

```
Data Source (S3) 
    ↓
Glue Crawler (discovers schema)
    ↓
Glue Catalog (stores metadata)
    ↓
Glue Job (ETL transformation)
    ↓
S3 (processed data)
    ↓
Athena/Redshift (querying)
```
