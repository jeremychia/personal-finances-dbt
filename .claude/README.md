# Claude Code Setup

Project-scoped Claude Code skill for dbt model documentation.

## Skill: `/dbt-docs`

Invoke with `/dbt-docs` to see the documentation template, examples, and validation checklist for dbt models.

Covers:
- Documentation template (Purpose, Granularity, Filters, Business Logic, Example, Keywords)
- Column-level guidelines
- Real examples from your project
- Peer review checklist

## Theory

See `DOCUMENTATION_FRAMEWORK.md` in the project root for:
- Design principles (information efficiency, the five core questions users ask)
- Why each field matters for financial consolidation systems
- Information theory rationale
- Anti-patterns and review guidelines

## Files

- `settings.json` — Project Claude Code config
- `skills/dbt-docs.md` — The skill itself

## Getting Started

Type `/dbt-docs` in Claude Code when documenting a model. Read `DOCUMENTATION_FRAMEWORK.md` for the "why" behind the standard.
