from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .models import (
    ContextPack,
    EvidenceFinding,
    EvidencePassport,
    PassportClaim,
    RoleProfile,
    Rule,
    RulePack,
    SuppressionLog,
    TraceRecord,
)
from .rules import select_applicable_rule
from .scoring import (
    METHOD_STRENGTH,
    compute_audit_traceability,
    compute_decision_actionability,
    compute_epistemic_warrant,
    compute_interpretive_fit,
    compute_limitation_propagation,
    compute_material_relevance,
    compute_normative_alignment,
    compute_overall_rcea,
)

_FIELD_ABSTRACTION_LEVELS: dict[str, str] = {
    "metric": "technical",
    "value": "technical",
    "threshold": "technical",
    "severity": "mixed",
    "method": "technical",
    "uncertainty": "mixed",
    "limitations": "mixed",
    "regulatory_mapping": "legal",
    "context_tags": "nontechnical",
    "evidence_level": "technical",
    "finding_family": "mixed",
    "finding_id": "technical",
    "provenance_hash": "technical",
    "timestamp": "mixed",
}

_UNCERTAINTY_STATEMENTS: dict[str, str] = {
    "low": "Low uncertainty; findings are well-supported.",
    "medium": "Medium uncertainty; interpret with caution.",
    "high": "High uncertainty; treat findings as indicative only.",
    "unknown": "Uncertainty is unknown; treat findings conservatively.",
}


def _stable_hash(data: dict) -> str:
    blob = json.dumps(data, sort_keys=True, default=str).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def build_headline(finding: EvidenceFinding, role: RoleProfile, rule: Rule) -> str:
    severity = finding.severity.value.upper()
    family = finding.finding_family.value.replace("_", " ").title()
    return f"[{severity}] {family} finding — {rule.action_label} (role: {role.role_id})"


def build_summary(finding: EvidenceFinding, role: RoleProfile, rule: Rule) -> str:
    template = rule.action_rationale_template
    ctx = {
        "metric": finding.metric,
        "value": finding.value,
        "threshold": finding.threshold,
        "severity": finding.severity.value,
        "method": finding.method,
        "uncertainty": finding.uncertainty.value,
        "role": role.role_id,
        "action": rule.action_label,
    }
    try:
        return template.format(**ctx)
    except KeyError:
        return template


def build_visible_fields(finding: EvidenceFinding, rule: Rule) -> dict:
    finding_dict = json.loads(finding.model_dump_json())
    result: dict = {}
    for field in sorted(rule.visible_fields):
        if field in finding_dict:
            result[field] = finding_dict[field]
    return result


def build_suppression_log(
    finding: EvidenceFinding, rule: Rule, role: RoleProfile
) -> list[SuppressionLog]:
    logs: list[SuppressionLog] = []
    for field in sorted(rule.suppressed_fields):
        rationale = rule.suppression_rationale.get(field, "Suppressed per role policy.")
        logs.append(SuppressionLog(
            field=field,
            role_id=role.role_id,
            rule_id=rule.rule_id,
            rule_version=rule.version,
            rationale=rationale,
            retrievable=True,
        ))
    return logs


def propagate_limitations(finding: EvidenceFinding, rule: Rule) -> list[str]:
    if rule.limitation_propagation_required:
        return list(finding.limitations)
    return []


def assign_action_label(rule: Rule) -> str:
    return rule.action_label


def create_claim(
    text: str,
    finding: EvidenceFinding,
    rule: Rule,
    context: ContextPack,
    role: RoleProfile,
    passport_version: str,
    claim_id: str,
    visible_fields_used: list[str],
) -> PassportClaim:
    trace = TraceRecord(
        claim_id=claim_id,
        source_finding_id=finding.finding_id,
        source_hash=finding.provenance_hash,
        source_method=finding.method,
        source_timestamp=finding.timestamp,
        applied_rule_id=rule.rule_id,
        applied_rule_version=rule.version,
        context_pack_id=context.context_pack_id,
        context_pack_version=context.version,
        role_id=role.role_id,
        passport_version=passport_version,
    )
    return PassportClaim(
        claim_id=claim_id,
        text=text,
        visible_fields_used=visible_fields_used,
        trace=trace,
    )


def _build_claims(
    finding: EvidenceFinding,
    rule: Rule,
    context: ContextPack,
    role: RoleProfile,
    visible_fields: dict,
    passport_version: str,
) -> list[PassportClaim]:
    claims: list[PassportClaim] = []

    for field_name in sorted(visible_fields.keys()):
        claim_id = f"claim-{_stable_hash({'finding': finding.finding_id, 'role': role.role_id, 'field': field_name, 'version': passport_version})}"
        text = (
            f"Field '{field_name}' has value {repr(visible_fields[field_name])} "
            f"(sourced from finding {finding.finding_id} via rule {rule.rule_id})."
        )
        claims.append(create_claim(
            text=text,
            finding=finding,
            rule=rule,
            context=context,
            role=role,
            passport_version=passport_version,
            claim_id=claim_id,
            visible_fields_used=[field_name],
        ))

    if rule.regulatory_reference_required and finding.regulatory_mapping:
        claim_id = f"claim-{_stable_hash({'finding': finding.finding_id, 'role': role.role_id, 'field': 'regulatory', 'version': passport_version})}"
        refs = ", ".join(sorted(finding.regulatory_mapping))
        text = (
            f"Applicable regulatory references: {refs} "
            f"(sourced from finding {finding.finding_id} via rule {rule.rule_id})."
        )
        claims.append(create_claim(
            text=text,
            finding=finding,
            rule=rule,
            context=context,
            role=role,
            passport_version=passport_version,
            claim_id=claim_id,
            visible_fields_used=["regulatory_mapping"],
        ))

    return claims


def _compute_scores(
    finding: EvidenceFinding,
    rule: Rule,
    role: RoleProfile,
    visible_fields: dict,
    propagated_limitations: list[str],
    claims: list[PassportClaim],
) -> dict[str, float | None]:
    finding_field_names = list(json.loads(finding.model_dump_json()).keys())

    mr = compute_material_relevance(finding_field_names, rule.required_fields)
    ew = compute_epistemic_warrant(
        finding.evidence_level.value,
        finding.uncertainty.value,
        METHOD_STRENGTH,
    )

    required_regulatory: list[str] = []
    if rule.regulatory_reference_required and finding.regulatory_mapping:
        required_regulatory = finding.regulatory_mapping[:1]
    na = compute_normative_alignment(finding.regulatory_mapping, required_regulatory)

    inf = compute_interpretive_fit(
        list(visible_fields.keys()),
        role.acceptable_abstraction_levels,
        _FIELD_ABSTRACTION_LEVELS,
    )
    da = compute_decision_actionability(
        rule.action_label,
        role.admissible_actions,
        rule.traceability_requirement,
        finding_field_names,
    )
    lp = compute_limitation_propagation(finding.limitations, propagated_limitations)
    at = compute_audit_traceability(claims)

    return {
        "material_relevance": mr,
        "epistemic_warrant": ew,
        "normative_alignment": na,
        "interpretive_fit": inf,
        "decision_actionability": da,
        "limitation_propagation": lp,
        "audit_traceability": at,
    }


def generate_passport(
    finding: EvidenceFinding,
    role: RoleProfile,
    context: ContextPack,
    rule_pack: RulePack,
) -> EvidencePassport:
    rule = select_applicable_rule(finding, role, context, rule_pack)

    version_input = {
        "finding_id": finding.finding_id,
        "role_id": role.role_id,
        "context_pack_id": context.context_pack_id,
        "rule_pack_id": rule_pack.rule_pack_id,
        "rule_pack_version": rule_pack.version,
        "rule_id": rule.rule_id,
        "rule_version": rule.version,
    }
    passport_version = f"v{_stable_hash(version_input)}"
    passport_id = f"passport-{_stable_hash({**version_input, 'type': 'id'})}"

    visible_fields = build_visible_fields(finding, rule)
    suppression_log = build_suppression_log(finding, rule, role)
    propagated_limitations = propagate_limitations(finding, rule)
    claims = _build_claims(finding, rule, context, role, visible_fields, passport_version)

    headline = build_headline(finding, role, rule)
    summary = build_summary(finding, role, rule)

    scores = _compute_scores(finding, rule, role, visible_fields, propagated_limitations, claims)
    overall = compute_overall_rcea(scores, role.weights)

    rcea_scores_out: dict[str, float] = {k: v for k, v in scores.items() if v is not None}
    rcea_scores_out["overall"] = overall

    regulatory_refs = sorted(finding.regulatory_mapping) if rule.regulatory_reference_required else []

    decision_relevance = (
        f"This passport supports the '{rule.action_label}' decision for role '{role.role_id}'. "
        f"Confidence: {overall:.2f}."
    )

    return EvidencePassport(
        passport_id=passport_id,
        passport_version=passport_version,
        role_id=role.role_id,
        action_label=rule.action_label,
        headline=headline,
        summary=summary,
        decision_relevance=decision_relevance,
        visible_fields=visible_fields,
        suppressed_fields=sorted(rule.suppressed_fields),
        suppression_log=suppression_log,
        limitations=propagated_limitations,
        uncertainty_statement=_UNCERTAINTY_STATEMENTS.get(
            finding.uncertainty.value, "Uncertainty level unspecified."
        ),
        regulatory_or_policy_references=regulatory_refs,
        claims=claims,
        rcea_scores=rcea_scores_out,
        overall_rcea=overall,
        expires_at=None,
    )
