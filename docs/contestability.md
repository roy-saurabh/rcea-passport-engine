# Contestability

The RCEA Passport Engine is designed to support the contestability of AI governance decisions. Two mechanisms make this possible.

## Suppression Logs

When a field is suppressed from a role's view, a `SuppressionLog` entry records: the field name, the role for which it was suppressed, the rule and rule version that caused the suppression, a human-readable rationale, and a `retrievable=True` flag.

The `retrievable` flag indicates that the underlying evidence is not destroyed — it remains in the audit trail and can be surfaced by a role with appropriate authority (e.g., a platform administrator or independent auditor). Any affected party who receives a passport and disputes its basis can invoke the suppression log to identify what was withheld and why, and request access through the appropriate governance channel.

## Trace Records

Every passport claim carries a `TraceRecord` linking it to:
- the source finding ID and provenance hash (integrity of the evidence);
- the applied rule ID and version (the policy that shaped the view);
- the context pack ID and version (the deployment context used);
- the role ID (the intended audience);
- the passport version hash (reproducibility anchor).

This means that for any claim in any passport, a reviewer can reconstruct exactly what evidence was used, which rule produced the view, and whether a different rule pack version would have changed the outcome. Combined with the limitation propagation mechanism — which ensures material caveats are surfaced where required — the passport architecture supports structured challenge of governance decisions without requiring access to the full audit corpus.
