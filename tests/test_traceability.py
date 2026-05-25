"""Tests for rcea/traceability.py."""
from __future__ import annotations

import pytest

from rcea.exceptions import TraceabilityError
from rcea.passport import generate_passport
from rcea.scoring import compute_audit_traceability
from rcea.traceability import (
    validate_all_claims_have_trace,
    validate_no_unsupported_claims,
    validate_traceability_complete,
)


def test_all_claims_have_trace_privacy_dpo(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    validate_all_claims_have_trace(passport)


def test_validate_traceability_complete_returns_true(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    assert validate_traceability_complete(passport) is True


def test_audit_traceability_score_is_one(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    at = compute_audit_traceability(passport.claims)
    assert at == pytest.approx(1.0)


def test_all_examples_all_roles_have_trace(privacy_example, robustness_example, supplier_example, fairness_example):
    examples = [privacy_example, robustness_example, supplier_example, fairness_example]
    for finding, context, roles, rule_pack in examples:
        for role_id, role in roles.items():
            passport = generate_passport(finding, role, context, rule_pack)
            validate_all_claims_have_trace(passport)
            assert validate_traceability_complete(passport) is True


def test_validate_no_unsupported_claims_passes(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    for role_id, role in roles.items():
        passport = generate_passport(finding, role, context, rule_pack)
        validate_no_unsupported_claims(passport)
