**Role-Conditioned Evidentiary Adequacy**

*A Formal Construct and Accountability-Preserving Architecture for AI Governance Evidence*

Anonymous Author(s)

*Anonymous Institution*

*Submission target: ACM FAccT 2027 · Revised draft (theory and methods paper)*

**Abstract**

AI governance decisions are rarely made by a single actor. Data protection officers, security leaders, procurement teams, technical reviewers, suppliers, administrators, and executive owners may rely on the same underlying assessment evidence, yet they differ in authority, liability, expertise, decision rights, and action horizons. Existing AI evaluation systems typically expose flat metric reports or static documentation artefacts (model cards, datasheets, system cards), assuming that transparency is achieved once technical outputs are made visible. We argue that such undifferentiated reporting is structurally insufficient for organisational AI accountability, and that the missing scientific object is not better visualisation but a formal model of role-conditioned evidentiary adequacy.

This paper makes three contributions. **First**, we introduce *role-conditioned evidentiary adequacy* (RCEA), a construct specifying when a shared AI evidence body is adequate for a specific accountable role, decision task, and governance context. We decompose RCEA into seven dimensions and, for each, give a computable scoring rule over the evidence body, the role profile, the action, and the governance context. **Second**, we present a reference architecture for *accountability-preserving interpretation*: a deterministic, versioned mapping from a common evidence substrate to role-conditioned evidence passport views, with audit traceability enforced structurally. We anonymise the reference implementation as *System P* for double-blind review. **Third**, we provide an *evaluation framework*: a separation of objective RCEA (computed from substrate and rule pack), perceived RCEA (a candidate eight-item scale to be psychometrically validated), and decision-quality outcomes, together with a measurement protocol and explicit threats to validity.

We position role-conditioned evidence not as a user-interface convenience but as a structural requirement for accountable AI governance in multi-stakeholder organisations. The paper argues that evidence *availability* and evidence *transparency* do not by themselves yield evidence *adequacy*, and that progressive disclosure is admissible—indeed required—provided audit traceability and contestability are preserved. We do not report empirical results; the evaluation framework is the methodological contribution that future empirical work, including our own, can instantiate.

**Keywords:** AI accountability, AI governance, evidence passports, audit infrastructure, multi-stakeholder governance, evidentiary adequacy, interpretive fit, progressive disclosure, contestability, AI assurance.

# **1\.  Introduction**

Organisational governance of AI systems is conducted as a multi-actor activity. A single deployment may pass through privacy review by a data protection officer (DPO), security review by a Chief Information Security Officer (CISO) or security lead, methodological review by an AI lead, procurement review by a contracts and compliance officer, executive sign-off by an accountable owner, and ongoing operational checks by a platform administrator. Each of these actors is differently authorised, differently exposed to liability, differently trained, and differently positioned in the decision lifecycle. Yet the evidence on which they must act is typically presented as a single, undifferentiated technical artefact: a metric dashboard, an evaluation report, a model card \[Mitchell et al. 2019\], a datasheet \[Gebru et al. 2021\], a system card, an assurance case \[Bloomfield & Rushby 2019; Arnold et al. 2019\], or a static PDF.

Current AI assurance and audit platforms tend to assume that producing more evidence, more openly, is sufficient for accountability \[Raji et al. 2020; Brundage et al. 2020\]. This assumption conflates three distinct properties: *availability* (the evidence exists somewhere in the system), *transparency* (the evidence can be inspected or disclosed), and *adequacy* (the evidence can validly support a role-specific accountable decision). A DPO does not merely need to see a fairness metric; they need to understand whether the finding is material to lawful processing, automated decision-making, affected data subjects, and required safeguards under the General Data Protection Regulation \[GDPR 2016; Wachter et al. 2017; Edwards & Veale 2017\]. A CISO does not merely need to see an adversarial robustness score; they need to know whether the finding constitutes an exploitable attack surface or operational resilience concern. A procurement officer does not merely need model-performance outputs; they need evidence of supplier obligations, attestations, gaps, expiry, and contractual risk. The same evidence body can be technically complete and yet decision-insufficient for any one of these roles.

The intuition that “different stakeholders need different summaries” is widespread in explainable AI \[Miller 2019; Arrieta et al. 2020\] and in risk communication \[Fischhoff 1995; Gigerenzer 2002; Morgan et al. 2002\]. We argue that this intuition, however common, is too weak to ground a governance claim. Calling for tailored summaries treats the problem as one of personalisation. We instead treat it as a problem of *evidentiary adequacy*: the relation between an evidence body, an accountable role, a decision action, and a governance context. Role-conditioned views are not a UX courtesy; they are a structural condition for accountability when shared evidence is acted upon by actors with different decision rights.

**Contributions.** *(C1) A formal construct with computable subconstructs.* We define RCEA(E, r, a, C) over an evidence body E, role r, action a, and context C, decompose it into seven dimensions, and give computable scoring rules for each (§3). *(C2) A reference architecture.* We describe an accountability-preserving interpretation layer that maps a common evidence substrate to role-conditioned evidence passport views through a versioned deterministic rule pack, enforcing audit traceability and limitation propagation structurally (§5). The reference implementation is referred to as *System P*; the public name is anonymised for double-blind review and will be restored upon acceptance. *(C3) An evaluation framework with explicit construct separation.* We separate objective RCEA (computable from substrate and rule pack), perceived RCEA (a candidate scale), usability, and decision-quality outcomes, and we specify measurement instruments and threats to validity (§7).

**Scope.** This is a theory and methods paper. We do not claim empirical validation. We deliberately specify the construct, the architecture, and the evaluation framework precisely enough that we and others can subsequently test them.

The remainder of the paper proceeds as follows. §2 reviews related work. §3 develops the construct with computable subscores. §4 derives the governance role taxonomy from regulatory and management-systems instruments. §5 presents System P and differentiates the evidence passport from prior documentation artefacts. §6 works a single privacy finding through four role views. §7 sets out the evaluation framework. §8 addresses contestability and rule-pack governance. §9 discusses implications. §10–11 treat threats to validity, adverse impacts, and limitations.

# **2\.  Related Work**

**Explanation and audience.** Explainable AI research has long acknowledged that explanations must be evaluated relative to recipients \[Miller 2019; Arrieta et al. 2020\], and law-and-AI scholarship has examined whether and when “rights to explanation” attach to particular decision actors \[Wachter et al. 2017; Selbst & Barocas 2018; Edwards & Veale 2017\]. This literature treats audiences as cognitive or expertise categories rather than as accountability positions with formal decision rights, and rarely formalises adequacy for a specific governance *action*.

**Algorithmic auditing and documentation.** Model cards \[Mitchell et al. 2019\], datasheets \[Gebru et al. 2021\], FactSheets \[Arnold et al. 2019\], and assurance cases \[Bloomfield & Rushby 2019\] are structured artefacts that document the system itself; the audit literature \[Raji et al. 2020; Metcalf et al. 2021; Costanza-Chock et al. 2022; Mökander et al. 2023; Birhane et al. 2024\] situates these artefacts in organisational and ecosystem context. The recurring observation in this work is that documentation does not by itself produce accountable decisions; intermediary practices, institutional embedding, and contestability matter \[Watkins et al. 2021; Reisman et al. 2018\]. Our work formalises the missing relational property: when documentation *is* or *is not* adequate for a specific accountable role’s decision.

**Risk communication and decision framing.** Risk-communication research has shown that the same evidence can systematically support or undermine appropriate decisions depending on framing, abstraction level, and uncertainty representation \[Fischhoff 1995; Gigerenzer 2002; Morgan et al. 2002\]. These results have rarely been imported into AI governance with attention to formal accountability roles.

**CSCW: boundary objects, articulation work, and classification.** CSCW research on cross-role collaboration, boundary objects, articulation work, and classification infrastructures provides empirical grounding for how artefacts mediate distributed accountability \[Star & Griesemer 1989; Bowker & Star 1999; Schmidt & Bannon 1992; Suchman 1996; Strauss 1985\]. An evidence passport is, in CSCW terms, a boundary object that preserves a non-negotiable shared substrate; we develop this within a formal-model frame.

**Regulatory and management-systems instruments.** The EU AI Act \[EU 2024; Veale & Borgesius 2021\] assigns distinct obligations to providers, deployers, importers, distributors, authorised representatives, and notified bodies, and imposes technical documentation and human-oversight requirements. The NIST AI Risk Management Framework \[NIST 2023\] structures governance through Govern/Map/Measure/Manage functions. ISO/IEC 42001 \[ISO 2023\] formalises an AI management system. GDPR \[GDPR 2016\] prescribes controller/processor/DPO roles and DPIA obligations. These instruments specify *what* must be documented but leave *how* that documentation supports specific accountable roles’ decisions to implementers. Our work supplies a construct and architecture for that gap.

**Gap.** Across these literatures, three properties are routinely conflated: that evidence *exists*, that it is *visible*, and that it is *usable for a specific accountable decision*. We are not aware of prior work that (a) formally separates the third property as a distinct construct, (b) provides computable subconstructs, and (c) demonstrates a reference architecture that satisfies it without sacrificing a common auditable substrate. This paper addresses that gap.

# **3\.  Role-Conditioned Evidentiary Adequacy**

## **3.1  Three Distinct Properties**

***Table** 1\. Three commonly-conflated properties of governance evidence.*

| Property | Meaning | Why insufficient alone |
| :---- | :---- | :---- |
| Availability | Technical outputs exist somewhere in the system. | Evidence can exist but remain unusable for governance decisions. |
| Transparency | Evidence can be inspected or disclosed. | Raw visibility does not ensure correct interpretation. |
| Adequacy | Evidence can validly support a role-specific accountable decision. | The construct this paper addresses. |

## **3.2  Definition**

**Definition (Role-Conditioned Evidentiary Adequacy).** *Role-conditioned evidentiary adequacy is the degree to which a shared AI governance evidence body is materially relevant, epistemically warranted, normatively aligned, interpretable, actionable, uncertainty-aware, and auditable for a specific accountable role making a specific governance decision in a specific organisational and regulatory context.*

## **3.3  Formal Model**

The evidence body is a set of findings E \= { f₁, …, fₙ }. Each finding is a tuple

fᵢ \= ⟨ type, metric, value, method, threshold, uncertainty,

provenance, limitation, regulatory\_mapping, context ⟩.

A role profile is r \= ⟨ authority, liability, expertise, decision\_rights, horizon, needs ⟩. A decision action is drawn from A \= { approve, approve\_with\_conditions, request\_evidence, escalate, block, reassess }. A governance context is C \= ⟨ sector, jurisdiction, system\_purpose, risk\_class, deployment\_stage, affected\_population ⟩.

We then define RCEA : (E, r, a, C) ↦ \[0, 1\] as the degree to which E supports r taking action a in context C.

## **3.4  Seven Subconstructs with Computable Scoring Rules**

We decompose RCEA into seven dimensions and give a scoring rule for each. Each rule produces a value in \[0, 1\] and is computed from the substrate, the role-action-context-conditioned requirement set (specified by the rule pack of §5), and the rendered passport view V.

Let F\_E be the set of evidence fields actually present in the substrate for the relevant findings, and FᵣᵉƵ\_(r,a,C) the role/action/context-conditioned set of required fields. Let V\_(r,a,C) be the rendered passport view; let claims(V) be its set of distinct claims; let trace(c) be the trace record for claim c.

**Material relevance.**

MR \= | F\_E ∩ FᵣᵉƵ\_(r,a,C) | / | FᵣᵉƵ\_(r,a,C) |.

**Epistemic warrant.** For each finding fⱼ relevant to (r, a, C) with importance weight qⱼ ∈ \[0, 1\] set by the rule pack, let σ(fⱼ) ∈ \[0, 1\] be the method-strength score against the required standard (1 if method meets or exceeds the standard, 0 if not, intermediate values for partial standards).

EW \= ( Σⱼ  qⱼ · σ(fⱼ) ) / ( Σⱼ  qⱼ ).

**Normative alignment.** Let M\_E be the set of regulatory/policy mappings present in the substrate and MᵣᵉƵ\_(r,a,C) the mappings required.

NA \= | M\_E ∩ MᵣᵉƵ\_(r,a,C) | / | MᵣᵉƵ\_(r,a,C) |.

**Interpretive fit.** Each rendered field v ∈ V\_(r,a,C) has an abstraction level ℓ(v) on an ordered scale (raw ≺ method ≺ normalised ≺ narrative ≺ executive). Let Lᵒᵏ(r) be the role-acceptable abstraction set.

IF \= ( 1 / |V\_(r,a,C)| ) · Σᵥ  ᵽ\[ ℓ(v) ∈ Lᵒᵏ(r) \].

**Decision actionability.** The passport must propose an action a\* ∈ A that is admissible for r and structurally complete. Let ℱ(a) denote the set of mandatory action fields (label, rationale, evidence trace, deadline or expiry, responsible role).

DA \= ᵽ\[ a\* ∈ Aᵃᵈᵐ\_r \] · | ℱ(a\*) ∩ V | / | ℱ(a\*) |.

**Uncertainty and limitation propagation.** Let Lᵐᵃᵗ\_(r,a,C) be the substrate limitations material to (r, a, C) and L\_V the limitations propagated into V.

ULP \= | Lᵐᵃᵗ\_(r,a,C) ∩ L\_V | / | Lᵐᵃᵗ\_(r,a,C) |.

**Audit traceability.**

AT \= | { c ∈ claims(V) : trace(c) is valid } | / | claims(V) |.

A trace is valid iff it resolves to a source finding, method, timestamp, evidence hash, applied rule (with version), context-pack (with version), and role profile, and the rule version is current at passport issuance time.

## **3.5  Weighted Adequacy Function**

We combine the seven subscores as a role-weighted sum:

RCEA(E, r, a, C) \= w₁ˣ MR \+ w₂ˣ EW \+ w₃ˣ NA \+ w₄ˣ IF

\+ w₅ˣ DA \+ w₆ˣ ULP \+ w₇ˣ AT,

with Σₖ wₖˣ \= 1 and wₖˣ ≥ 0\. The role-specific weights wₖˣ are not assumed a priori; they are derived from expert elicitation as specified in §7. The qualitative pattern we expect (Table 2\) is theoretically motivated and empirically falsifiable.

***Table** 2\. Theoretically-motivated role-weight pattern for the seven RCEA dimensions. Empirical estimation procedure is given in §7.*

| Dimension | DPO | CISO | AI Lead | Procure. | Exec. |
| :---- | :---: | :---: | :---: | :---: | :---: |
| **Material relevance** | High | High | High | High | High |
| **Epistemic warrant** | Med. | High | V. High | Med. | Med. |
| **Normative alignment** | V. High | High | Med. | High | High |
| **Interpretive fit** | High | High | High | High | V. High |
| **Decision actionability** | V. High | High | High | V. High | V. High |
| **Limitation propagation** | V. High | High | V. High | High | High |
| **Audit traceability** | High | High | V. High | V. High | High |

## **3.6  Objective and Perceived RCEA**

The function above defines *objective* RCEA: a value computed from the substrate, the rule pack, and the rendered view, with no participant input. *Perceived* RCEA is a separately measured psychological construct: the actor’s appraisal of whether the evidence they were shown supported their decision. The two are distinct: a passport can be objectively adequate yet perceived as inadequate (e.g., when interpretive fit is off), and vice versa. We treat their relationship as a testable empirical question (§7).

## **3.7  Accountability-Preserving Interpretation**

**Definition (Accountability-Preserving Interpretation).** *The transformation of a common evidence body into role-conditioned views such that each view is decision-sufficient for its intended governance role while all claims remain traceable to the same underlying evidence record, rule pack, limitations, and version history.*

An architecture satisfies accountability-preserving interpretation iff (i) every role view derives deterministically from one immutable substrate under a versioned rule pack, (ii) AT \= 1 on every emitted passport, and (iii) suppressed fields remain retrievable under audit.

# **4\.  Governance Role Taxonomy**

The taxonomy below describes roles as *accountability positions* with distinct decision rights and liability exposures, not as audiences. Table 3 shows the derivation from regulatory and management-systems instruments; Table 4 states each role’s authority, exposure, evidence need, and admissible actions.

***Table** 3\. Derivation of the role taxonomy from regulatory and management-systems instruments.*

| Source | Role concepts extracted | Mapped role(s) in this paper |
| :---- | :---- | :---- |
| EU AI Act \[EU 2024; Veale & Borgesius 2021\] | provider, deployer, importer, distributor, authorised representative, notified body, natural persons assigned to human oversight | Vendor/Supplier; Executive/Owner; Procurement Officer; AI Lead; Platform Administrator |
| NIST AI RMF \[NIST 2023\] | Govern/Map/Measure/Manage functions and role assignments | Executive/Owner (Govern); AI Lead (Map, Measure); CISO and DPO (Manage); Platform Administrator (Manage operations) |
| ISO/IEC 42001 \[ISO 2023\] | top management responsibilities, AI risk treatment, monitoring, documentation, internal audit | Executive/Owner; AI Lead; Platform Administrator |
| GDPR \[GDPR 2016\] | controller, processor, DPO, DPIA, automated decision-making (Art. 22), data subject rights | DPO/Privacy Officer; Vendor/Supplier; Executive/Owner |
| Procurement & supplier governance \[Watkins et al. 2021; Reisman et al. 2018\] | due diligence on suppliers, contractual evidence, attestations, expiry | Procurement Officer; Vendor/Supplier |
| Security management (NIST SP 800-53; ISO/IEC 27001\) | system security approval, access control, incident response, resilience | CISO/Security Lead; Platform Administrator |

***Table** 4\. Governance role taxonomy. Roles are accountability positions with different decision rights, not audiences in a communication sense.*

| Role | Decision authority | Liability exposure | Evidence need | Decision action |
| :---- | :---- | :---- | :---- | :---- |
| Executive / Owner | Deployment and escalation | Organisational, financial, board-level | Residual risk, readiness, blockers | Approve, pause, escalate, fund remediation |
| DPO / Privacy Officer | Lawfulness and data-protection review | Data protection and rights-based liability | Personal data, safeguards, DPIA relevance, automated decisioning | Approve processing, request DPIA, block processing |
| CISO / Security Lead | Security approval and resilience | Security, breach, infrastructure risk | Attack surface, exfiltration, adversarial robustness, access controls | Approve, require controls, block production |
| AI Lead / Technical Reviewer | Methodological validity | Model performance and technical reliability | Raw metrics, methods, thresholds, reproducibility, uncertainty | Accept test, rerun test, require mitigation |
| Procurement Officer | Supplier due diligence | Contractual and supplier-risk exposure | Vendor evidence, attestations, missing documents, expiry | Approve supplier, request evidence, delay procurement |
| Vendor / Supplier | Evidence submission and remediation | Customer-facing compliance and contractual risk | Missing artefacts, required evidence, readiness gaps | Submit evidence, remediate, update declaration |
| Platform Administrator | Operational integrity | Workflow, access, and system-state risk | Passport status, entitlement, expiry, evidence freshness | Lock, unlock, expire, notify, archive |

The taxonomy is sector-agnostic at this level; sector-specific extensions (e.g., clinical safety officers, financial model risk managers, public-sector auditors) are anticipated. The architecture supports adding roles by extending the rule pack rather than re-engineering the substrate.

# **5\.  Reference Architecture: System P**

## **5.1  Differentiation from Prior Artefacts**

Several existing artefacts document AI systems for governance purposes. Table 5 situates the evidence passport against them.

***Table** 5\. Evidence passports differentiated from prior documentation artefacts.*

| Artefact | Primary object | Intended audience | Limitation | Distinction of evidence passport |
| :---- | :---- | :---- | :---- | :---- |
| Model card \[Mitchell et al. 2019\] | Model behaviour and intended use | Broad technical / public audience | Usually static, not role-conditioned, not deterministically generated | Role-conditioned views over a versioned substrate; deterministic generation with traceability |
| Datasheet \[Gebru et al. 2021\] | Dataset provenance and composition | Dataset users and downstream model builders | Dataset-centric; does not extend to system-level decision support | System- and evidence-centric; role-conditioned views over assessment findings |
| FactSheet \[Arnold et al. 2019\] | Supplier’s declaration of conformity | Procuring organisation | Static and narrative; not designed to differ across consuming roles | Role-conditioned, rule-generated, versioned |
| System card / capability card | System capabilities and limitations | Broad public / governance audience | Narrative and curated; opaque rule for inclusion/exclusion | Rule pack is inspectable and versioned |
| Audit report \[Raji et al. 2020; Costanza-Chock et al. 2022\] | Audit findings against a scope | Client / regulator | Monolithic; not differentiated by accountable role within the client | Multi-role role-conditioned views from one substrate |
| Assurance case \[Bloomfield & Rushby 2019\] | Structured safety argument | Safety / regulatory actors | Domain-specific; argument-based; not designed for cross-role accountability | Role-conditioned evidentiary adequacy across roles; structural traceability |

The distinguishing property of the evidence passport is structural traceability of role-conditioned interpretation. Model cards, datasheets, FactSheets, system cards, audit reports, and assurance cases are each useful for the purposes they were designed for; none has been designed to provide deterministic, role-conditioned, traceable views over a single immutable substrate for multiple accountable roles simultaneously.

## **5.2  Design Goals**

1. **Common substrate.** All role views derive from one immutable evidence body. Role views may not introduce facts not in the substrate.

2. **Deterministic interpretation.** The mapping from substrate to role view is rule-based and reproducible.

3. **Versioned rules.** Every interpretation rule is identified by version, allowing prior decisions to be reproduced and disputes adjudicated.

4. **Progressive disclosure with traceability.** Role views may foreground or suppress fields; the substrate remains auditable and every surfaced claim links to its source.

5. **Limitation propagation.** Caveats, uncertainty, and scope limits propagate into all role views where they bear on the decision.

6. **No claim without trace.** The system refuses to emit a passport in which any claim does not resolve to a source under a current rule.

7. **Contestability.** Suppressed fields are retrievable on request; rule decisions are challengeable; the rule pack itself is auditable (§8).

## **5.3  Components**

**Common evidence substrate.** The canonical record. Each normalised finding includes type, metric, value, method, threshold, uncertainty, provenance, limitation, regulatory mapping, and context. Findings are content-addressed by hash and timestamped at ingestion. Once admitted, a finding is immutable; corrections are recorded as new findings that supersede prior ones, with the prior record retained.

**Context pack.** The structural variables that condition interpretation: sector, jurisdiction, system purpose, deployment stage, risk class, affected population, data modality, supplier status, regulatory baseline, organisation policy baseline. The context pack is versioned alongside the substrate.

**Versioned interpretation rule pack.** Deterministic rules of the form role × finding\_family × threshold × severity × context\_condition ⟶ { visible\_fields, suppressed\_fields, escalation, action\_label, limitation\_propagation\_set, traceability\_requirement }. Rules are authored by domain experts, reviewed, and version-controlled. A rule-pack version is recorded on every emitted passport.

**Role-conditioned passport views.** Each view includes headline; summary at role-appropriate abstraction; decision relevance; action label drawn from A with rationale, deadline, and responsible role; visible/suppressed fields; regulatory or policy reference; evidence limitations and uncertainty statement; trace links to source findings, rule version, context-pack version, and substrate hash; passport version and expiry.

**Audit substrate.** Every role-conditioned statement is traceable to source finding, method, timestamp, evidence hash, applied rule (with version), context-pack (with version), role profile, and passport version. Traceability is enforced at production time: the system refuses to emit a passport with any untraceable claim.

## **5.4  Progressive Disclosure as Interpretive Safety**

A common objection to role-conditioned views is that they reduce transparency. We reject this framing. Suppressing a field from a role view is not equivalent to removing it from the record. The substrate retains the raw evidence; role views foreground the fields most relevant to the actor’s decision rights and suppress fields likely to distort interpretation outside that decision context. Where a suppressed field is requested—by auditors, regulators, the role-holder, or by contestation channels (§8)—it is retrievable in full under the same trace.

Progressive disclosure is therefore an *interpretive-safety mechanism*: a means of preventing predictable misuse of technical metrics by actors whose decisions require a different evidentiary frame. Its acceptability is conditional on the preservation of audit traceability and contestability, properties the architecture enforces structurally.

# **6\.  Worked Example: One Finding, Four Role Views**

We illustrate accountability-preserving interpretation by showing how a single privacy finding is rendered for four roles. The substrate finding (lightly abbreviated):

{  
  "finding\_family":  "privacy",  
  "metric":          "pii\_entity\_count",  
  "value":           14,  
  "threshold":       0,  
  "severity":        "high",  
  "method":          "NER \+ pattern-based PII scan",  
  "uncertainty":     "medium",  
  "limitation":      "validated only for EN and FR",  
  "context":         "recruitment screening chatbot",  
  "regulatory\_mapping": \["GDPR Art. 22",  
                          "GDPR Art. 35 (DPIA)"\],  
  "provenance":      "sha256:8a91...c4",  
  "timestamp":       "2026-11-04T10:13:22Z"  
}  
The context pack indicates EU jurisdiction, high-risk class (employment/recruitment under EU AI Act Annex III), pre-deployment stage, and adult job-applicants as the affected population.

**DPO view.** *Headline:* Personal-data indicators detected in input corpus; lawfulness and DPIA review required before deployment. *Decision relevance:* Recruitment screening with PII triggers GDPR Art. 22 considerations and likely an Art. 35 DPIA obligation. *Action label:* request\_evidence (DPIA, lawful-basis statement, retention schedule). *Visible fields:* regulatory mapping, affected population, severity, limitation. *Suppressed (retrievable on trace):* raw entity count, NER method details. *Limitations propagated:* scan validated only for EN/FR; coverage gap for other applicant languages. *Trace:* substrate hash 8a91…c4; rule R-PRIV-014 v3; context-pack v2.

**CISO view.** *Headline:* Personal-data exposure surface in recruitment chatbot pipeline; review logging, retention, egress controls, and incident-response posture. *Action label:* approve\_with\_conditions (encryption-at-rest verification; egress filtering on PII channels). *Visible:* severity, attack-surface framing, control families. *Suppressed (retrievable):* regulatory mapping (foregrounded for DPO; here secondary). *Limitations propagated:* language-coverage limitation flagged as residual risk.

**AI Lead view.** *Headline:* PII detector identified 14 entities above threshold 0 using NER \+ pattern-based method; uncertainty medium. *Action label:* rerun\_test on multilingual corpus before deployment widens beyond EN/FR. *Visible:* raw metric, method, threshold, uncertainty, limitation. *Suppressed (retrievable):* none material at this abstraction level.

**Executive view.** *Headline:* Deployment recommended paused pending DPO review and AI-Lead retest. *Decision relevance:* unresolved personal-data exposure in a high-risk system. *Action label:* pause; awaiting DPO and AI Lead findings. *Visible:* severity, decision recommendation, blockers, expected timeline. *Suppressed (retrievable):* raw metric, method, regulatory clause-level mapping.

**What is the same across views.** The substrate hash, the finding identity, the language-coverage limitation, the regulatory context, and the trace structure. No view introduces a fact absent from the substrate; no view drops a material limitation; every claim resolves to a source under a current rule.

# **7\.  Evaluation Framework**

We do not report empirical results. We specify the measurement framework so the construct and architecture can be tested by future work.

## **7.1  Construct Separation**

We separate four constructs to prevent the conflation reviewer-flagged in earlier formulations.

***Table** 6\. Construct separation in the evaluation framework.*

| Construct | Measurement |
| :---- | :---- |
| Objective RCEA | Computed per the seven scoring rules (§3.4) from substrate, rule pack, and rendered view. |
| Perceived RCEA | Candidate eight-item scale (§7.2); psychometric properties to be established. |
| Usability | A standard scale such as SUS short form, treated as a discriminant construct. |
| Decision quality | Accuracy against expert-consensus reference; calibration (Brier, ECE); reasoning quality (coded). |
| Decision confidence | Self-report (1–7). |

Two questions are central: (i) does objective RCEA predict perceived RCEA? (ii) does perceived RCEA mediate the relationship between condition (presentation format) and decision quality, controlling for usability and confidence? Earlier formulations that treated perceived RCEA alone risked relabelling usability or confidence; the four-way construct separation closes that gap.

## **7.2  Candidate Perceived-RCEA Scale**

We propose an eight-item candidate scale, rated 1–7 (strongly disagree–strongly agree). The scale is candidate; psychometric validation is a precondition to using it for inferential claims.

1. The information provided was sufficient for my role-specific decision.

2. The evidence highlighted what was most relevant to my responsibility.

3. The evidence was presented at the right level of technical detail for my role.

4. I understood what action I was expected to take.

5. The limitations of the evidence were clear.

6. I could identify which findings supported the recommendation.

7. I could trace the recommendation back to the underlying evidence.

8. I felt confident in my decision without relying on unsupported assumptions.

**Validation procedure.** Reliability via Cronbach’s α and McDonald’s ω (target ≥ 0.8); exploratory factor analysis on a pilot subsample; confirmatory factor analysis if sample size permits; convergent validity against decision confidence; predictive validity against decision accuracy; *discriminant* validity against SUS short form. Items overlapping with usability or confidence are candidates for revision after pilot results.

## **7.3  Evaluation Design Specifications**

We specify three evaluation components. The intent is to make the construct testable; we do not commit to specific recruitment numbers or analyses prior to ethics approval and preregistration.

**Component 1: Elicitation of role-specific evidence needs.** A structured Delphi-style elicitation across the seven roles in Table 4, with a target of at least three experts per role (minimum n \= 21; preferred range n \= 28–35 to support per-role weight estimation). The output is the role × field importance matrix and, after pre-specified aggregation onto the seven RCEA dimensions, the empirical role-weight matrix {wₖˣ}. Inter-rater agreement (Krippendorff’s α) is reported per role; pairwise role divergence is computed using Jensen–Shannon divergence on normalised field-importance distributions. The seven-role taxonomy may be collapsed for elicitation if per-role recruitment falls short, in which case the seven-role architectural taxonomy and the elicited weighting taxonomy are reported separately.

**Component 2: Architecture-level evaluation.** For a corpus of assessment records (a mix of real, ethically-cleared records and synthetic stress-tests covering privacy, fairness, robustness, explainability, security, documentation, and supplier evidence), the architecture is evaluated against: (a) per-pair field-exposure distance; (b) alignment between the field-exposure profile and the elicited evidence-need profile (Spearman ρ, pre-specified threshold ρ ≥ 0.6 per role for acceptance); (c) traceability completeness (AT \= 1 is the system-correctness requirement, not a statistical hypothesis); (d) limitation propagation rate. Semantic distance between rendered text (multiple sentence encoders for robustness) is reported only as a descriptive measurement and is *not* treated as evidence of adequacy.

**Component 3: Practitioner experiment.** A factorial design with three conditions to avoid a strawman baseline: *Flat* (raw metric table), *Conventional* (a model-card-style or audit-report-style document of comparable length and care to current practice), and *Passport* (role-conditioned evidence passport). Within-subjects vignettes drawn from Component 2\. Stratification by professional role. Primary outcome: decision accuracy against expert-consensus reference decisions, not “ground truth”. Power is determined by simulation under pre-specified assumptions about base accuracy, intra-participant correlation, between-vignette variance, and condition effect; assumptions and simulation script are part of the preregistration when this component is run.

**Statistical approach.** For accuracy, a generalised linear mixed-effects model with participant and vignette random intercepts, condition and role main effects, and the condition × role interaction; analogous models for secondary outcomes with appropriate link functions. For the mediation question, contemporary causal-mediation methods \[Imai et al. 2010; VanderWeele 2015\] are appropriate, with sensitivity analyses for sequential-ignorability assumptions; we explicitly do not rely on Baron–Kenny step-wise testing. If sample size precludes confirmatory mediation, indirect-effect estimates are reported as exploratory with bootstrapped confidence intervals.

## **7.4  What Counts as Falsification**

* If Component 1 finds no systematic between-role divergence in evidence needs (median pairwise Jensen–Shannon divergence below a pre-specified threshold), the role-relative claim of the construct is not supported and the role-weighting matrix is not derivable as proposed.

* If Component 2 finds AT \< 1 on any record, the architecture is defective as specified and is revised before further claims.

* If Component 3 finds no positive effect on decision accuracy of the Passport condition relative to the Conventional condition (not merely the Flat condition), the practical claim is not supported.

* If a condition effect on accuracy is not mediated by perceived RCEA after controlling for usability and confidence, the causal model is revised.

* If benefits are confined to a single role, generalisability claims are contextualised.

# **8\.  Contestability and Rule-Pack Governance**

Progressive disclosure concentrates interpretive authority in whoever authors the rule pack. The architecture mitigates this risk only if specific contestability mechanisms are present and inspectable.

**Right to raw evidence.** Any role-holder may request the substrate fields suppressed from their default view; requests are logged and granted under documented policy.

**Auditor inspection.** Auditors and regulators have access to suppressed fields, to the rule pack, and to the rule version applied at issuance.

**Versioned, inspectable rule pack.** The rule pack is itself an artefact: every rule has a version, an author, a review record, and a change log. Rule changes are diff-able. Prior passports remain reproducible under the rule version they were issued against.

**Challenge of action labels.** A role-holder may challenge an action label assigned by a rule. Challenges produce a contestation record linked to the passport and the rule. Rules whose challenges exceed a documented threshold are flagged for review.

**Logged suppression decisions.** Each suppressed field is logged with the rule that suppressed it, the context-pack version, and the suppression rationale.

**Audit of progressive-disclosure policy.** The progressive-disclosure policy is itself subject to periodic audit, distinct from audit of any single passport, with results published to the organisation.

**Governance of the rule pack.** Rules encode interpretive judgments; the authority to author or change them is itself a governance question. We propose a separation of duties: rule authoring (domain experts), rule review (a cross-role committee that includes DPO, security, AI lead, and an external reviewer), rule promotion to production (the executive owner), and rule audit (independent of authoring). This separation does not make the rule pack neutral; it makes its non-neutrality inspectable and challengeable.

# **9\.  Discussion**

**Evidence transparency is not enough.** Metric visibility can be insufficient or misleading when evidence is not conditioned on the decision rights and responsibilities of the actor using it. Transparency without adequacy can produce a documented record of decisions that no actor was positioned to make well.

**Evidentiary adequacy is role-conditioned.** The main theoretical contribution is to treat adequacy as a relational property: evidence is adequate *for a role, for a decision, in a context*. Adequacy becomes measurable through role-conditioned scoring rather than through global readability or completeness checks; assurance pipelines and regulator-facing documentation can be designed against an explicit adequacy target.

**Accountability-preserving interpretation.** Role-specific views need not fragment accountability if they are generated from one substrate through versioned deterministic rules with full traceability. The contribution is the interpretation layer, not the rendering.

**Progressive disclosure as interpretive safety, conditional on contestability.** Selective foregrounding is not a reduction of transparency when raw evidence remains auditable and contestability mechanisms are present (§8). The architecture supplies the structural condition under which progressive disclosure is defensible.

**Implications.** Assurance pipelines and AI audit platforms can be evaluated for whether they produce role-conditioned adequate evidence rather than only complete evidence. Procurement review processes can require structured supplier-side passports as a precondition for engagement. EU AI Act technical documentation requirements can be operationalised through role-conditioned passports satisfying provider, deployer, and regulator-facing needs from one substrate.

# **10\.  Threats to Validity and Adverse Impacts**

## **10.1  Threats to Construct Validity**

The seven-dimension decomposition is theoretically motivated. It may not survive empirical factor analysis: dimensions may collapse (e.g., decision actionability and audit traceability could load together), split, or fail to discriminate from adjacent constructs (interpretive fit versus usability is the most exposed). The candidate perceived-RCEA scale risks measuring usability or confidence rather than adequacy; this is exactly why the framework separates objective RCEA, perceived RCEA, usability, and confidence as distinct constructs.

## **10.2  Threats to Internal Validity**

Vignette-based experiments do not reproduce organisational stakes (career risk, regulatory exposure, supplier relationships). Effects observed in controlled studies may overstate effects in deployment. Expert-consensus reference decisions are not objective truth; disagreement among panellists reflects genuine ambiguity in the field and is reported transparently.

## **10.3  Threats to External Validity**

The role taxonomy is sector-agnostic; clinical, financial, and public-sector deployments will need extensions. Regulatory mappings are jurisdiction-specific; rules encoded for one jurisdiction do not transfer without revision. Deterministic rule packs require ongoing maintenance.

## **10.4  Adverse Impacts and Their Mitigations**

**Concentration of interpretive authority.** A rule pack that determines what each role sees is a locus of power. Concentration risk is mitigated by inspectable, versioned rules; cross-role review of rule changes; logged suppression decisions; and contestability (§8).

**Manipulation through selective suppression.** A bad-faith rule author could suppress fields strategically. Mitigations: external audit of the rule pack; statistical monitoring of suppression patterns; mandatory propagation of material limitations.

**False sense of accountability.** A traceable passport may give a misleading impression of due diligence even when the underlying assessment is shallow. Mitigation: the substrate quality (epistemic warrant subscore) is reported on every passport; assurance pipelines must publish substrate audit results, not only passports.

**Substitution for legal judgment.** Passports must not be presented as certifications or substitutes for legal review. The architecture supports documentation and interpretation; it does not determine legal compliance.

**Privacy and labour effects.** Logging of contestation behaviour, suppression requests, and decisions could expose role-holders to monitoring or retaliation. Mitigation: contestation logs are accessible to internal audit and external regulators, but not used in individual performance review.

# **11\.  Limitations**

**No empirical results.** This paper presents construct, architecture, and evaluation framework; we do not report empirical findings. The construct is testable; the architecture is implementable; whether the construct improves accountable decisions in practice is an open empirical question.

**Construct iterativity.** The seven-dimension decomposition is theoretically motivated and will be refined as empirical work proceeds; where dimensions collapse or split, the construct is revised and the revision documented.

**Role-taxonomy granularity.** The seven roles map onto common organisational structures but coarsen real role distributions; combined roles (e.g., DPO who is also security lead) and split roles (separate AI-ethics and AI-engineering leads) require local mapping.

**Rule-pack maintenance cost.** Deterministic rules require maintenance as regulations, methods, and organisational policies evolve. This cost is the price of audit-grade traceability.

# **12\.  Ethics, Reproducibility, and Adverse Impacts Statement**

This paper introduces no participant data; the worked example is synthetic and illustrative. Empirical components specified in §7 will require IRB or ethics review at the lead institution prior to data collection. We commit to releasing, upon publication or thereafter: the construct’s scoring rules in formal form; an open reference implementation of the substrate-to-view transformation; the candidate scale; the qualitative coding scheme; and pre-registration documents for empirical components, where applicable. Adverse impacts of the architecture, and their mitigations, are addressed in §10.

# **13\.  Conclusion**

AI accountability cannot be achieved by producing more evidence alone. It requires evidence infrastructures that make shared evidence role-conditionally adequate for accountable decisions while preserving a common audit substrate and structural contestability. We have introduced role-conditioned evidentiary adequacy as a formal construct with seven computable subscores, presented a reference architecture (System P) that operationalises the construct through a versioned interpretation rule pack and structurally enforced traceability, and specified an evaluation framework that separates objective RCEA, perceived RCEA, usability, and decision quality. Whether the construct improves accountable decisions in practice is an empirical question; we have specified the conditions under which the answer can be yes, no, or qualified.

# **Generative AI Usage Statement**

The authors used generative AI tools for language editing and structural drafting assistance. All scientific claims, formal definitions, citations, analyses, and final text were reviewed and verified by the authors. No generative AI was used to fabricate empirical results; this paper reports none.

# **References**

Arnold, M., Bellamy, R.K.E., Hind, M., Houde, S., Mehta, S., Mojsilovic, A., Nair, R., Ramamurthy, K.N., Olteanu, A., Piorkowski, D., Reimer, D., Richards, J., Tsay, J., Varshney, K.R. (2019). FactSheets: Increasing trust in AI services through supplier’s declarations of conformity. IBM Journal of Research and Development, 63(4/5), 6:1–6:13.

Arrieta, A.B., Díaz-Rodríguez, N., Del Ser, J., et al. (2020). Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. Information Fusion, 58, 82–115.

Birhane, A., Steed, R., Ojewale, V., Vecchione, B., Raji, I.D. (2024). AI auditing: The broken bus on the road to AI accountability. In Proc. IEEE Conference on Secure and Trustworthy Machine Learning (SaTML).

Bloomfield, R., Rushby, J. (2019). Assurance 2.0: A manifesto. arXiv:1906.00608.

Bowker, G.C., Star, S.L. (1999). Sorting Things Out: Classification and Its Consequences. MIT Press, Cambridge, MA.

Brundage, M., Avin, S., Wang, J., et al. (2020). Toward trustworthy AI development: Mechanisms for supporting verifiable claims. arXiv:2004.07213.

Costanza-Chock, S., Raji, I.D., Buolamwini, J. (2022). Who audits the auditors? Recommendations from a field scan of the algorithmic auditing ecosystem. In Proc. FAccT ’22, pp. 1571–1583. ACM.

Edwards, L., Veale, M. (2017). Slave to the algorithm? Why a ‘right to an explanation’ is probably not the remedy you are looking for. Duke Law & Technology Review, 16, 18–84.

European Parliament and Council. (2016). Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data (General Data Protection Regulation). OJ L 119/1.

European Parliament and Council. (2024). Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act). Official Journal of the European Union, L series.

Fischhoff, B. (1995). Risk perception and communication unplugged: Twenty years of process. Risk Analysis, 15(2), 137–145.

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Wallach, H., Daumé III, H., Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, 64(12), 86–92.

Gigerenzer, G. (2002). Calculated Risks: How to Know When Numbers Deceive You. Simon & Schuster, New York.

Imai, K., Keele, L., Yamamoto, T. (2010). Identification, inference, and sensitivity analysis for causal mediation effects. Statistical Science, 25(1), 51–71.

ISO/IEC. (2023). ISO/IEC 42001:2023 Information technology — Artificial intelligence — Management system. International Organization for Standardization, Geneva.

Metcalf, J., Moss, E., Watkins, E.A., Singh, R., Elish, M.C. (2021). Algorithmic impact assessments and accountability: The co-construction of impacts. In Proc. FAccT ’21, pp. 735–746. ACM.

Miller, T. (2019). Explanation in artificial intelligence: Insights from the social sciences. Artificial Intelligence, 267, 1–38.

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D., Gebru, T. (2019). Model cards for model reporting. In Proc. FAT\* ’19, pp. 220–229. ACM.

Mökander, J., Schuett, J., Kirk, H.R., Floridi, L. (2023). Auditing large language models: A three-layered approach. AI and Ethics, 4, 1085–1115.

Morgan, M.G., Fischhoff, B., Bostrom, A., Atman, C.J. (2002). Risk Communication: A Mental Models Approach. Cambridge University Press.

National Institute of Standards and Technology. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1.

Raji, I.D., Smart, A., White, R.N., Mitchell, M., Gebru, T., Hutchinson, B., Smith-Loud, J., Theron, D., Barnes, P. (2020). Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. In Proc. FAT\* ’20, pp. 33–44. ACM.

Reisman, D., Schultz, J., Crawford, K., Whittaker, M. (2018). Algorithmic impact assessments: A practical framework for public agency accountability. AI Now Institute Report.

Schmidt, K., Bannon, L. (1992). Taking CSCW seriously: Supporting articulation work. Computer Supported Cooperative Work, 1(1), 7–40.

Selbst, A.D., Barocas, S. (2018). The intuitive appeal of explainable machines. Fordham Law Review, 87, 1085–1139.

Star, S.L., Griesemer, J.R. (1989). Institutional ecology, ‘translations’ and boundary objects: Amateurs and professionals in Berkeley’s Museum of Vertebrate Zoology, 1907–39. Social Studies of Science, 19(3), 387–420.

Strauss, A. (1985). Work and the division of labor. The Sociological Quarterly, 26(1), 1–19.

Suchman, L. (1996). Supporting articulation work. In R. Kling (Ed.), Computerization and Controversy (2nd ed., pp. 407–423). Academic Press, San Diego.

VanderWeele, T.J. (2015). Explanation in Causal Inference: Methods for Mediation and Interaction. Oxford University Press.

Veale, M., Borgesius, F.Z. (2021). Demystifying the Draft EU Artificial Intelligence Act. Computer Law Review International, 22(4), 97–112.

Wachter, S., Mittelstadt, B., Floridi, L. (2017). Why a right to explanation of automated decision-making does not exist in the General Data Protection Regulation. International Data Privacy Law, 7(2), 76–99.

Watkins, E.A., Moss, E., Metcalf, J., Singh, R., Elish, M.C. (2021). Governing algorithmic systems with impact assessments: Six observations. In Proc. AIES ’21, pp. 1010–1022. ACM.