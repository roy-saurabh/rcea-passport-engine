"""Tests that no unsupported claims are generated."""
from __future__ import annotations

import pytest

from rcea.exceptions import UnsupportedClaimError
from rcea.models import PassportClaim, TraceRecord
from rcea.passport import generate_passport
from rcea.traceability import validate_no_unsupported_claims
from datetime import datetime, timezone


def test_no_unsupported_claims_all_examples(privacy_example, robustness_example, supplier_example, fairness_example):
    examples = [privacy_example, robustness_example, supplier_example, fairness_example]
    for finding, context, roles, rule_pack in examples:
        for role_id, role in roles.items():
            passport = generate_passport(finding, role, context, rule_pack)
            validate_no_unsupported_claims(passport)


def test_unsupported_claim_raises_error(privacy_example):
    finding, context, roles, rule_pack = privacy_example
    passport = generate_passport(finding, roles["dpo"], context, rule_pack)

    # Inject a claim referencing a field not in visible_fields
    fake_trace = TraceRecord(
        claim_id="claim-fake",
        source_finding_id=finding.finding_id,
        source_hash=finding.provenance_hash,
        source_method=finding.method,
        source_timestamp=finding.timestamp,
        applied_rule_id="rule-fake",
        applied_rule_version="1.0.0",
        context_pack_id=context.context_pack_id,
        context_pack_version=context.version,
        role_id="dpo",
        passport_version=passport.passport_version,
    )
    fake_claim = PassportClaim(
        claim_id="claim-fake",
        text="This claim references a non-visible field.",
        visible_fields_used=["provenance_hash"],  # suppressed field
        trace=fake_trace,
    )
    tampered = passport.model_copy(
        update={"claims": passport.claims + [fake_claim]}
    )
    with pytest.raises(UnsupportedClaimError):
        validate_no_unsupported_claims(tampered)
