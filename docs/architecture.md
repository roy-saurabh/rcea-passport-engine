# Architecture

## Overview

The RCEA Passport Engine implements a deterministic pipeline that transforms a common AI audit evidence substrate into role-conditioned evidence passports. Each passport is tailored to the information needs, authority scope, and expertise level of a specific governance role.

## The RCEA Pipeline

The pipeline has four stages:

1. **Evidence ingestion.** An `EvidenceFinding` captures a single auditable finding from the AI system under evaluation. It carries metric values, severity, method, uncertainty, regulatory mappings, and limitations. A `ContextPack` encodes the deployment context: jurisdiction, sector, risk class, regulatory baseline.

2. **Rule matching.** The `RuleMatcher` selects the applicable `Rule` from the `RulePack` by filtering on `role_id`, `finding_family`, `severity_minimum`, and `context_conditions`. If multiple rules match, the lexicographically first `rule_id` is chosen for determinism.

3. **Passport generation.** The `PassportGenerator` applies the selected rule to produce an `EvidencePassport`. It: (a) projects the finding through `visible_fields` and `suppressed_fields`; (b) creates a trace record for every claim; (c) writes a suppression log entry for every suppressed field; (d) propagates material limitations when the rule requires it; and (e) computes all RCEA subscores and the weighted overall score.

4. **Validation.** The `validation` and `traceability` modules verify that every claim traces to a source finding and rule, that no claim references a suppressed field, that required limitations are present, and that suppression logs are complete.

## Role of the Rule Pack

The `RulePack` is the sole source of role-conditioned policy. It specifies which fields are visible to each role, which are suppressed, what action label is recommended, whether limitations must be propagated, and whether regulatory references are required. Changing the rule pack without changing its version is an integrity violation; the passport version hash encodes the rule pack version, making version drift detectable.

## Suppression and Traceability

Every suppressed field produces a `SuppressionLog` entry with a rationale and a `retrievable=True` flag, indicating that the underlying data can be recovered through the audit trail. Every passport claim carries a `TraceRecord` linking it to the source finding hash, the applied rule, the context pack, and the role. This enables post-hoc contestability of governance decisions.

## Score Aggregation

RCEA subscores are computed per-dimension and then aggregated via role-weighted average. If a dimension is not applicable (e.g., normative alignment when no regulatory references are required), it returns `None` and is excluded from aggregation; weights are renormalised over the remaining active set. This avoids artificially inflating scores for roles that do not bear regulatory liability.
