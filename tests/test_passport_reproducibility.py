"""Tests for passport reproducibility."""
from __future__ import annotations

import copy
import json

import pytest

from rcea.exceptions import ReproducibilityError
from rcea.models import RulePack
from rcea.passport import generate_passport
from rcea.validation import validate_passport_reproducibility


def test_same_inputs_produce_same_passport_id(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    p1 = generate_passport(finding, roles["dpo"], context, rule_pack)
    p2 = generate_passport(finding, roles["dpo"], context, rule_pack)
    assert p1.passport_id == p2.passport_id
    assert p1.passport_version == p2.passport_version


def test_same_inputs_produce_same_scores(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    p1 = generate_passport(finding, roles["dpo"], context, rule_pack)
    p2 = generate_passport(finding, roles["dpo"], context, rule_pack)
    assert p1.overall_rcea == p2.overall_rcea
    assert p1.rcea_scores == p2.rcea_scores


def test_validate_passport_reproducibility_passes(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    p1 = generate_passport(finding, roles["dpo"], context, rule_pack)
    p2 = generate_passport(finding, roles["dpo"], context, rule_pack)
    validate_passport_reproducibility(p1, p2)


def test_validate_passport_reproducibility_fails_on_tamper(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    p1 = generate_passport(finding, roles["dpo"], context, rule_pack)
    p2 = generate_passport(finding, roles["dpo"], context, rule_pack)
    tampered = p2.model_copy(update={"overall_rcea": p2.overall_rcea + 0.1})
    with pytest.raises(ReproducibilityError):
        validate_passport_reproducibility(p1, tampered)


def test_changing_rule_pack_version_changes_passport_version(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    p1 = generate_passport(finding, roles["dpo"], context, rule_pack)

    # Create modified rule pack with bumped version
    rp_data = json.loads(rule_pack.model_dump_json())
    rp_data["version"] = "2.0.0"
    rule_pack_v2 = RulePack.model_validate(rp_data)
    p2 = generate_passport(finding, roles["dpo"], context, rule_pack_v2)

    assert p1.passport_version != p2.passport_version


def test_all_roles_reproducible(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    for role_id, role in roles.items():
        p1 = generate_passport(finding, role, context, rule_pack)
        p2 = generate_passport(finding, role, context, rule_pack)
        validate_passport_reproducibility(p1, p2)
