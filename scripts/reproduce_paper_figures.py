#!/usr/bin/env python3
"""Reproduce paper figures as Mermaid diagrams."""
from __future__ import annotations

from pathlib import Path

OUTPUT_DIR = Path("paper_artifacts/figures")

_PIPELINE = """\
# Figure 1 — RCEA Pipeline

```mermaid
flowchart LR
    F[Evidence Finding] --> M[Rule Matcher]
    C[Context Pack]     --> M
    R[Role Profile]     --> M
    RP[Rule Pack]       --> M
    M  --> RU[Selected Rule]
    RU --> PG[Passport Generator]
    F  --> PG
    C  --> PG
    R  --> PG
    PG --> VF[Visible Fields]
    PG --> SL[Suppression Log]
    PG --> LP[Limitations]
    PG --> CL[Claims + Traces]
    PG --> SC[RCEA Scores]
    VF --> EP[Evidence Passport]
    SL --> EP
    LP --> EP
    CL --> EP
    SC --> EP
    style EP fill:#2d6a4f,color:#fff
```
"""

_ARCHITECTURE = """\
# Figure 2 — Evidence Passport Architecture

```mermaid
classDiagram
    class EvidenceFinding {
        +finding_id : str
        +finding_family : FindingFamily
        +metric : str
        +value : Any
        +severity : Severity
        +method : str
        +uncertainty : Uncertainty
        +limitations : list[str]
        +regulatory_mapping : list[str]
        +evidence_level : EvidenceLevel
    }
    class EvidencePassport {
        +passport_id : str
        +passport_version : str
        +role_id : str
        +action_label : str
        +visible_fields : dict
        +suppressed_fields : list[str]
        +suppression_log : list[SuppressionLog]
        +limitations : list[str]
        +claims : list[PassportClaim]
        +rcea_scores : dict[str,float]
        +overall_rcea : float
    }
    class PassportClaim {
        +claim_id : str
        +text : str
        +trace : TraceRecord
    }
    class TraceRecord {
        +claim_id : str
        +source_finding_id : str
        +applied_rule_id : str
        +role_id : str
        +passport_version : str
    }
    class SuppressionLog {
        +field : str
        +role_id : str
        +rule_id : str
        +rationale : str
        +retrievable : bool
    }
    EvidencePassport "1" --> "*" PassportClaim
    EvidencePassport "1" --> "*" SuppressionLog
    PassportClaim    "1" --> "1" TraceRecord
```
"""

_SCORE_AGGREGATION = """\
# Figure 3 — RCEA Score Aggregation

```mermaid
flowchart TD
    MR[Material Relevance MR]       --> W[Weighted Sum]
    EW[Epistemic Warrant EW]        --> W
    NA[Normative Alignment NA]      --> W
    IF[Interpretive Fit IF]         --> W
    DA[Decision Actionability DA]   --> W
    LP[Limitation Propagation LP]   --> W
    AT[Audit Traceability AT]       --> W
    W  --> O[Overall RCEA Score]
    N/A([N/A dimension]) -. excluded .-> W
    style O  fill:#2d6a4f,color:#fff
    style N/A fill:#aaa,color:#fff
```

> N/A dimensions are excluded; weights are renormalised over the remaining active set.
"""

_WORKED_EXAMPLE = """\
# Figure 4 — Worked Example: Privacy/Recruitment Finding Transformation

```mermaid
flowchart LR
    subgraph Input
        F[Finding: pii_entity_count=14\\nseverity=high]
        C[Context: sector=recruitment\\njurisdiction=EU]
        RP[Rule pack: rp-privacy-recruit-001 v1.0.0]
    end
    subgraph RoleViews
        DPO[DPO Passport\\nAction: suspend_processing\\nVisible: metric, value, threshold,\\n severity, regulatory_mapping,\\n limitations]
        CISO[CISO Passport\\nAction: mandate_security_review\\nVisible: metric, value, method,\\n severity, limitations]
        AIL[AI Lead Passport\\nAction: commission_audit\\nVisible: metric, value, threshold,\\n method, uncertainty, limitations]
        EXEC[Executive Passport\\nAction: require_board_briefing\\nVisible: severity, context_tags,\\n finding_family]
    end
    Input --> DPO
    Input --> CISO
    Input --> AIL
    Input --> EXEC
```
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    figures = {
        "fig1_rcea_pipeline.md": _PIPELINE,
        "fig2_passport_architecture.md": _ARCHITECTURE,
        "fig3_score_aggregation.md": _SCORE_AGGREGATION,
        "fig4_worked_example.md": _WORKED_EXAMPLE,
    }
    for filename, content in figures.items():
        path = OUTPUT_DIR / filename
        path.write_text(content)
        print(f"Figure written: {path}")
    print("\nAll paper figures generated.")


if __name__ == "__main__":
    main()
