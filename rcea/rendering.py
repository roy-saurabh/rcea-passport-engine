from __future__ import annotations

import json
from pathlib import Path

from .models import EvidencePassport


def render_passport_markdown(passport: EvidencePassport) -> str:
    lines = [
        "# Evidence Passport",
        "",
        f"**Passport ID:** `{passport.passport_id}`  ",
        f"**Version:** `{passport.passport_version}`  ",
        f"**Role:** `{passport.role_id}`  ",
        f"**Action:** {passport.action_label}  ",
        "",
        "## Headline",
        passport.headline,
        "",
        "## Summary",
        passport.summary,
        "",
        "## Decision Relevance",
        passport.decision_relevance,
        "",
        "## Uncertainty",
        passport.uncertainty_statement,
        "",
    ]

    if passport.limitations:
        lines += ["## Limitations", ""]
        for lim in passport.limitations:
            lines.append(f"- {lim}")
        lines.append("")

    if passport.regulatory_or_policy_references:
        lines += ["## Regulatory References", ""]
        for ref in passport.regulatory_or_policy_references:
            lines.append(f"- {ref}")
        lines.append("")

    lines += ["## RCEA Scores", "", "| Dimension | Score |", "|-----------|-------|"]
    for k, v in sorted(passport.rcea_scores.items()):
        lines.append(f"| {k} | {v:.4f} |")
    lines.append("")

    lines += ["## Visible Fields", ""]
    for k, v in sorted(passport.visible_fields.items()):
        lines.append(f"- **{k}:** {v}")
    lines.append("")

    if passport.suppressed_fields:
        lines += ["## Suppressed Fields", ""]
        for entry in passport.suppression_log:
            lines.append(f"- **{entry.field}:** {entry.rationale}")
        lines.append("")

    lines += ["## Claims & Traceability", ""]
    for claim in passport.claims:
        lines += [
            f"### {claim.claim_id}",
            claim.text,
            f"- Source finding: `{claim.trace.source_finding_id}`",
            f"- Rule: `{claim.trace.applied_rule_id}` v{claim.trace.applied_rule_version}",
            "",
        ]

    return "\n".join(lines)


def render_passport_html(passport: EvidencePassport) -> str:
    md = render_passport_markdown(passport)
    escaped = (
        md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return (
        f'<!DOCTYPE html>\n<html lang="en">\n<head>'
        f'<meta charset="UTF-8">'
        f'<title>Evidence Passport {passport.passport_id}</title>\n'
        f'<style>body{{font-family:monospace;max-width:900px;margin:2em auto;padding:0 1em}}</style>\n'
        f'</head>\n<body><pre>{escaped}</pre></body>\n</html>'
    )


def save_passport_json(passport: EvidencePassport, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(passport.model_dump_json())
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True, default=str)
