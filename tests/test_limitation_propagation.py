"""Tests for limitation propagation."""
from __future__ import annotations

import pytest

from rcea.exceptions import LimitationPropagationError
from rcea.passport import generate_passport
from rcea.rules import select_applicable_rule
from rcea.validation import validate_limitation_propagation


def test_dpo_propagates_all_limitations(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    assert len(passport.limitations) == len(finding.limitations)
    for lim in finding.limitations:
        assert lim in passport.limitations


def test_executive_has_empty_limitations(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["executive"], context, rule_pack)
    assert passport.limitations == []


def test_validate_limitation_propagation_passes_dpo(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    role = roles["dpo"]
    passport = generate_passport(finding, role, context, rule_pack)
    rule = select_applicable_rule(finding, role, context, rule_pack)
    validate_limitation_propagation(passport, finding, rule)


def test_validate_limitation_propagation_fails_when_omitted(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    role = roles["dpo"]
    passport = generate_passport(finding, role, context, rule_pack)
    rule = select_applicable_rule(finding, role, context, rule_pack)

    # Intentionally remove a limitation
    tampered = passport.model_copy(update={"limitations": []})
    with pytest.raises(LimitationPropagationError):
        validate_limitation_propagation(tampered, finding, rule)


def test_all_examples_limitation_propagation(privacy_example, robustness_example, supplier_example, fairness_example):
    examples = [privacy_example, robustness_example, supplier_example, fairness_example]
    for finding, context, roles, rule_pack in examples:
        for role_id, role in roles.items():
            passport = generate_passport(finding, role, context, rule_pack)
            rule = select_applicable_rule(finding, role, context, rule_pack)
            validate_limitation_propagation(passport, finding, rule)
