#!/usr/bin/env python3
"""
Enrich dbt YAML documentation with sample data from BigQuery.
Queries DISTINCT values for each column to provide real examples.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from google.cloud import bigquery


def load_yaml(path: str) -> dict:
    """Load YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def save_yaml(path: str, data: dict) -> None:
    """Save YAML file preserving structure."""
    with open(path, "w") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def get_bq_client() -> bigquery.Client:
    """Initialize BigQuery client."""
    keyfile = os.getenv("DBT_KEYFILE_PATH", "keys/keyfile.json")
    if not Path(keyfile).exists():
        raise FileNotFoundError(
            f"BigQuery keyfile not found at {keyfile}. "
            "Set DBT_KEYFILE_PATH or place at keys/keyfile.json"
        )
    return bigquery.Client.from_service_account_json(keyfile)


def get_sample_values(
    client: bigquery.Client, project: str, table: str, column: str
) -> list[str]:
    """Query DISTINCT values for a column directly from BigQuery tables.

    Tries to find the table in any dataset by scanning available datasets.
    """
    try:
        # Get list of datasets in the project
        datasets = client.list_datasets()
        dataset_ids = [d.dataset_id for d in datasets]

        # Try common dataset patterns first
        priority_datasets = [
            f"prod_{table.split('_')[0]}",  # e.g., prod_mart for mart_*
            f"prod_facts",
            f"prod_mart",
            f"prod_dim",
            f"prod_staging",
        ]

        # Try priority datasets first, then others
        for dataset_id in priority_datasets + dataset_ids:
            if dataset_id not in dataset_ids:
                continue

            try:
                query = f"""
                SELECT DISTINCT {column}
                FROM `{project}.{dataset_id}.{table}`
                WHERE {column} IS NOT NULL
                ORDER BY {column}
                LIMIT 3
                """
                results = client.query(query).result()
                values = [str(row[column]) for row in results]
                return values
            except Exception:
                # Try next dataset
                continue

        return []
    except Exception as e:
        print(f"⚠️  Error querying {table}.{column}: {e}", file=sys.stderr)
        return []


def format_sample_value(value: Any, dtype: str) -> str:
    """Format sample value for display in documentation."""
    if value is None:
        return "NULL"
    if dtype in ("DATE", "TIMESTAMP"):
        return f'"{value}"'
    if isinstance(value, (int, float)):
        return str(value)
    return f'"{value}"'


def enrich_column_description(
    description: str,
    sample_values: list[str],
    column_type: str = None,
) -> str:
    """Add sample values to column description, replacing existing examples."""
    if not sample_values or not description:
        return description

    # Remove existing "(e.g. ...)" patterns to avoid duplicates
    cleaned = re.sub(r"\s*\(e\.g\.\s*[^)]+\)", "", description)
    cleaned = cleaned.rstrip(".")

    # Add new example
    samples_str = ", ".join(format_sample_value(v, column_type) for v in sample_values)
    return f"{cleaned} (e.g. {samples_str})."


# Columns that are self-evident and don't need sample values
SKIP_ENRICHMENT = {
    # Date/time columns with obvious values
    "day_of_week_iso",
    "day_of_month",
    "day_of_year",
    "iso_week_of_year",
    "month",
    "quarter",
    "year",
    # Self-explanatory numeric sequences
    "is_latest_date",
    "is_redeemed",
    # Fields with obvious boolean-like values
    "flag",
}


def should_enrich_column(col_name: str, description: str) -> bool:
    """Determine if a column should be enriched with sample values.

    Skip columns that are:
    - Already well-documented with clear examples
    - Self-evident (dates, booleans, sequential numbers)
    - Containing only NULL/empty data
    """
    # Skip known self-evident columns
    if col_name in SKIP_ENRICHMENT:
        return False

    # Skip columns that already have good examples
    if " (e.g. " in description and len(description) > 100:
        return False

    return True


def process_model(
    client: bigquery.Client,
    model: dict,
    project: str,
) -> dict:
    """Enrich a single model with sample data using discretion."""
    table_name = model.get("name")
    if not table_name:
        return model

    print(f"Processing {table_name}...")

    columns = model.get("columns", [])
    for column in columns:
        col_name = column.get("name")
        if not col_name:
            continue

        description = column.get("description", "")

        # Check if this column should be enriched
        if not should_enrich_column(col_name, description):
            continue

        # Get sample values from BigQuery
        samples = get_sample_values(client, project, table_name, col_name)

        if samples:
            enriched = enrich_column_description(description, samples)
            column["description"] = enriched
            print(f"  ✓ {col_name}: {samples}")
        else:
            print(f"  - {col_name}: no data available")

    return model


def main():
    """Main entry point."""
    project = "jeremy-chia"

    print(f"🔄 Enriching documentation with BigQuery samples...")
    print(f"   Project: {project}\n")

    # Find all _models.yml files
    models_dir = Path("models")
    yaml_files = list(models_dir.glob("**/*_models.yml"))

    if not yaml_files:
        print("❌ No *_models.yml files found in models/")
        sys.exit(1)

    print(f"📄 Found {len(yaml_files)} model files\n")

    # Initialize BigQuery client
    try:
        client = get_bq_client()
        print("✅ Connected to BigQuery\n")
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    # Process each file
    for yaml_file in yaml_files:
        print(f"\n📝 {yaml_file}")
        print("-" * 50)

        try:
            data = load_yaml(yaml_file)
            models = data.get("models", [])

            for model in models:
                process_model(client, model, project)

            # Save enriched YAML
            save_yaml(yaml_file, data)
            print(f"✅ Saved {yaml_file}")

        except Exception as e:
            print(f"❌ Error processing {yaml_file}: {e}", file=sys.stderr)
            continue

    print("\n✨ Documentation enrichment complete!")


if __name__ == "__main__":
    main()
