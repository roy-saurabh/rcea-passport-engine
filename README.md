# RCEA Passport Engine

[![Tests](https://github.com/roy-saurabh/rcea-passport-engine/actions/workflows/tests.yml/badge.svg)](https://github.com/roy-saurabh/rcea-passport-engine/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20384670.svg)](https://doi.org/10.5281/zenodo.20384670)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

**Manuscript:** Role-Conditioned Evidentiary Adequacy for AI Governance: A Computable Framework, Evidence Passport Architecture, and Reference Implementation.

> **WARNING:** This is a research reference implementation using synthetic data only. It is **not** a legal compliance certification engine and does not constitute legal advice. RCEA scores are not legal determinations of regulatory compliance.

---

## Purpose

This repository is the companion reference implementation for the RCEA manuscript. It demonstrates that Role-Conditioned Evidentiary Adequacy (RCEA) can be computed deterministically from:

- a common **evidence substrate** (`EvidenceFinding`),
- a **governance role profile** (`RoleProfile`),
- a **context pack** encoding the deployment context (`ContextPack`),
- and a **rule pack** encoding role-conditioned evidence policies (`RulePack`).

It generates **evidence passport** views tailored to each governance role, with full traceability, suppression logging, limitation propagation, and RCEA scoring.

---

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/roy-saurabh/rcea-passport-engine.git
cd rcea-passport-engine
pip install -e ".[dev]"
```

---

## Quickstart

Generate a DPO evidence passport for the privacy/recruitment example:

```bash
python scripts/generate_passport.py \
    --example privacy_recruitment \
    --role dpo \
    --out examples/privacy_recruitment/outputs/dpo_passport.json \
    --markdown examples/privacy_recruitment/outputs/dpo_passport.md
```

Compute RCEA subscores:

```bash
python scripts/compute_rcea.py --example privacy_recruitment --role dpo
```

Validate a generated passport:

```bash
python scripts/validate_passport.py \
    examples/privacy_recruitment/outputs/dpo_passport.json \
    --example privacy_recruitment \
    --role dpo
```

Run all tests:

```bash
pytest tests/ -v
```

---

## Full Reproduction

To reproduce all paper tables, figures, and example passports from scratch:

```bash
git clone https://github.com/roy-saurabh/rcea-passport-engine.git
cd rcea-passport-engine
pip install -e ".[dev,notebooks]"
pytest tests/ -v
python scripts/reproduce_paper_tables.py
python scripts/reproduce_paper_figures.py
```

---

## Examples

| Example | Finding | Roles |
|---------|---------|-------|
| `privacy_recruitment` | PII entity count = 14 (threshold: 0), GDPR Art. 22 & 35 | DPO, CISO, AI Lead, Executive |
| `robustness_healthcare` | Adversarial accuracy drop = 0.28 (threshold: 0.05) | CISO, AI Lead, Executive |
| `supplier_procurement` | Missing supplier attestations × 3 | Procurement, Vendor, Executive |
| `fairness_credit` | Demographic parity difference = 0.18 (threshold: 0.10) | DPO, AI Lead, Executive |

Generate all passports for all examples:

```bash
for ex in privacy_recruitment robustness_healthcare supplier_procurement fairness_credit; do
  for role in $(python3 -c "import json; d=json.load(open(f'examples/$ex/role_profiles.json')); [print(r['role_id']) for r in d]"); do
    python scripts/generate_passport.py --example $ex --role $role \
        --out examples/$ex/outputs/${role}_passport.json
  done
done
```

---

## Reproducing Paper Tables and Figures

```bash
python scripts/reproduce_paper_tables.py   # → paper_artifacts/tables/
python scripts/reproduce_paper_figures.py  # → paper_artifacts/figures/
```

Tables produced:
- `subconstructs.csv / .md` — RCEA subconstruct definitions
- `role_taxonomy.csv / .md` — governance role taxonomy
- `rcea_scores.csv / .md` — all example × role RCEA score matrix

Figures produced (Mermaid diagrams):
- `fig1_rcea_pipeline.md` — end-to-end RCEA pipeline
- `fig2_passport_architecture.md` — passport data model
- `fig3_score_aggregation.md` — score aggregation with N/A handling
- `fig4_worked_example.md` — worked example transformation

---

## RCEA Subscores

| Symbol | Dimension | Description |
|--------|-----------|-------------|
| MR | Material Relevance | Fraction of role-required fields present in the finding |
| EW | Epistemic Warrant | Evidence quality score, penalised for uncertainty |
| NA | Normative Alignment | Coverage of required regulatory/policy references |
| IF | Interpretive Fit | Match between field abstraction level and role expertise |
| DA | Decision Actionability | Action admissibility and mandatory field coverage |
| LP | Limitation Propagation | Fraction of material limitations propagated to passport |
| AT | Audit Traceability | Fraction of claims with complete trace records |

**N/A handling:** If a dimension is not applicable (e.g., NA when no regulatory references are required), it returns `None` and is excluded from the weighted average. Weights are renormalised over active dimensions. N/A is never treated as 1.0.

**Overall RCEA** = weighted average of active subscores, weights defined per role in `role_profiles.json`.

---

## Worked Example: Privacy/Recruitment DPO

```
Finding:  pii_entity_count = 14  (threshold: 0)
Severity: HIGH
Method:   NER + pattern-based PII scan
Reg. map: GDPR Art. 22, GDPR Art. 35, EU AI Act Annex III

DPO Passport:
  Action:                   suspend_processing
  Passport ID:              passport-c06234162581dd8f
  Visible fields:           metric, value, threshold, severity,
                            regulatory_mapping, limitations,
                            uncertainty, evidence_level
  Suppressed:               provenance_hash, method, context_tags
  Limitations propagated:   2 / 2

RCEA Scores (DPO):
  material_relevance        1.0000
  epistemic_warrant         0.6500   (tested - medium uncertainty penalty)
  normative_alignment       1.0000
  interpretive_fit          0.5000   (legal role, mix of legal/technical fields)
  decision_actionability    1.0000
  limitation_propagation    1.0000
  audit_traceability        1.0000
  ─────────────────────────────────
  Overall RCEA              0.8725

Role comparison (same finding):
  Role        Overall    Action
  dpo         0.8725     suspend_processing
  ciso        0.9222     mandate_security_review
  ai_lead     0.9028     commission_audit
  executive   0.8938     require_board_briefing
```

---

## Limitations

- All example data is **synthetic**. It does not represent any real AI system, deployment, or audit.
- RCEA scores depend on rule pack design. Poorly designed rules will produce misleading scores.
- The scoring functions are simplified operationalisations of the theoretical constructs. They do not capture all aspects of evidentiary adequacy.
- The engine performs no semantic validation of claim text beyond traceability checks.
- This implementation targets Python 3.11+ and has not been performance-optimised for large corpora.

---

## Citation

If you use this software or the RCEA framework, please cite:

```bibtex
@software{rcea_passport_engine,
  title  = {RCEA Passport Engine: Role-Conditioned Evidentiary Adequacy Reference Implementation},
  author  = {Saurabh, Roy},
  year    = {2026},
  version = {0.1.1},
  doi     = {10.5281/zenodo.20384670},
  url     = {https://github.com/roy-saurabh/rcea-passport-engine}
}
```

See also `CITATION.cff` for the CFF format citation.

---

## License

MIT License. See [LICENSE](LICENSE).
