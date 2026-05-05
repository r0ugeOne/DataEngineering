"""
Example Airflow DAG for data pipeline orchestration.

This demonstrates a simple data ingestion and transformation pipeline.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments
default_args = {
    'owner': 'data-engineering',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

# Define DAG
dag = DAG(
    'data_ingestion_pipeline',
    default_args=default_args,
    description='Daily data ingestion and processing',
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False,
)


def extract_data(**context):
    """Extract data from source."""
    print("Extracting data from API...")
    # Implementation here
    return "extraction_complete"


def transform_data(**context):
    """Transform and clean data."""
    print("Transforming data...")
    # Implementation here
    return "transformation_complete"


def load_data(**context):
    """Load data to warehouse."""
    print("Loading data...")
    # Implementation here
    return "load_complete"


# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Set dependencies
extract_task >> transform_task >> load_task
