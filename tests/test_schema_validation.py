"""Tests for JSON schema validation."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rcea.passport import generate_passport
from rcea.validation import validate_json_schema, validate_passport_schema

SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"


def test_finding_json_validates_against_schema(privacy_example):
    finding, _, _, _ = privacy_example
    data = json.loads(finding.model_dump_json())
    validate_json_schema(data, SCHEMAS_DIR / "finding.schema.json")


def test_context_pack_json_validates_against_schema(privacy_example):
    _, context, _, _ = privacy_example
    data = json.loads(context.model_dump_json())
    validate_json_schema(data, SCHEMAS_DIR / "context_pack.schema.json")


def test_rule_pack_json_validates_against_schema(privacy_example):
    _, _, _, rule_pack = privacy_example
    data = json.loads(rule_pack.model_dump_json())
    validate_json_schema(data, SCHEMAS_DIR / "rule_pack.schema.json")


def test_passport_validates_against_schema_dpo(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)
    validate_passport_schema(passport, SCHEMAS_DIR)


def test_all_examples_passports_validate(privacy_example, robustness_example, supplier_example, fairness_example):
    examples = [privacy_example, robustness_example, supplier_example, fairness_example]
    for finding, context, roles, rule_pack in examples:
        for role_id, role in roles.items():
            passport = generate_passport(finding, role, context, rule_pack)
            validate_passport_schema(passport, SCHEMAS_DIR)


def test_example_finding_files_validate_against_schema():
    examples_dir = Path(__file__).parent.parent / "examples"
    for example_dir in sorted(examples_dir.iterdir()):
        finding_path = example_dir / "finding.json"
        if finding_path.exists():
            data = json.loads(finding_path.read_text())
            validate_json_schema(data, SCHEMAS_DIR / "finding.schema.json")
