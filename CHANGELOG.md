# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.1] — 2026-05-26

### Changed

- Executive rule `rule-priv-exec-001` now includes a `limitation_notice` field, emitting a high-level summary notice to the executive passport and raising LP from 0.00 to 0.50 (overall RCEA: 0.8313 → 0.8938 for the privacy/recruitment example)
- `Rule` model gains optional `limitation_notice: str | None` field; `propagate_limitations` and `compute_limitation_propagation` updated accordingly
- `schemas/rule_pack.schema.json` extended with optional `limitation_notice` property

### Fixed

- `paper_artifacts/tables/rcea_scores.csv` executive row for `privacy_recruitment` corrected to LP = 0.5000 / RCEA = 0.8937

## [0.1.0] — 2026-05-25

### Added

- Initial public release: `rcea/` package with engine, scoring, passport, rules, and traceability modules
- Four synthetic worked examples: `privacy_recruitment`, `robustness_healthcare`, `supplier_procurement`, `fairness_credit`
- Sixty tests across eight test files covering scoring, passport reproducibility, suppression logging, traceability, schema validation, limitation propagation, N/A dimension handling, and unsupported-claim detection
- JSON schemas for evidence finding, role profile, context pack, rule pack, and passport
- Five CLI scripts: `generate_passport.py`, `compute_rcea.py`, `validate_passport.py`, `reproduce_paper_tables.py`, `reproduce_paper_figures.py`
- Paper artefacts: CSV/Markdown tables (subconstruct definitions, role taxonomy, RCEA score matrix) and Mermaid figure diagrams
- Two Jupyter notebooks demonstrating engine usage and score analysis
- GitHub Actions CI workflow running tests and paper reproduction on every push
- `CITATION.cff` and BibTeX metadata for software citation
