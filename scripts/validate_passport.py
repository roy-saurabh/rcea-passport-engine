#!/usr/bin/env python3
"""Validate a generated passport JSON file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rcea.models import ContextPack, EvidenceFinding, EvidencePassport, RoleProfile, RulePack
from rcea.rules import select_applicable_rule
from rcea.traceability import validate_all_claims_have_trace, validate_no_unsupported_claims
from rcea.validation import validate_limitation_propagation, validate_suppression_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an RCEA passport JSON.")
    parser.add_argument("passport_path", help="Path to passport JSON file")
    parser.add_argument("--example", required=True, help="Example directory name")
    parser.add_argument("--role", required=True, help="Role ID")
    args = parser.parse_args()

    passport_data = json.loads(Path(args.passport_path).read_text())
    passport = EvidencePassport.model_validate(passport_data)

    base = Path("examples") / args.example
    finding = EvidenceFinding.model_validate_json((base / "finding.json").read_text())
    context = ContextPack.model_validate_json((base / "context_pack.json").read_text())
    roles_data = json.loads((base / "role_profiles.json").read_text())
    roles = {r["role_id"]: RoleProfile.model_validate(r) for r in roles_data}
    rule_pack = RulePack.model_validate_json((base / "rule_pack.json").read_text())

    if args.role not in roles:
        print(f"Role '{args.role}' not found. Available: {sorted(roles.keys())}", file=sys.stderr)
        sys.exit(1)

    role = roles[args.role]
    rule = select_applicable_rule(finding, role, context, rule_pack)

    errors: list[str] = []

    for check_name, check_fn in [
        ("Traceability (all claims)", lambda: validate_all_claims_have_trace(passport)),
        ("No unsupported claims", lambda: validate_no_unsupported_claims(passport)),
        ("Limitation propagation", lambda: validate_limitation_propagation(passport, finding, rule)),
        ("Suppression logging", lambda: validate_suppression_logging(passport, rule)),
    ]:
        try:
            check_fn()
            print(f"  [PASS] {check_name}")
        except Exception as e:
            errors.append(f"[FAIL] {check_name}: {e}")
            print(f"  [FAIL] {check_name}: {e}")

    print()
    if errors:
        print(f"Validation FAILED with {len(errors)} error(s).")
        sys.exit(1)
    else:
        print(f"Passport {passport.passport_id} validated successfully.")
        print(f"Overall RCEA: {passport.overall_rcea:.4f}")


if __name__ == "__main__":
    main()
