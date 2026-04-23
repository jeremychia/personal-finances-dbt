# Data Testing

Build comprehensive data quality checks in dbt using a practical 7-level framework.

## The 7 Types of Data Quality Checks

Data quality breaks down into 7 distinct categories. Start with constraint and business checks; add more as needed.

### 1. Table Constraints

Ensure your table structure matches expectations:

- Uniqueness: No duplicate rows on key columns
- Not Null: Required columns have values
- Enum Check: Column values are from a permitted set
- Referential Integrity: Foreign keys match parent table values

These are foundational — they catch structural issues immediately.

### 2. Business Criteria

Work with subject matter experts to define business rules:

- Min/Max Bounds: Values fall within permitted ranges (e.g., transaction amounts > $0)
- Event Order: Events occur in expected sequence (e.g., account opened before first transaction)
- Data Format: Values match expected format (e.g., "$500.00" for currency)

Business checks catch domain-specific issues your schema wouldn't catch.

### 3. Schema Changes

Detect unintended schema drift:

- Data Type Shifts: Transformation functions produce unexpected types
- Upstream Changes: Source schema evolved without warning

Schema checks prevent bugs from creeping in silently.

### 4. Anomaly Detection

Catch metric deviations over time:

- Percentage Change: Flag if a metric shifts >X% between runs
- Standard Deviation: Alert if values fall outside normal range

Critical for business metrics (revenue, user counts, etc.) where changes signal bugs.

### 5. Data Distribution

Monitor data volume and composition:

- Row Count Stability: Row counts remain consistent across days (catch missing dates)
- Segment Size: Critical data segments stay proportionally similar

Distribution checks catch data loss from faulty joins or filters.

### 6. Reconciliation

Verify data flow through pipeline:

- Input vs Output: Output has same number of entities as input
- Data Duplication: No unexpected row multiplication

Reconciliation pinpoints where data is lost or duplicated.

### 7. Audit Logs

Log row counts at each transformation step:

- Row Counts In/Out: Record rows entering and leaving each step
- Debugging Trail: Audit logs show exactly where data is lost or duplicated

Audit logs are your first tool when debugging data issues.

## Implementation Strategy

Start here:
1. Constraint checks (uniqueness, not null, enums, referential integrity)
2. Business criteria (work with domain experts on min/max, event order, format)

Add as needed:
3. Schema checks (if upstream changes frequently)
4. Anomaly detection (for critical business metrics)
5. Distribution checks (if you've had join/filter bugs)
6. Reconciliation checks (add to major transformation steps)
7. Audit logs (log row counts in key pipelines)

## Warning Levels

Tag checks with severity levels (INFO, DEBUG, WARN, ERROR):

- ERROR: Block the pipeline (critical data issues)
- WARN: Alert but proceed (data degradation, minor issues)
- INFO: Log only (monitoring metrics, informational)
- DEBUG: Development only (detailed diagnostics)

Set warning levels based on check criticality and business impact.

## dbt Implementation

Use dbt-expectations or write custom tests in tests/ directory:

Constraint Test (dbt-expectations):

```yaml
versions:
  - version: 1
    columns:
      - name: transaction_id
        tests:
          - unique
          - not_null
```

Business Criteria Test (custom SQL):

```sql
-- tests/assert_positive_amounts.sql
select * from {{ ref('transactions') }}
where amount <= 0
```

Anomaly Detection (dbt test):

```sql
-- tests/assert_revenue_stability.sql
with current as (
  select count(*) as row_count from {{ ref('revenue') }}
),
previous as (
  select row_count from {{ ref('audit_log') }}
  where table_name = 'revenue'
  order by run_date desc limit 1
)
select * from current
where abs(row_count - previous.row_count) / previous.row_count > 0.10
```

## Quick Reference

| Check Type | Catches | When to Use |
|---|---|---|
| Constraints | Nulls, duplicates, invalid enums | Always |
| Business Criteria | Domain-specific violations | Work with SME |
| Schema Changes | Type shifts, missing columns | Frequent upstream changes |
| Anomaly Detection | Unexpected metric shifts | Business metrics |
| Distribution | Missing data, broken joins | History of join bugs |
| Reconciliation | Data loss in transformations | Major pipelines |
| Audit Logs | Where data goes missing | Debugging complex flows |
