# Docker Configuration for dbt Personal Finances

## Local Development Setup

1. **Copy your service account key:**
   ```bash
   cp /path/to/your-key.json keys/keyfile.json
   ```

2. **Update profiles.yml if needed:**
   - Adjust `project` and `dataset` values
   - The keyfile path is already configured

3. **Run dbt commands:**
   ```bash
   poetry run dbt deps
   poetry run dbt compile
   poetry run dbt run
   ```

## Docker Setup

### Build the image:
```bash
docker build -t personal-finances-dbt .
```

### Run with environment variables:
```bash
docker run -v $(pwd)/keys:/app/keys \
  -e DBT_KEYFILE_PATH=/app/keys/keyfile.json \
  personal-finances-dbt dbt run
```

### Using Docker Compose:
```yaml
version: '3.8'
services:
  dbt:
    build: .
    volumes:
      - ./keys:/app/keys:ro
    environment:
      - DBT_KEYFILE_PATH=/app/keys/keyfile.json
```

## CI/CD Setup

For GitHub Actions, GitLab CI, etc.:

1. Store your service account key as a secret
2. Write it to `keys/keyfile.json` in the pipeline
3. Run dbt commands with the local profiles.yml

Example GitHub Action:
```yaml
- name: Setup DBT credentials
  run: |
    mkdir -p keys
    echo '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}' > keys/keyfile.json

- name: Run dbt
  run: |
    poetry run dbt deps
    poetry run dbt run
```
