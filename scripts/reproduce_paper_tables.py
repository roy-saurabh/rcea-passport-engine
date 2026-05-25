#!/usr/bin/env python3
"""Reproduce paper tables as CSV and Markdown."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rcea.models import ContextPack, EvidenceFinding, RoleProfile, RulePack
from rcea.passport import generate_passport

OUTPUT_DIR = Path("paper_artifacts/tables")

EXAMPLES: list[tuple[str, list[str]]] = [
    ("privacy_recruitment", ["dpo", "ciso", "ai_lead", "executive"]),
    ("robustness_healthcare", ["ciso", "ai_lead", "executive"]),
    ("supplier_procurement", ["procurement", "vendor", "executive"]),
    ("fairness_credit", ["dpo", "ai_lead", "executive"]),
]

SUBCONSTRUCTS = [
    ("Material Relevance", "MR", "Fraction of role-required evidence fields present in the finding"),
    ("Epistemic Warrant", "EW", "Quality and certainty of the evidence method, penalised for uncertainty"),
    ("Normative Alignment", "NA", "Coverage of applicable regulatory/policy references"),
    ("Interpretive Fit", "IF", "Match between evidence abstraction level and role expertise"),
    ("Decision Actionability", "DA", "Whether the recommended action is within role authority and all mandatory fields present"),
    ("Limitation Propagation", "LP", "Fraction of material limitations carried forward to passport"),
    ("Audit Traceability", "AT", "Fraction of passport claims with complete trace records"),
]

ROLE_TAXONOMY = [
    ("dpo", "Data Protection Officer", "legal", "GDPR compliance, data subject rights", "suspend_processing, require_dpia"),
    ("ciso", "Chief Information Security Officer", "security", "Information security, incident response", "halt_deployment, mandate_security_review"),
    ("ai_lead", "AI/ML Lead Engineer", "technical", "Model performance, technical compliance", "commission_audit, require_retraining"),
    ("procurement", "Procurement Officer", "mixed", "Procurement compliance, vendor risk", "suspend_vendor_contract, request_attestation"),
    ("executive", "Executive / Board Member", "executive", "Organisational risk, regulatory exposure", "halt_programme, require_board_briefing"),
    ("vendor", "AI System Vendor", "mixed", "Attestation accuracy, contractual compliance", "provide_attestation"),
    ("platform_admin", "Platform Administrator", "technical", "System integrity, operational continuity", "admin actions"),
]


def _load_example(name: str) -> tuple[EvidenceFinding, ContextPack, dict[str, RoleProfile], RulePack]:
    base = Path("examples") / name
    finding = EvidenceFinding.model_validate_json((base / "finding.json").read_text())
    context = ContextPack.model_validate_json((base / "context_pack.json").read_text())
    roles_data = json.loads((base / "role_profiles.json").read_text())
    roles = {r["role_id"]: RoleProfile.model_validate(r) for r in roles_data}
    rule_pack = RulePack.model_validate_json((base / "rule_pack.json").read_text())
    return finding, context, roles, rule_pack


def generate_subconstruct_table() -> None:
    csv_path = OUTPUT_DIR / "subconstructs.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["construct", "symbol", "description"])
        writer.writeheader()
        for name, sym, desc in SUBCONSTRUCTS:
            writer.writerow({"construct": name, "symbol": sym, "description": desc})

    md_lines = ["# RCEA Subconstruct Definitions", "",
                "| Construct | Symbol | Description |",
                "|-----------|--------|-------------|"]
    for name, sym, desc in SUBCONSTRUCTS:
        md_lines.append(f"| {name} | {sym} | {desc} |")
    (OUTPUT_DIR / "subconstructs.md").write_text("\n".join(md_lines) + "\n")
    print(f"Subconstruct table written to {csv_path}")


def generate_role_taxonomy_table() -> None:
    fieldnames = ["role_id", "role_name", "expertise_level", "liability", "typical_actions"]
    csv_path = OUTPUT_DIR / "role_taxonomy.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in ROLE_TAXONOMY:
            writer.writerow(dict(zip(fieldnames, row)))

    md_lines = ["# Role Taxonomy", "",
                "| Role ID | Role Name | Expertise | Liability | Typical Actions |",
                "|---------|-----------|-----------|-----------|-----------------|"]
    for row in ROLE_TAXONOMY:
        md_lines.append("| " + " | ".join(row) + " |")
    (OUTPUT_DIR / "role_taxonomy.md").write_text("\n".join(md_lines) + "\n")
    print(f"Role taxonomy table written to {csv_path}")


def generate_rcea_score_table() -> None:
    all_score_keys = ["material_relevance", "epistemic_warrant", "normative_alignment",
                      "interpretive_fit", "decision_actionability", "limitation_propagation",
                      "audit_traceability", "overall"]
    rows: list[dict] = []

    for example_name, role_ids in EXAMPLES:
        finding, context, roles, rule_pack = _load_example(example_name)
        for role_id in role_ids:
            if role_id not in roles:
                continue
            passport = generate_passport(finding, roles[role_id], context, rule_pack)
            row: dict = {"example": example_name, "role": role_id}
            for k in all_score_keys:
                v = passport.rcea_scores.get(k)
                row[k] = f"{v:.4f}" if v is not None else "N/A"
            row["overall"] = f"{passport.overall_rcea:.4f}"
            rows.append(row)

    fieldnames = ["example", "role"] + all_score_keys
    csv_path = OUTPUT_DIR / "rcea_scores.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    md_lines = ["# RCEA Scores by Example and Role", ""]
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join(["---"] * len(fieldnames)) + " |"
    md_lines += [header, separator]
    for row in rows:
        md_lines.append("| " + " | ".join(row.get(k, "—") for k in fieldnames) + " |")
    (OUTPUT_DIR / "rcea_scores.md").write_text("\n".join(md_lines) + "\n")
    print(f"RCEA score table written to {csv_path}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_subconstruct_table()
    generate_role_taxonomy_table()
    generate_rcea_score_table()
    print("\nAll paper tables generated.")


if __name__ == "__main__":
    main()
