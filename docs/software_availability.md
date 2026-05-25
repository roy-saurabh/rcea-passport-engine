# Software Availability Statement

The RCEA Passport Engine is freely available under the MIT License. Source code is hosted at:

> https://github.com/roy-saurabh/rcea-passport-engine

A permanently archived snapshot is deposited at Zenodo:

> https://doi.org/10.5281/zenodo.20384670

The repository contains only synthetic example data. No personal data, proprietary models, or external API calls are included. All computation is deterministic and self-contained. The software requires Python 3.11 or later and the `pydantic` and `jsonschema` packages.

To install and run:

```bash
pip install -e .
python scripts/generate_passport.py --example privacy_recruitment --role dpo \
    --out examples/privacy_recruitment/outputs/dpo_passport.json
```

To reproduce all paper tables and figures:

```bash
python scripts/reproduce_paper_tables.py
python scripts/reproduce_paper_figures.py
```

All outputs are written to `paper_artifacts/tables/` and `paper_artifacts/figures/`.
