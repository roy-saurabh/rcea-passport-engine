"""Tests for rcea/scoring.py."""
from __future__ import annotations

import pytest

from rcea.scoring import (
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


def test_material_relevance_empty_required_returns_none():
    assert compute_material_relevance(["a", "b"], []) is None


def test_material_relevance_full_match():
    assert compute_material_relevance(["a", "b", "c"], ["a", "b"]) == 1.0


def test_material_relevance_partial():
    result = compute_material_relevance(["a"], ["a", "b"])
    assert result == pytest.approx(0.5)


def test_material_relevance_no_match():
    assert compute_material_relevance(["a"], ["b", "c"]) == pytest.approx(0.0)


def test_epistemic_warrant_empty_rubric_returns_none():
    assert compute_epistemic_warrant("tested", "low", {}) is None


def test_epistemic_warrant_high_evidence_low_uncertainty():
    result = compute_epistemic_warrant("independently_verified", "low", METHOD_STRENGTH)
    assert result == pytest.approx(1.0)


def test_epistemic_warrant_tested_medium_uncertainty():
    result = compute_epistemic_warrant("tested", "medium", METHOD_STRENGTH)
    assert result == pytest.approx(0.65)


def test_epistemic_warrant_clamped_to_zero():
    result = compute_epistemic_warrant("assertion", "unknown", METHOD_STRENGTH)
    assert result >= 0.0


def test_normative_alignment_empty_required_returns_none():
    assert compute_normative_alignment(["GDPR Art. 5"], []) is None


def test_normative_alignment_full_coverage():
    actual = ["GDPR Art. 22", "GDPR Art. 35"]
    required = ["GDPR Art. 22"]
    assert compute_normative_alignment(actual, required) == pytest.approx(1.0)


def test_normative_alignment_partial():
    actual = ["GDPR Art. 22"]
    required = ["GDPR Art. 22", "EU AI Act Art. 9"]
    assert compute_normative_alignment(actual, required) == pytest.approx(0.5)


def test_interpretive_fit_empty_fields_returns_none():
    assert compute_interpretive_fit([], ["mixed"], {"severity": "mixed"}) is None


def test_interpretive_fit_all_match():
    result = compute_interpretive_fit(
        ["severity"], ["mixed"], {"severity": "mixed"}
    )
    assert result == pytest.approx(1.0)


def test_interpretive_fit_none_match():
    result = compute_interpretive_fit(
        ["metric"], ["nontechnical"], {"metric": "technical"}
    )
    assert result == pytest.approx(0.0)


def test_decision_actionability_empty_admissible_returns_none():
    assert compute_decision_actionability("suspend", [], [], []) is None


def test_decision_actionability_full():
    result = compute_decision_actionability(
        "suspend_processing",
        ["suspend_processing", "escalate"],
        ["metric"],
        ["metric", "value"],
    )
    assert result == pytest.approx(1.0)


def test_decision_actionability_action_not_admissible():
    result = compute_decision_actionability(
        "unknown_action",
        ["suspend_processing"],
        [],
        [],
    )
    assert result == pytest.approx(0.5)


def test_limitation_propagation_empty_material_returns_none():
    assert compute_limitation_propagation([], ["something"]) is None


def test_limitation_propagation_full():
    lims = ["lim1", "lim2"]
    assert compute_limitation_propagation(lims, lims) == pytest.approx(1.0)


def test_limitation_propagation_partial():
    result = compute_limitation_propagation(["lim1", "lim2"], ["lim1"])
    assert result == pytest.approx(0.5)


def test_audit_traceability_empty_claims_returns_one():
    assert compute_audit_traceability([]) == pytest.approx(1.0)


def test_overall_rcea_all_none_returns_zero():
    result = compute_overall_rcea({"a": None, "b": None}, {"a": 0.5, "b": 0.5})
    assert result == pytest.approx(0.0)


def test_overall_rcea_one_none_renormalises():
    # b is None, so only 'a' contributes; weight renormalised to 1.0
    result = compute_overall_rcea({"a": 0.8, "b": None}, {"a": 0.5, "b": 0.5})
    assert result == pytest.approx(0.8)


def test_overall_rcea_weighted():
    scores = {"a": 1.0, "b": 0.0}
    weights = {"a": 0.75, "b": 0.25}
    result = compute_overall_rcea(scores, weights)
    assert result == pytest.approx(0.75)
