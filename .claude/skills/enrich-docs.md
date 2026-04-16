# enrich-docs

Enrich dbt YAML documentation with sample data from BigQuery — with discretion. Only enriches columns where examples add real value.

## Usage

```bash
python3 .claude/enrich_docs_with_samples.py
```

## What it does

- Connects to your BigQuery `jeremy-chia` project
- Queries DISTINCT values for relevant columns in fact/dimension tables
- Skips self-evident columns (e.g., day_of_week_iso, day_of_month) to avoid noise
- Updates YAML descriptions with real, contextual sample values
- Preserves existing documentation structure

## Examples

- Enriches: local_date → (e.g. "2024-03-31", "2024-04-01")
- Skips: day_of_month → already clear (1-31)
- Enriches: category → (e.g. "Groceries", "Transport", "Entertainment")
- Skips: is_latest_date → boolean flag, self-evident

## Configuration

Edit the script to customize skip list:
- Line ~119-131: SKIP_ENRICHMENT set for self-evident columns
- Project: jeremy-chia (line ~185)

## Requirements

- Google Cloud BigQuery credentials at keys/keyfile.json
- Python packages: pyyaml, google-cloud-bigquery
