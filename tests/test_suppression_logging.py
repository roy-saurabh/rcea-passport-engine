"""Tests for suppression logging."""
from __future__ import annotations

import pytest

from rcea.exceptions import SuppressionLogError
from rcea.passport import generate_passport
from rcea.rules import select_applicable_rule
from rcea.validation import validate_suppression_logging


def test_every_suppressed_field_has_log_entry(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    for role_id, role in roles.items():
        passport = generate_passport(finding, role, context, rule_pack)
        rule = select_applicable_rule(finding, role, context, rule_pack)
        logged_fields = {log.field for log in passport.suppression_log}
        for field in rule.suppressed_fields:
            assert field in logged_fields, f"Role {role_id}: suppressed field '{field}' not in suppression log"


def test_validate_suppression_logging_passes(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    for role_id, role in roles.items():
        passport = generate_passport(finding, role, context, rule_pack)
        rule = select_applicable_rule(finding, role, context, rule_pack)
        validate_suppression_logging(passport, rule)


def test_validate_suppression_logging_fails_when_entry_missing(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    role = roles["dpo"]
    passport = generate_passport(finding, role, context, rule_pack)
    rule = select_applicable_rule(finding, role, context, rule_pack)

    # Remove all suppression log entries
    tampered = passport.model_copy(update={"suppression_log": []})
    with pytest.raises(SuppressionLogError):
        validate_suppression_logging(tampered, rule)


def test_all_examples_suppression_logging(privacy_example, robustness_example, supplier_example, fairness_example):
    examples = [privacy_example, robustness_example, supplier_example, fairness_example]
    for finding, context, roles, rule_pack in examples:
        for role_id, role in roles.items():
            passport = generate_passport(finding, role, context, rule_pack)
            rule = select_applicable_rule(finding, role, context, rule_pack)
            validate_suppression_logging(passport, rule)


def test_suppression_log_includes_rationale(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    for entry in passport.suppression_log:
        assert entry.rationale, f"Empty rationale for field '{entry.field}'"
        assert entry.retrievable is True
