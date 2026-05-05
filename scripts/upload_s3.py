"""
S3 Upload Script

This script uploads files to AWS S3 with error handling and logging.
"""

import boto3
import logging
from pathlib import Path
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class S3Manager:
    """Manage S3 operations."""
    
    def __init__(self, bucket_name: str, region_name: str = 'us-east-1'):
        """
        Initialize S3 manager.
        
        Args:
            bucket_name: S3 bucket name
            region_name: AWS region
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        logger.info(f"Initialized S3 manager for bucket: {bucket_name}")
    
    def upload_file(self, file_path: str, s3_key: str) -> bool:
        """
        Upload a file to S3.
        
        Args:
            file_path: Local file path
            s3_key: S3 object key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not Path(file_path).exists():
                logger.error(f"File not found: {file_path}")
                return False
            
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            logger.info(f"Successfully uploaded {file_path} to s3://{self.bucket_name}/{s3_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def upload_directory(self, local_dir: str, s3_prefix: str) -> int:
        """
        Upload all files from a local directory to S3.
        
        Args:
            local_dir: Local directory path
            s3_prefix: S3 prefix for all files
            
        Returns:
            Number of files uploaded
        """
        count = 0
        local_path = Path(local_dir)
        
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_path)
                s3_key = f"{s3_prefix}/{relative_path}".replace('\\', '/')
                
                if self.upload_file(str(file_path), s3_key):
                    count += 1
        
        logger.info(f"Uploaded {count} files to S3")
        return count
    
    def download_file(self, s3_key: str, file_path: str) -> bool:
        """Download a file from S3."""
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, file_path)
            logger.info(f"Downloaded s3://{self.bucket_name}/{s3_key} to {file_path}")
            return True
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return False


def main():
    """Main function."""
    # Example usage
    bucket_name = "my-data-bucket"
    s3_manager = S3Manager(bucket_name)
    
    # Upload a single file
    s3_manager.upload_file("data/processed/sample_data.parquet", "processed/sample_data.parquet")
    
    # Upload a directory
    s3_manager.upload_directory("data/processed", "data/processed")


if __name__ == "__main__":
    main()
