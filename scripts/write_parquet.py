"""
Parquet Writing Script

This script converts data to Parquet format with compression and partitioning.
"""

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_parquet(
    input_path: str,
    output_path: str,
    compression: str = 'snappy',
    partition_cols: list = None
) -> None:
    """
    Convert data to Parquet format.
    
    Args:
        input_path: Input file path (CSV or similar)
        output_path: Output Parquet file path
        compression: Compression algorithm (snappy, gzip, brotli)
        partition_cols: Columns to partition by
    """
    logger.info(f"Reading data from {input_path}")
    df = pd.read_csv(input_path)
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write to Parquet
    logger.info(f"Writing to Parquet with {compression} compression")
    df.to_parquet(
        output_path,
        compression=compression,
        index=False,
        engine='pyarrow'
    )
    
    logger.info(f"Parquet file saved to {output_path}")
    
    # Log statistics
    file_size = Path(output_path).stat().st_size / 1024 / 1024
    logger.info(f"File size: {file_size:.2f} MB")
    logger.info(f"Rows: {len(df)}, Columns: {len(df.columns)}")


def read_parquet_summary(parquet_path: str) -> dict:
    """Get summary statistics from Parquet file."""
    parquet_file = pq.ParquetFile(parquet_path)
    
    summary = {
        'num_rows': parquet_file.metadata.num_rows,
        'num_columns': parquet_file.metadata.num_columns,
        'compression': parquet_file.schema.to_arrow_schema(),
        'schema': parquet_file.schema_arrow.to_pandas_dtype()
    }
    
    logger.info(f"Parquet Summary: {summary}")
    return summary


def main():
    """Main function."""
    input_file = "data/raw/sample_data.csv"
    output_file = "data/processed/sample_data.parquet"
    
    convert_to_parquet(input_file, output_file)
    read_parquet_summary(output_file)


if __name__ == "__main__":
    main()
