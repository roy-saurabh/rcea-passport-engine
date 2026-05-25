# Evidence Passport

**Passport ID:** `passport-c06234162581dd8f`  
**Version:** `va54aafbb664959e5`  
**Role:** `dpo`  
**Action:** suspend_processing  

## Headline
[HIGH] Privacy finding — suspend_processing (role: dpo)

## Summary
Finding: pii_entity_count=14 (threshold: 0). Severity: high. Recommended action: suspend_processing for role dpo.

## Decision Relevance
This passport supports the 'suspend_processing' decision for role 'dpo'. Confidence: 0.87.

## Uncertainty
Medium uncertainty; interpret with caution.

## Limitations

- Validated only for English and French; other languages may have undetected PII
- NER model may miss obfuscated or encoded PII forms

## Regulatory References

- EU AI Act Annex III employment/recruitment
- GDPR Art. 22
- GDPR Art. 35

## RCEA Scores

| Dimension | Score |
|-----------|-------|
| audit_traceability | 1.0000 |
| decision_actionability | 1.0000 |
| epistemic_warrant | 0.6500 |
| interpretive_fit | 0.5000 |
| limitation_propagation | 1.0000 |
| material_relevance | 1.0000 |
| normative_alignment | 1.0000 |
| overall | 0.8725 |

## Visible Fields

- **evidence_level:** tested
- **limitations:** ['Validated only for English and French; other languages may have undetected PII', 'NER model may miss obfuscated or encoded PII forms']
- **metric:** pii_entity_count
- **regulatory_mapping:** ['GDPR Art. 22', 'GDPR Art. 35', 'EU AI Act Annex III employment/recruitment']
- **severity:** high
- **threshold:** 0
- **uncertainty:** medium
- **value:** 14

## Suppressed Fields

- **context_tags:** Internal tagging metadata not relevant to legal determination.
- **method:** Methodological detail deferred to AI Lead review.
- **provenance_hash:** Technical hash not actionable for legal review.

## Claims & Traceability

### claim-58b56dc819795ab0
Field 'evidence_level' has value 'tested' (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-6bdd797bc8965576
Field 'limitations' has value ['Validated only for English and French; other languages may have undetected PII', 'NER model may miss obfuscated or encoded PII forms'] (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-fa89b04f40acec36
Field 'metric' has value 'pii_entity_count' (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-a7c817621a0ab8a6
Field 'regulatory_mapping' has value ['GDPR Art. 22', 'GDPR Art. 35', 'EU AI Act Annex III employment/recruitment'] (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-8f1d4e508199a69e
Field 'severity' has value 'high' (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-383056d43fa6dfba
Field 'threshold' has value 0 (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-d4f928feac7002ce
Field 'uncertainty' has value 'medium' (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-2826d254ac11e911
Field 'value' has value 14 (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0

### claim-30803892d5f2f87c
Applicable regulatory references: EU AI Act Annex III employment/recruitment, GDPR Art. 22, GDPR Art. 35 (sourced from finding find-privacy-001 via rule rule-priv-dpo-001).
- Source finding: `find-privacy-001`
- Rule: `rule-priv-dpo-001` v1.0.0
