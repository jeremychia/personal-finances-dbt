# dbt Model Documentation Skill

## Purpose
Ensure dbt models follow a consistent, user-centric documentation standard that answers the five core questions: Why? What atomic unit? What's excluded? How? What does a real row look like?

Use this skill when:
- Adding a new dbt model
- Updating column definitions
- Reviewing documentation during peer review
- Migrating legacy models to the standard

## Documentation Template

### Model-Level

```yaml
- name: <model_name>
  description: |
    Purpose: <What problem does this solve?>
    Granularity: <One row per...?>
    Filters: <What's excluded?>
    Business logic: <How is data transformed?>
    Example: <Sample row with actual values>
    Keywords: <comma-separated search terms>
```

**Required fields:**
- **Purpose** — One sentence. Answer: "Is this the right table?"
- **Granularity** — Define atomic unit (transaction, account, date, category)
- **Filters** — Explicit constraints or exclusions
- **Business logic** — Describe transformations without requiring SQL reading
- **Example** — Real row with actual values from your domain
- **Keywords** — 3-5 searchable terms for discoverability

### Column-Level

```yaml
columns:
  - name: <column_name>
    description: <What is this?> [units/format/valid values/constraints]
```

**Rules:**
- One sentence: meaning + source
- Append brackets for: `[units]`, `[format YYYY-MM-DD]`, `[e.g. "SGD", "EUR"]`, `[negative for debits, positive for credits]`, `[1-12 range]`
- Use multi-line only for complex calculated fields
- Keep units/examples concise—don't restate column name or data type

### Optional

```yaml
tests: [unique, not_null, relationships]
meta:
  owner: <team_name>
tags: [staging, marts, finance, core]
```

---

## Examples

### Dimension Model
```yaml
- name: dim_categories
  description: |
    Purpose: Category dimension for transaction categorization and hierarchical grouping.
    Granularity: One row per unique category.
    Filters: None - includes all categories.
    Business logic: Categories mapped to multiple hierarchical levels for flexible reporting and expense analysis.
    Example: category="Groceries", category2="Food", category3="Essentials", fixed_vs_variable="Variable"
    Keywords: categories, expenses, income, classification, hierarchy
  columns:
    - name: category
      description: Primary transaction category (unique identifier). Must be unique.
      tests: [unique]
    - name: category2
      description: Secondary category grouping [e.g. "Food"].
    - name: category3
      description: Tertiary category grouping [e.g. "Essentials"].
    - name: fixed_vs_variable
      description: Classification as fixed or variable expense [e.g. "Fixed", "Variable"].
```

### Fact Table
```yaml
- name: fact_bank_transactions
  description: |
    Purpose: Unified bank transaction fact table across all accounts and currencies.
    Granularity: One row per bank transaction.
    Filters: None - includes all transactions from all sources.
    Business logic: Merges transactions from all bank sources, standardizes schema, enriches with categories and account details.
    Example: bank_source="sg_sgd_dbs", local_date="2026-04-15", local_currency="SGD", local_amount=-50, category="Groceries", description="NTUC Fairprice"
    Keywords: transactions, banking, payments, transfers, multi-currency, credit-card
  columns:
    - name: bank_source
      description: Source bank/account identifier [e.g. "sg_sgd_dbs", "de_eur_n26"].
    - name: local_date
      description: Transaction date in local timezone [format YYYY-MM-DD].
    - name: local_currency
      description: Transaction currency code [e.g. "SGD", "EUR", "USD"].
    - name: local_amount
      description: Transaction amount in local currency [negative for debits, positive for credits].
    - name: category
      description: Transaction category for expense tracking [e.g. "Groceries"].
    - name: description
      description: Transaction description or merchant name [e.g. "NTUC Fairprice"].
```

---

## Validation Checklist

- [ ] **Purpose** — Answers "Why does this exist?" in one sentence
- [ ] **Granularity** — Clear what each row represents (prevents join bugs)
- [ ] **Filters** — All exclusions explicit (no surprise missing data)
- [ ] **Business logic** — Understandable without reading SQL
- [ ] **Example** — Real values from your data, not fabricated
- [ ] **Keywords** — Discoverable terms (searchable, not jargon)
- [ ] **Columns** — Every column has description + units/examples
- [ ] **Tests** — Key columns (IDs, amounts) have appropriate tests

---

## Why This Matters

In a financial consolidation system:
- **Granularity** prevents silent join errors
- **Filters** catch balance discrepancies early
- **Examples** prove multi-currency/multi-account handling works
- **Keywords** enable discovery across many similar models
- **Business logic** builds trust in the numbers

See `DOCUMENTATION_FRAMEWORK.md` in your project root for the complete design rationale and information theory behind each section.

---

## Quick Commands

```bash
# Generate and preview documentation
dbt docs generate && dbt docs serve

# Validate your documentation
dbt docs generate  # Will show any missing descriptions
```

---

## Next Steps

1. Choose a model to document (new or legacy)
2. Follow the template above
3. Validate with the checklist
4. Peer review with team
5. Run `dbt docs generate` to preview in dbt Docs
