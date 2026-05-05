"""
Data Cleaning Script

This script performs data cleaning and validation.
"""

import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from file."""
    logger.info(f"Loading data from {file_path}")
    
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Remove duplicates
    df = df.drop_duplicates()
    logger.info(f"Removed duplicates. Shape: {df.shape}")
    
    # Handle missing values
    df = df.dropna()
    logger.info(f"Removed NaN values. Shape: {df.shape}")
    
    # Convert data types
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    logger.info("Data cleaning completed")
    return df


def validate_data(df: pd.DataFrame) -> bool:
    """Validate cleaned data."""
    if df.empty:
        logger.warning("DataFrame is empty!")
        return False
    
    logger.info(f"Data validation passed. Shape: {df.shape}")
    return True


def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned data."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if output_path.endswith('.parquet'):
        df.to_parquet(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)
    
    logger.info(f"Cleaned data saved to {output_path}")


def main():
    """Main function."""
    input_file = "data/raw/sample_data.csv"
    output_file = "data/processed/cleaned_data.parquet"
    
    df = load_data(input_file)
    df = clean_data(df)
    
    if validate_data(df):
        save_cleaned_data(df, output_file)


if __name__ == "__main__":
    main()
