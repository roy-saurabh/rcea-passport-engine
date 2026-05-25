from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class FindingFamily(str, Enum):
    privacy = "privacy"
    fairness = "fairness"
    robustness = "robustness"
    security = "security"
    explainability = "explainability"
    documentation = "documentation"
    governance = "governance"
    supplier = "supplier"


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Uncertainty(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    unknown = "unknown"


class EvidenceLevel(str, Enum):
    assertion = "assertion"
    documented = "documented"
    tested = "tested"
    independently_verified = "independently_verified"


class RoleName(str, Enum):
    dpo = "dpo"
    ciso = "ciso"
    ai_lead = "ai_lead"
    procurement = "procurement"
    executive = "executive"
    vendor = "vendor"
    platform_admin = "platform_admin"


class ExpertiseLevel(str, Enum):
    nontechnical = "nontechnical"
    mixed = "mixed"
    technical = "technical"
    legal = "legal"
    security = "security"
    executive = "executive"


class EvidenceFinding(BaseModel):
    finding_id: str
    finding_family: FindingFamily
    metric: str
    value: Union[int, float, str, bool, dict, list]
    threshold: Optional[Union[int, float, str, bool, dict, list]] = None
    severity: Severity
    method: str
    uncertainty: Uncertainty
    limitations: list[str]
    regulatory_mapping: list[str]
    context_tags: list[str]
    provenance_hash: str
    timestamp: datetime
    evidence_level: EvidenceLevel


class ContextPack(BaseModel):
    context_pack_id: str
    jurisdiction: str
    sector: str
    system_purpose: str
    risk_class: str
    deployment_stage: str
    affected_population: str
    data_modality: list[str]
    supplier_status: str
    regulatory_baseline: list[str]
    policy_baseline: list[str]
    version: str


class RoleProfile(BaseModel):
    role_id: str
    role_name: RoleName
    authority: list[str]
    liability: list[str]
    expertise_level: ExpertiseLevel
    admissible_actions: list[str]
    acceptable_abstraction_levels: list[str]
    evidence_needs: list[str]
    weights: dict[str, float]


class Rule(BaseModel):
    rule_id: str
    version: str
    role_id: str
    finding_family: str
    severity_minimum: str
    context_conditions: dict
    required_fields: list[str]
    visible_fields: list[str]
    suppressed_fields: list[str]
    action_label: str
    action_rationale_template: str
    limitation_propagation_required: bool
    regulatory_reference_required: bool
    traceability_requirement: list[str]
    suppression_rationale: dict[str, str]


class RulePack(BaseModel):
    rule_pack_id: str
    version: str
    rules: list[Rule]


class TraceRecord(BaseModel):
    claim_id: str
    source_finding_id: str
    source_hash: str
    source_method: str
    source_timestamp: datetime
    applied_rule_id: str
    applied_rule_version: str
    context_pack_id: str
    context_pack_version: str
    role_id: str
    passport_version: str


class PassportClaim(BaseModel):
    claim_id: str
    text: str
    visible_fields_used: list[str]
    trace: TraceRecord


class SuppressionLog(BaseModel):
    field: str
    role_id: str
    rule_id: str
    rule_version: str
    rationale: str
    retrievable: bool


class EvidencePassport(BaseModel):
    passport_id: str
    passport_version: str
    role_id: str
    action_label: str
    headline: str
    summary: str
    decision_relevance: str
    visible_fields: dict
    suppressed_fields: list[str]
    suppression_log: list[SuppressionLog]
    limitations: list[str]
    uncertainty_statement: str
    regulatory_or_policy_references: list[str]
    claims: list[PassportClaim]
    rcea_scores: dict[str, float]
    overall_rcea: float
    expires_at: Optional[datetime] = None
