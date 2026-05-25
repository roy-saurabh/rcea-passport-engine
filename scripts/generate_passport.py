#!/usr/bin/env python3
"""Generate an evidence passport for a given example and role."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rcea.models import ContextPack, EvidenceFinding, RoleProfile, RulePack
from rcea.passport import generate_passport
from rcea.rendering import render_passport_markdown, save_passport_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an RCEA evidence passport.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate_passport.py --example privacy_recruitment --role dpo \\
      --out examples/privacy_recruitment/outputs/dpo_passport.json
  python scripts/generate_passport.py --example fairness_credit --role ai_lead \\
      --out examples/fairness_credit/outputs/ai_lead_passport.json --markdown out.md
""",
    )
    parser.add_argument("--example", required=True, help="Example directory name")
    parser.add_argument("--role", required=True, help="Role ID")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--markdown", help="Optional Markdown output path")
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
    save_passport_json(passport, args.out)
    print(f"Passport saved:  {args.out}")
    print(f"Passport ID:     {passport.passport_id}")
    print(f"Version:         {passport.passport_version}")
    print(f"Overall RCEA:    {passport.overall_rcea:.4f}")
    print(f"Action:          {passport.action_label}")

    if args.markdown:
        md = render_passport_markdown(passport)
        Path(args.markdown).write_text(md)
        print(f"Markdown saved:  {args.markdown}")


if __name__ == "__main__":
    main()
