"""
Fetch mart_transactions from BigQuery and cache locally as JSON.
Uses service account authentication from keys/keyfile.json
"""

import json
import os
from pathlib import Path
from google.cloud import bigquery
from google.oauth2 import service_account

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
KEYFILE_PATH = PROJECT_ROOT / "keys" / "keyfile.json"
CACHE_PATH = Path(__file__).parent / "data" / "transactions.json"


def fetch_and_cache():
    """Fetch data from BigQuery and cache locally."""

    # Ensure data directory exists
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Setup credentials
    credentials = service_account.Credentials.from_service_account_file(
        str(KEYFILE_PATH), scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    client = bigquery.Client(credentials=credentials, project="jeremy-chia")

    query = """
    SELECT
        bank_source,
        CAST(local_date AS STRING) as local_date,
        local_currency,
        local_amount,
        category,
        category2,
        category3,
        fixed_vs_variable,
        description,
        translated_currency,
        translated_amount
    FROM `jeremy-chia.prod_mart.mart_transactions`
    ORDER BY local_date DESC
    """

    print("Fetching data from BigQuery...")
    result = client.query(query).result()

    # Convert to list of dicts
    data = [dict(row) for row in result]

    # Save to JSON
    with open(CACHE_PATH, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"Cached {len(data)} transactions to {CACHE_PATH}")
    return data


if __name__ == "__main__":
    fetch_and_cache()
