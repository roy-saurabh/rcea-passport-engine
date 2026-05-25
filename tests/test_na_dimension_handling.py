"""Tests for N/A dimension handling and weight renormalisation."""
from __future__ import annotations

import pytest

from rcea.scoring import (
    compute_material_relevance,
    compute_normative_alignment,
    compute_overall_rcea,
    compute_limitation_propagation,
)
from rcea.passport import generate_passport


def test_empty_required_fields_returns_none():
    assert compute_material_relevance(["a", "b"], []) is None


def test_empty_required_mappings_returns_none():
    assert compute_normative_alignment(["GDPR Art. 5"], []) is None


def test_empty_material_limitations_returns_none():
    assert compute_limitation_propagation([], ["some limitation"]) is None


def test_all_none_subscores_return_zero():
    result = compute_overall_rcea(
        {"mr": None, "ew": None, "na": None},
        {"mr": 0.4, "ew": 0.3, "na": 0.3},
    )
    assert result == pytest.approx(0.0)


def test_one_none_subscore_renormalises():
    # 'na' is None; only 'mr'=1.0 and 'ew'=0.0 remain
    # weights: mr=0.5, ew=0.5; total active weight = 1.0
    result = compute_overall_rcea(
        {"mr": 1.0, "ew": 0.0, "na": None},
        {"mr": 0.5, "ew": 0.5, "na": 0.5},
    )
    # (1.0*0.5 + 0.0*0.5) / (0.5+0.5) = 0.5
    assert result == pytest.approx(0.5)


def test_na_dimension_does_not_default_to_one(privacy_example):
    """If a dimension is N/A, it must not be counted as 1.0."""
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["executive"], context, rule_pack)
    # executive rule has no regulatory_reference_required, so normative_alignment may be None
    # overall_rcea must NOT be the same as if na=1.0
    scores = passport.rcea_scores
    # overall should be computed only over present scores
    from rcea.scoring import compute_overall_rcea as coro
    expected = coro(
        {k: v for k, v in scores.items() if k != "overall"},
        roles["executive"].weights,
    )
    assert passport.overall_rcea == pytest.approx(expected)


def test_overall_rcea_missing_weight_defaults_to_one():
    # If a key is present in subscores but not in weights, default weight=1.0
    result = compute_overall_rcea({"x": 0.6}, {})
    assert result == pytest.approx(0.6)
