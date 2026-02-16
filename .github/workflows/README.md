# dbt Docs Deployment Configuration

This directory contains GitHub Actions workflows for deploying dbt documentation to GitHub Pages.

## Available Workflows

### 1. `deploy-dbt-docs.yml` (Full Documentation)
**Recommended for production use**

- Connects to BigQuery to generate complete documentation including table statistics and column information
- Requires BigQuery service account credentials as GitHub secrets
- Generates full catalog.json with table/column metadata
- Runs on push to main branch

### 2. `deploy-dbt-docs-static.yml` (Static Documentation)
**Recommended for public repositories or when you don't want to expose credentials**

- Generates documentation without connecting to the data warehouse
- No credentials required - uses only project files
- Limited to model definitions, descriptions, and lineage
- No table statistics or column-level information from the warehouse
- Runs on model file changes

## Setup Instructions

1. **Choose your preferred workflow** based on your security requirements and documentation needs

2. **For full documentation** (`deploy-dbt-docs.yml`):
   - Add `DBT_SERVICE_ACCOUNT_KEY` secret to GitHub repository
   - Ensure service account has BigQuery read permissions

3. **For static documentation** (`deploy-dbt-docs-static.yml`):
   - No additional secrets required
   - Documentation will be limited to project-defined metadata

4. **Enable GitHub Pages**:
   - Repository Settings → Pages
   - Source: "GitHub Actions"

5. **Optional**: Disable the workflow you don't need by renaming the file extension from `.yml` to `.yml.disabled`

## Customization

### Custom dbt target
Both workflows use `--target prod` by default. Modify the workflow files to use a different target if needed:

```yaml
dbt docs generate --target your-target-name
```

### Different trigger conditions
Modify the `on:` section in either workflow to change when documentation is deployed:

```yaml
on:
  push:
    branches: [ main, develop ]  # Deploy on multiple branches
  schedule:
    - cron: '0 6 * * *'  # Deploy daily at 6 AM UTC
```

### Custom deployment path
The documentation deploys to the root of your GitHub Pages site by default. To deploy to a subdirectory, modify the artifact preparation step:

```yaml
- name: Prepare docs for Pages
  run: |
    mkdir -p docs-site/docs  # Deploy to /docs subdirectory
    cp target/index.html docs-site/docs/
    # ... rest of file copying
```
