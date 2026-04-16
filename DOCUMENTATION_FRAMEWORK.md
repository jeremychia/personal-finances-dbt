# dbt Documentation Framework

A principled approach to documenting data models for financial consolidation systems.

---

## Design Principles

### 1. **Information Efficiency**
Document only what is *necessary* and *not otherwise derivable*. Readers can inspect SQL for the query logic; they need help understanding **why** and **what the output means**.

- **Not necessary**: Column data types (schema is in the YAML)
- **Necessary**: Business meaning, calculation intent, valid value ranges, atomic unit definition

This respects reader time. In a financial consolidation system where stakeholders need to trust balances across multiple institutions, every minute saved on clarity is one less minute spent debugging.

### 2. **Answering the Data User's Core Questions**
A data user arriving at your model for the first time has five implicit questions:

1. **"Why does this model exist?"** → `Purpose`
2. **"What is the atomic unit?"** → `Granularity`
3. **"What data is *not* here?"** → `Filters`
4. **"How was it built?"** → `Business logic`
5. **"What does a real row look like?"** → `Example`

Each section directly answers one. This is isomorphic to how a reader's brain searches for confidence in data.

### 3. **Searchability & Discoverability**
Adding `Keywords` admits a hard truth: stakeholders don't memorize your data catalog. They search for it. In a multi-account financial system, someone asks "do we have a category hierarchy?" or "where's the multi-currency transaction data?"—*not* the model name. Keywords index for these natural language queries.

### 4. **Consolidation Context**
Your system's core job is reconciling truth across institutions (DBS, N26, Wise, Vanguard, etc.). This context shapes what documentation matters:

- **Granularity matters** because row counts differ by source and time period
- **Filters matter** because exclusions (e.g., pending transactions, corporate accounts) explain gaps in balances
- **Example values matter** because they prove you handle the specific currencies, account types, and transaction patterns your institution set sends
- **Keywords matter** because stakeholders searching "SGD", "multi-currency", or "credit card" need to find relevant tables quickly

---

## Language Principles

### 1. Plain Language Over Tech Jargon
Use simple, concrete words that accountants and CFOs understand. Avoid corporate speak.

**Bad examples:**
- "Single source of truth" — what does "source of truth" mean?
- "Consolidate all transactions" — too abstract
- "Unified view" — empty phrase
- "Enrich with categories" — jargon

**Good alternatives:**
- "One place to find all transactions" — concrete, actionable
- "Brings together transactions from..." — specific
- "All transactions in one table" — clear
- "Adds category information" — plain language

### 2. No Redundant Prefix Naming
When a model name already signals its tier (stg_*, dim_*, fact_*, mart_*), don't repeat it in the description.

**Bad:** "Staging layer for German N26 transactions..."

**Good:** "Standardizes German N26 transactions..."

The model name `stg_bank_de_eur_n26` already tells you it's staging. Use the description space to explain *what it does*, not *what tier it's in*.

### 3. Include Source URLs for Auditability
For models sourced from specific banks or investment platforms, include a link to their web portal or login page. Non-technical users need this to verify data integrity.

**Example:**
```
Purpose: Standardizes N26 German EUR transactions.
(N26 portal: https://app.n26.com/login)

Purpose: Brings together CDP investment positions for Singapore equity holdings.
(CDP login: https://www.sgx.com/investor-services)
```

This bridges the gap between raw data and live source, reducing audit friction.

---

## Why This Structure?

### Purpose
**What it does:** Answers "Is this the right table?" in one sentence.

**Why it matters:** A user scanning dbt docs needs to eliminate tables quickly. "Category dimension for transaction categorization" immediately tells you whether `dim_categories` is what you're looking for. It's the first filter.

**Information theory:** Minimizes entropy. A purpose statement reduces the problem space from "all models" to "relevant models" before the user reads further.

### Granularity
**What it does:** Defines the atomic unit—what each row represents.

**Why it matters:**
- In consolidation, you're joining across tables. Granularity mismatches cause silent bugs (e.g., joining fact_transactions to dim_accounts at account-level when fact_transactions is per-transaction).
- Users need to know whether a row is "per transaction", "per account", "per date", or "per category" before they write a JOIN.
- Prevents questions like "Why are there duplicate dates?" or "Why are there N rows per account?"

**Information theory:** Granularity is the *binding contract* between table structure and semantics. Without it, users guess. With it, they know.

### Filters
**What it does:** Explicitly states constraints and exclusions.

**Why it matters:**
- Financial consolidation has many sources with different data policies.
- Filters answer questions like "Why is my Q1 balance $2k short?" → "Oh, we exclude pending transactions" or "That account wasn't connected until April."
- Silently excluding data is how financial errors persist. Explicit filters make gaps visible.

**Information theory:** A filter is a boundary condition. Stating it prevents users from drawing conclusions outside its scope.

### Business Logic
**What it does:** Describes transformations and enrichment without requiring SQL reading.

**Why it matters:**
- A non-technical stakeholder (CFO, accountant) needs to trust the numbers. "Merges transactions from all bank sources, standardizes schema, and enriches with categories and source account details" is more trustworthy than "JOIN and GROUP BY" in SQL.
- In regulatory contexts (if you scale), logic documentation is often a requirement.
- It's the bridge between raw data (bank API responses) and user-facing numbers.

**Information theory:** Allows stakeholders to audit without parsing SQL—reduces cognitive load and increases trust.

### Example
**What it does:** Shows a real row with actual values from your system.

**Why it matters:**
- Abstract descriptions lie. "local_amount is negative for debits" means nothing until you see `local_amount = -50` for a grocery purchase.
- In a multi-currency, multi-account system, seeing `bank_source = "sg_sgd_dbs"`, `local_currency = "SGD"`, `local_amount = -50` together proves you handle SGD correctly.
- Examples catch semantic errors: if you document "negative for debits" but your data is positive, the example makes that mismatch obvious during peer review.

**Information theory:** Concreteness reduces ambiguity. An example is compressed, transferable knowledge—one row teaches more than paragraphs.

### Keywords
**What it does:** Adds searchable tags for navigation.

**Why it matters:**
- In a consolidation system, you have many similar-sounding models: `fact_bank_transactions`, `fact_crypto_transactions`, `fact_investment_transactions`.
- A user searching "multi-currency" should find all relevant tables in one search, not dig through every model's description.
- Keywords also act as a controlled vocabulary: "We use 'transfers' not 'movements'; we use 'payments' not 'outflows'."

**Information theory:** Keywords are metadata that enable semantic search—they answer "What should I search for?" before the user knows they need to search.

---

## Column Documentation

### Template
```
<What is this column?> [units/examples/constraints]
```

### Design Choices

**"What is this column?"** — Use one sentence to state meaning and source.
- `local_amount` = "Transaction amount in local currency"
- `category` = "Transaction category for expense tracking"

Avoid restating the column name (`category is the category`) or the data type (`text field`).

**Units in brackets** — Append clarifications that a data user must know to interpret the value correctly.
- `[negative for debits, positive for credits]` — sign convention
- `[e.g. "SGD", "EUR", "USD"]` — valid values
- `[1-12]` — range
- `[format YYYY-MM-DD]` — format

This keeps the description concise while encoding critical information.

**When to use multi-line** — Only when the column involves complex calculations or conditional logic. Example:

```yaml
- name: adjusted_cost_basis
  description: |
    Adjusted cost basis accounting for dividend reinvestment and corporate actions.
    For shares purchased before 2020: original purchase price.
    For shares purchased 2020+: includes dividend adjustments per tax regulations.
```

For most columns, one line suffices.

---

## Applying This to Financial Consolidation

### Dimension Models
Dimensions describe *what* — entities, categories, dates.

**Documentation focus:**
- Granularity (one per category? one per account?)
- Hierarchies (how do categories nest?)
- Completeness (do we have all categories? all dates?)

Example: `dim_categories` documents a hierarchy (category → category2 → category3), making it clear that `category` is the most detailed level and `category3` the broadest. A user can then choose which level to GROUP BY.

### Fact Models
Facts describe *transactions* — what happened.

**Documentation focus:**
- Granularity (one per transaction or aggregated?)
- Multi-currency handling (amounts, currencies, exchange rates)
- Consolidation scope (which accounts/sources included?)
- Timing (transaction date vs. posting date?)

Example: `fact_bank_transactions` documents that it's "one row per transaction" across all sources, uses local currency/amount, and excludes nothing. A user building a report can confidently SUM amounts (within currency) or JOIN to exchange rate tables if needed.

### Example: Why This Matters
Imagine a user asks: "What's the total in my accounts?"

Without documentation, they might write:
```sql
SELECT SUM(local_amount) FROM fact_bank_transactions
```

But this sums across all currencies (SGD + EUR + USD = nonsense). With documentation stating "local_amount in local currency" + the example showing mixed currencies, they *know* to join to an exchange rate table first. That's the value of documentation in a consolidation system.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Correction |
|---|---|---|
| **"Column for storing X"** | Describes the container, not the content | "Unique transaction identifier" |
| **"See the SQL"** | Punts to code; defeats documentation | Summarize the logic in prose |
| **Generic Keywords** | "data, table, column, finance" | Specific: "transfers, multi-currency, reconciliation" |
| **Missing Granularity** | Users guess and join incorrectly | "One row per transaction across all accounts" |
| **Implicit Filters** | Users miss edge cases | "Excludes pending transactions and internal transfers" |
| **Fabricated Examples** | Users distrust if examples don't match data | Pull real values from dbt seed or actual queries |
| **Redundant prefix naming** | "Staging layer for..." when model is stg_* | Just describe what it does: "Standardizes N26 transactions..." |
| **Corporate tech jargon** | "Single source of truth", "unified view", "consolidate" opaque to accountants/CFOs | "One place to find all transactions", "combines data from", "adds..." |
| **Missing source URLs** | Users can't audit back to original data | Include banking/investment platform URLs (N26, DBS, Wise, etc.) |

---

## Checklist for Reviewers

When peer-reviewing a model's documentation:

1. **Purpose** — Can a non-technical stakeholder understand why this table exists?
2. **Granularity** — Is it clear what each row represents? Would I accidentally double-count if I JOIN this?
3. **Filters** — Are all exclusions explicit? Could a user be surprised by missing data?
4. **Business Logic** — Can an accountant audit this without reading SQL?
5. **Example** — Is it a real row? Does it match the described schema and filters?
6. **Keywords** — If I search "SGD" or "credit cards", would I find this table?
7. **Columns** — Could I interpret each value correctly without asking the author?

If the answer to any is "no" or "I'm not sure", request revision.

---

## Scaling This Practice

As your system grows (more accounts, more asset classes, more users):

1. **Maintain examples** — When you add Crypto or Bonds, update examples to show those asset types.
2. **Evolve keywords** — As users search, log queries. Update keywords to match natural language.
3. **Document changes** — When logic changes (e.g., "now including pending transactions"), update Filters and Business Logic immediately.
4. **Create a glossary** — If jargon emerges (terms users don't understand), define it in a shared glossary linked from dbt docs.

---

## References

- **Information Theory:** Shannon, "A Mathematical Theory of Communication" (1948) — why precision reduces uncertainty
- **Data Governance:** Gartner's data governance framework — why metadata is as important as data
- **Financial Consolidation:** IFRS 10 (Consolidated Financial Statements) — consolidation principles (adapted for personal finance)
- **Data Product Design:** "[What Customers Really Want From You](https://www.reforge.com/blog/data-products)" — user-centric documentation

---

## Revision History

- **2026-04-15** — Framework created to support personal finance consolidation system
