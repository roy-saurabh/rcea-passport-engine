#!/usr/bin/env python3
"""Compute and display RCEA subscores for a given example and role."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rcea.models import ContextPack, EvidenceFinding, RoleProfile, RulePack
from rcea.passport import generate_passport


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute RCEA subscores.")
    parser.add_argument("--example", required=True, help="Example directory name")
    parser.add_argument("--role", required=True, help="Role ID")
    args = parser.parse_args()

    base = Path("examples") / args.example
    if not base.exists():
        print(f"Example directory not found: {base}", file=sys.stderr)
        sys.exit(1)

    finding = EvidenceFinding.model_validate_json((base / "finding.json").read_text())
    context = ContextPack.model_validate_json((base / "context_pack.json").read_text())
    roles_data = json.loads((base / "role_profiles.json").read_text())
    roles = {r["role_id"]: RoleProfile.model_validate(r) for r in roles_data}
    rule_pack = RulePack.model_validate_json((base / "rule_pack.json").read_text())

    if args.role not in roles:
        print(
            f"Role '{args.role}' not found. Available: {sorted(roles.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    passport = generate_passport(finding, roles[args.role], context, rule_pack)

    print(f"\nRCEA Scores — example={args.example}, role={args.role}")
    print("=" * 56)
    for k, v in sorted(passport.rcea_scores.items()):
        if k == "overall":
            continue
        print(f"  {k:<32} {v:.4f}")
    print("-" * 56)
    print(f"  {'Overall RCEA':<32} {passport.overall_rcea:.4f}")
    print()
    print(f"  Action label:    {passport.action_label}")
    print(f"  Passport ID:     {passport.passport_id}")


if __name__ == "__main__":
    main()
