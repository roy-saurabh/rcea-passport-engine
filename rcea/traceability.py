from __future__ import annotations

from .exceptions import TraceabilityError, UnsupportedClaimError
from .models import ContextPack, EvidenceFinding, EvidencePassport, Rule, RoleProfile, TraceRecord


def validate_trace_record(
    trace: TraceRecord,
    finding: EvidenceFinding,
    rule: Rule,
    context: ContextPack,
    role: RoleProfile,
    passport: EvidencePassport,
) -> None:
    if trace.source_finding_id != finding.finding_id:
        raise TraceabilityError(
            f"Trace source_finding_id mismatch: {trace.source_finding_id} != {finding.finding_id}"
        )
    if trace.applied_rule_id != rule.rule_id:
        raise TraceabilityError(
            f"Trace rule_id mismatch: {trace.applied_rule_id} != {rule.rule_id}"
        )
    if trace.context_pack_id != context.context_pack_id:
        raise TraceabilityError(
            f"Trace context_pack_id mismatch: {trace.context_pack_id} != {context.context_pack_id}"
        )
    if trace.role_id != role.role_id:
        raise TraceabilityError(
            f"Trace role_id mismatch: {trace.role_id} != {role.role_id}"
        )
    if trace.passport_version != passport.passport_version:
        raise TraceabilityError(
            f"Trace passport_version mismatch: {trace.passport_version} != {passport.passport_version}"
        )


def validate_all_claims_have_trace(passport: EvidencePassport) -> None:
    for claim in passport.claims:
        if claim.trace is None:
            raise TraceabilityError(f"Claim {claim.claim_id} has no trace record")


def validate_no_unsupported_claims(passport: EvidencePassport) -> None:
    """Every claim's visible_fields_used must be a subset of visible_fields keys or regulatory_mapping."""
    visible_keys = set(passport.visible_fields.keys()) | {"regulatory_mapping"}
    for claim in passport.claims:
        for field in claim.visible_fields_used:
            if field not in visible_keys:
                raise UnsupportedClaimError(
                    f"Claim {claim.claim_id} references field '{field}' not in visible_fields"
                )


def validate_traceability_complete(passport: EvidencePassport) -> bool:
    try:
        validate_all_claims_have_trace(passport)
        return True
    except TraceabilityError:
        return False
