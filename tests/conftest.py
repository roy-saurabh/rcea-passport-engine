"""Shared fixtures for all tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from rcea.models import ContextPack, EvidenceFinding, RoleProfile, RulePack


def _load_example(name: str) -> tuple[EvidenceFinding, ContextPack, dict[str, RoleProfile], RulePack]:
    base = Path(__file__).parent.parent / "examples" / name
    finding = EvidenceFinding.model_validate_json((base / "finding.json").read_text())
    context = ContextPack.model_validate_json((base / "context_pack.json").read_text())
    roles_data = json.loads((base / "role_profiles.json").read_text())
    roles = {r["role_id"]: RoleProfile.model_validate(r) for r in roles_data}
    rule_pack = RulePack.model_validate_json((base / "rule_pack.json").read_text())
    return finding, context, roles, rule_pack


@pytest.fixture
def privacy_example():
    return _load_example("privacy_recruitment")


@pytest.fixture
def robustness_example():
    return _load_example("robustness_healthcare")


@pytest.fixture
def supplier_example():
    return _load_example("supplier_procurement")


@pytest.fixture
def fairness_example():
    return _load_example("fairness_credit")
