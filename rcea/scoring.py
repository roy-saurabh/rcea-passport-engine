from __future__ import annotations

from typing import Optional

from .models import PassportClaim

METHOD_STRENGTH: dict[str, float] = {
    "independently_verified": 1.0,
    "tested": 0.75,
    "documented": 0.5,
    "assertion": 0.25,
}

_UNCERTAINTY_PENALTY: dict[str, float] = {
    "low": 0.0,
    "medium": 0.1,
    "high": 0.25,
    "unknown": 0.35,
}


def compute_material_relevance(
    evidence_fields: list[str],
    required_fields: list[str],
) -> Optional[float]:
    """Fraction of required fields present in evidence. None if required_fields is empty."""
    if not required_fields:
        return None
    present = sum(1 for f in required_fields if f in evidence_fields)
    return present / len(required_fields)


def compute_epistemic_warrant(
    evidence_level: str,
    uncertainty: str,
    method_strength_rubric: dict[str, float],
    importance_weights: Optional[dict[str, float]] = None,
) -> Optional[float]:
    """Score based on evidence level and uncertainty. None only if rubric is empty."""
    if not method_strength_rubric:
        return None
    base = method_strength_rubric.get(evidence_level, 0.25)
    penalty = _UNCERTAINTY_PENALTY.get(uncertainty, 0.2)
    return max(0.0, min(1.0, base - penalty))


def compute_normative_alignment(
    actual_mappings: list[str],
    required_mappings: list[str],
) -> Optional[float]:
    """Fraction of required regulatory mappings present. None if required_mappings is empty."""
    if not required_mappings:
        return None
    present = sum(1 for m in required_mappings if m in actual_mappings)
    return present / len(required_mappings)


def compute_interpretive_fit(
    rendered_fields: list[str],
    acceptable_levels: list[str],
    field_levels: dict[str, str],
) -> Optional[float]:
    """Fraction of rendered fields at acceptable abstraction levels. None if rendered_fields is empty."""
    if not rendered_fields:
        return None
    fit = sum(
        1 for f in rendered_fields
        if field_levels.get(f, "technical") in acceptable_levels
    )
    return fit / len(rendered_fields)


def compute_decision_actionability(
    action_label: str,
    admissible_actions: list[str],
    mandatory_action_fields: list[str],
    passport_fields: list[str],
) -> Optional[float]:
    """1.0 if action admissible and all mandatory fields present, else partial. None if admissible_actions empty."""
    if not admissible_actions:
        return None
    action_ok = 1.0 if action_label in admissible_actions else 0.0
    if not mandatory_action_fields:
        field_ok = 1.0
    else:
        present = sum(1 for f in mandatory_action_fields if f in passport_fields)
        field_ok = present / len(mandatory_action_fields)
    return (action_ok + field_ok) / 2.0


def compute_limitation_propagation(
    material_limitations: list[str],
    propagated_limitations: list[str],
    limitation_notice: Optional[str] = None,
) -> Optional[float]:
    """Fraction of material limitations propagated. None if material_limitations is empty.
    A limitation_notice counts as one partial credit even without verbatim match."""
    if not material_limitations:
        return None
    propagated = sum(1 for lim in material_limitations if lim in propagated_limitations)
    if limitation_notice is not None:
        propagated = max(propagated, 1)
    return min(propagated, len(material_limitations)) / len(material_limitations)


def compute_audit_traceability(claims: list[PassportClaim]) -> float:
    """Fraction of claims with complete trace records. Returns 1.0 if no claims."""
    if not claims:
        return 1.0
    traced = sum(1 for c in claims if c.trace is not None)
    return traced / len(claims)


def compute_overall_rcea(
    subscores: dict[str, Optional[float]],
    weights: dict[str, float],
) -> float:
    """Weighted average over non-None subscores. Renormalises weights for N/A dimensions."""
    active = {k: v for k, v in subscores.items() if v is not None}
    if not active:
        return 0.0
    active_weights = {k: weights.get(k, 1.0) for k in active}
    total_w = sum(active_weights.values())
    if total_w == 0.0:
        return 0.0
    return sum(active[k] * active_weights[k] for k in active) / total_w
