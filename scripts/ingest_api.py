"""
API Data Ingestion Script

This script fetches data from external APIs and stores it locally.
"""

import requests
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_from_api(endpoint: str, params: dict = None) -> dict:
    """
    Fetch data from an API endpoint.
    
    Args:
        endpoint: API endpoint URL
        params: Query parameters
        
    Returns:
        JSON response data
    """
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        logger.info(f"Successfully fetched data from {endpoint}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching from API: {e}")
        raise


def save_data(data: dict, output_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        output_path: Path to save the file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    logger.info(f"Data saved to {output_path}")


def main():
    """Main function to run the ingestion process."""
    # Example: fetch data from a public API
    endpoint = "https://jsonplaceholder.typicode.com/posts"
    
    data = fetch_from_api(endpoint, params={"_limit": 10})
    
    output_file = f"data/raw/api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_data(data, output_file)


if __name__ == "__main__":
    main()
