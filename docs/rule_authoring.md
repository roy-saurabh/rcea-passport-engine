# Rule Authoring Guide

Rules are stored in `rule_pack.json` files inside each example directory. A `RulePack` contains a `rule_pack_id`, a semantic `version`, and a list of `Rule` objects.

## Rule Fields

| Field | Type | Description |
|-------|------|-------------|
| `rule_id` | str | Unique identifier within the rule pack. |
| `version` | str | Semantic version of this individual rule. |
| `role_id` | str | The role this rule targets. Must match a `RoleProfile.role_id`. |
| `finding_family` | str | The finding family this rule applies to (e.g., `privacy`, `fairness`). |
| `severity_minimum` | str | Minimum finding severity for rule to apply (`low`, `medium`, `high`, `critical`). |
| `context_conditions` | dict | Key-value conditions on `ContextPack` fields. All must match. |
| `required_fields` | list[str] | Fields the role needs; used for Material Relevance scoring. |
| `visible_fields` | list[str] | Fields projected into the passport's `visible_fields`. |
| `suppressed_fields` | list[str] | Fields not shown to this role; each must have a `suppression_rationale` entry. |
| `action_label` | str | Recommended governance action for this role. |
| `action_rationale_template` | str | Python `.format()` template for the passport summary. Available keys: `metric`, `value`, `threshold`, `severity`, `method`, `uncertainty`, `role`, `action`. |
| `limitation_propagation_required` | bool | If true, all finding limitations must appear in the passport. |
| `regulatory_reference_required` | bool | If true, regulatory mappings appear in the passport and count toward NA score. |
| `traceability_requirement` | list[str] | Fields that must be present in the finding for full Decision Actionability credit. |
| `suppression_rationale` | dict[str,str] | Maps each suppressed field name to a human-readable rationale. |

## Authoring Guidelines

1. **One rule per role per finding family per context.** Do not create ambiguous overlapping rules; the engine picks lexicographically by `rule_id`.
2. **`visible_fields` and `suppressed_fields` must not overlap.** All finding fields should appear in one or the other.
3. **Every entry in `suppressed_fields` must have a corresponding entry in `suppression_rationale`.** Missing entries will cause validation failures.
4. **Bump `rule.version` whenever you change a rule.** This propagates to `passport_version` via the deterministic hash.
5. **Bump `rule_pack.version` whenever you add, remove, or modify any rule.** Passport hashes encode the rule pack version.
6. **Keep `action_label` within the role's `admissible_actions`.** A mismatch reduces the Decision Actionability score.

## Example Minimal Rule

```json
{
  "rule_id": "rule-privacy-dpo-example",
  "version": "1.0.0",
  "role_id": "dpo",
  "finding_family": "privacy",
  "severity_minimum": "medium",
  "context_conditions": {"sector": "recruitment"},
  "required_fields": ["metric", "value", "regulatory_mapping"],
  "visible_fields": ["metric", "value", "severity", "regulatory_mapping"],
  "suppressed_fields": ["provenance_hash", "method"],
  "action_label": "suspend_processing",
  "action_rationale_template": "Finding: {metric}={value}. Severity: {severity}. Action: {action}.",
  "limitation_propagation_required": true,
  "regulatory_reference_required": true,
  "traceability_requirement": ["metric", "value"],
  "suppression_rationale": {
    "provenance_hash": "Technical hash not actionable for legal review.",
    "method": "Methodological detail deferred to AI Lead."
  }
}
```
