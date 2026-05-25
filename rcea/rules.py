from __future__ import annotations

import json
from pathlib import Path

from .exceptions import RuleMatchError
from .models import ContextPack, EvidenceFinding, Rule, RulePack, RoleProfile

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def load_rule_pack(path: str | Path) -> RulePack:
    with open(path) as f:
        data = json.load(f)
    return RulePack.model_validate(data)


def _meets_severity(rule_severity: str, finding_severity: str) -> bool:
    rule_idx = _SEVERITY_ORDER.index(rule_severity) if rule_severity in _SEVERITY_ORDER else 0
    finding_idx = _SEVERITY_ORDER.index(finding_severity) if finding_severity in _SEVERITY_ORDER else 0
    return finding_idx >= rule_idx


def _meets_context_conditions(rule: Rule, context: ContextPack) -> bool:
    ctx_dict = context.model_dump()
    for key, val in rule.context_conditions.items():
        if key not in ctx_dict:
            return False
        if isinstance(val, list):
            if ctx_dict[key] not in val:
                return False
        else:
            if ctx_dict[key] != val:
                return False
    return True


def match_rules(
    finding: EvidenceFinding,
    role: RoleProfile,
    context: ContextPack,
    rule_pack: RulePack,
) -> list[Rule]:
    matched = []
    for rule in rule_pack.rules:
        if rule.role_id != role.role_id:
            continue
        if rule.finding_family != finding.finding_family.value:
            continue
        if not _meets_severity(rule.severity_minimum, finding.severity.value):
            continue
        if not _meets_context_conditions(rule, context):
            continue
        matched.append(rule)
    return matched


def select_applicable_rule(
    finding: EvidenceFinding,
    role: RoleProfile,
    context: ContextPack,
    rule_pack: RulePack,
) -> Rule:
    matched = match_rules(finding, role, context, rule_pack)
    if not matched:
        raise RuleMatchError(
            f"No rule matched: finding_family={finding.finding_family.value}, "
            f"role={role.role_id}, severity={finding.severity.value}"
        )
    return sorted(matched, key=lambda r: r.rule_id)[0]


def validate_rule_pack(rule_pack: RulePack) -> None:
    seen_ids: set[str] = set()
    for rule in rule_pack.rules:
        if rule.rule_id in seen_ids:
            raise ValueError(f"Duplicate rule_id: {rule.rule_id}")
        seen_ids.add(rule.rule_id)


def ensure_rule_pack_version(rule_pack: RulePack) -> str:
    return rule_pack.version
