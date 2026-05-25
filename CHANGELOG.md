# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
