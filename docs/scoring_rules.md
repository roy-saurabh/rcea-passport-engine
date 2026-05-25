# RCEA Scoring Rules

RCEA is a composite score comprising seven subscores. Each subscore measures a distinct evidentiary property. Subscores return `None` when not applicable; the aggregation renormalises weights over active dimensions.

## Subscores

### 1. Material Relevance (MR)

**Definition:** Fraction of role-required evidence fields present in the finding.

**Formula:** `MR = |{f ∈ required_fields : f ∈ evidence_fields}| / |required_fields|`

**N/A condition:** Returns `None` if `required_fields` is empty.

**Interpretation:** MR = 1.0 means the finding contains all fields the role needs. MR = 0 means no required fields are present.

---

### 2. Epistemic Warrant (EW)

**Definition:** Quality and certainty of the evidence method.

**Formula:** `EW = method_strength[evidence_level] - uncertainty_penalty[uncertainty]`, clamped to [0, 1].

Method strengths: `independently_verified=1.0`, `tested=0.75`, `documented=0.5`, `assertion=0.25`.

Uncertainty penalties: `low=0.0`, `medium=0.1`, `high=0.25`, `unknown=0.35`.

**N/A condition:** Returns `None` if the method strength rubric is empty.

---

### 3. Normative Alignment (NA)

**Definition:** Coverage of applicable regulatory/policy references.

**Formula:** `NA = |{m ∈ required_mappings : m ∈ actual_mappings}| / |required_mappings|`

**N/A condition:** Returns `None` if `required_mappings` is empty (i.e., the rule does not require regulatory references).

---

### 4. Interpretive Fit (IF)

**Definition:** Fraction of visible fields rendered at an abstraction level acceptable to the role.

**Formula:** `IF = |{f ∈ visible_fields : abstraction_level(f) ∈ acceptable_levels}| / |visible_fields|`

**N/A condition:** Returns `None` if `visible_fields` is empty.

**Field abstraction levels** (defaults): `severity → mixed`, `regulatory_mapping → legal`, `context_tags → nontechnical`, `metric/value/method/evidence_level → technical`.

---

### 5. Decision Actionability (DA)

**Definition:** Whether the recommended action is within the role's authority and all mandatory traceability fields are present.

**Formula:** `DA = (action_admissible + field_coverage) / 2`

where `action_admissible = 1.0` if `action_label ∈ admissible_actions`, else `0.0`; and `field_coverage` is the fraction of `traceability_requirement` fields present in the finding.

**N/A condition:** Returns `None` if `admissible_actions` is empty.

---

### 6. Limitation Propagation (LP)

**Definition:** Fraction of material finding limitations carried forward to the passport.

**Formula:** `LP = |{l ∈ material_limitations : l ∈ propagated_limitations}| / |material_limitations|`

**N/A condition:** Returns `None` if `material_limitations` is empty.

---

### 7. Audit Traceability (AT)

**Definition:** Fraction of passport claims that carry complete trace records.

**Formula:** `AT = |{c ∈ claims : c.trace ≠ None}| / |claims|`

Returns `1.0` if there are no claims.

---

## Overall RCEA

`RCEA = Σ(w_i * s_i) / Σ(w_i)` over active (non-None) dimensions.

Weights are role-specific and defined in the `RoleProfile.weights` field. If a weight is missing for an active dimension, it defaults to `1.0`.

**Critical rule:** N/A dimensions are excluded. They are never assigned `1.0` as a default.
