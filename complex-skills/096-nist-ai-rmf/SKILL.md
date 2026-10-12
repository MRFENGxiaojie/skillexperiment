---
name: nist-ai-rmf
description: AI risk assessment using NIST AI RMF 1.0 framework. Evaluate AI systems across 4 core functions (GOVERN, MAP, MEASURE, MANAGE) for trustworthy and responsible AI deployment. Use when the user asks to assess risks of an AI system before deployment, establish AI governance structures, evaluate AI trustworthiness, prepare for regulatory compliance (EU AI Act), or review third-party AI tools and vendors.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# NIST AI Risk Management Framework (AI RMF 1.0)

This skill enables AI agents to perform a comprehensive **AI risk assessment** using the **NIST AI Risk Management Framework (AI RMF 1.0)**, published January 2023 by the National Institute of Standards and Technology.

The AI RMF is a voluntary, technology- and sector-agnostic framework designed to help organizations manage risks associated with AI systems throughout their lifecycle. It promotes trustworthy AI development by addressing risks that affect individuals, organizations, and society.

Use this skill to identify, assess, and manage AI risks; establish governance structures; ensure trustworthy AI characteristics; and align with international AI risk management best practices.

Combine with "ISO 42001 AI Governance" for comprehensive compliance coverage or "OWASP LLM Top 10" for security-focused assessment.


## When to Use This Skill

Invoke this skill when:
- Assessing risks of AI systems before deployment
- Establishing AI governance and accountability structures
- Evaluating trustworthiness of AI products and services
- Preparing for regulatory compliance (EU AI Act, state AI laws)
- Conducting periodic AI risk reviews
- Evaluating third-party AI tools and vendors
- Building organizational AI risk management programs
- Documenting AI system risks for stakeholders


## Inputs Required

When executing this assessment, gather:

- **ai_system_description**: Description of the AI system (purpose, capabilities, deployment context, users, data sources) [REQUIRED]
- **system_lifecycle_stage**: Current stage (design, development, deployment, monitoring, decommissioning) [OPTIONAL, defaults to deployment]
- **organization_context**: Organization size, industry, risk tolerance, regulatory environment [OPTIONAL]
- **deployment_domain**: Sector and setting, including whether the system supports critical infrastructure [OPTIONAL]
- **existing_controls**: Current risk management processes or controls in place [OPTIONAL]
- **specific_concerns**: Known risks, incidents, or areas of focus [OPTIONAL]
- **stakeholders**: Key stakeholders and affected communities [OPTIONAL]


## Trustworthy AI Characteristics

The AI RMF identifies seven characteristics of trustworthy AI that serve as evaluation criteria across all functions:

1. **Valid and Reliable**: System performs as intended with consistent results
2. **Safe**: System does not endanger human life, health, property, or the environment
3. **Secure and Resilient**: System withstands adverse events and recovers gracefully
4. **Accountable and Transparent**: Information about the system is available to stakeholders
5. **Explainable and Interpretable**: Mechanisms and outputs can be understood
6. **Privacy-Enhanced**: Human autonomy and data rights are protected
7. **Fair with Harmful Bias Managed**: System does not produce discriminatory outcomes

---


## The 4 Core Functions

The AI RMF Core is composed of four functions, each broken into categories and subcategories:

### GOVERN Function

Establishes organizational policies, processes, and accountability for AI risk management. GOVERN is cross-cutting and applies across all other functions.

#### GOVERN 1: Policies and Processes
*Policies, processes, procedures, and practices across the organization related to the mapping, measuring, and managing of AI risks are in place, transparent, and implemented effectively.*

- **GOVERN 1.1**: Legal and regulatory requirements involving AI are understood, managed, and documented
- **GOVERN 1.2**: Trustworthy AI characteristics integrated into organizational policies, processes, and practices
- **GOVERN 1.3**: AI risk management processes and outcomes established through transparent policies, procedures, and controls
- **GOVERN 1.4**: Organizational risk tolerance evaluated and reflected in AI risk management processes and practices
- **GOVERN 1.5**: Ongoing monitoring and periodic review of risk management process with clear roles and responsibilities
- **GOVERN 1.6**: Mechanisms to inventory AI systems resourced by organizational risk priorities
- **GOVERN 1.7**: Processes for decommissioning and phasing out AI systems safely

#### GOVERN 2: Accountability Structures
*Accountability structures ensure appropriate teams and individuals are empowered, responsible, and trained for AI risk management.*

- **GOVERN 2.1**: Roles, responsibilities, and communication lines documented and clear
- **GOVERN 2.2**: Personnel receive AI risk management training
- **GOVERN 2.3**: Executive leadership takes responsibility for AI decisions

#### GOVERN 3: Workforce Diversity and Inclusion
*Workforce diversity, equity, inclusion, and accessibility processes are prioritized in AI risk management.*

- **GOVERN 3.1**: Decision-making informed by diverse team (demographics, disciplines, expertise)
- **GOVERN 3.2**: Policies define roles for human-AI configurations and oversight

#### GOVERN 4: Risk Culture
*Organizational teams are committed to a culture that considers and communicates AI risk.*

- **GOVERN 4.1**: Policies foster critical thinking and safety-first mindset
- **GOVERN 4.2**: Teams document and communicate risks and impacts broadly
- **GOVERN 4.3**: Practices enable AI testing, incident identification, and information sharing

#### GOVERN 5: Stakeholder Engagement
*Processes are in place for robust engagement with relevant AI actors.*

- **GOVERN 5.1**: Policies collect, consider, and integrate external feedback on impacts
- **GOVERN 5.2**: Mechanisms regularly incorporate adjudicated feedback into system design

#### GOVERN 6: Third-Party Risk
*Policies and procedures address AI risks from third-party software, data, and supply chain.*

- **GOVERN 6.1**: Policies address risks from third-party entities including IP infringement
- **GOVERN 6.2**: Contingency processes handle failures in high-risk third-party systems

---

### MAP Function

Identifies and contextualizes AI system risks within the operational environment.

#### MAP 1: Context Established
*Context is established and understood.*

- **MAP 1.1**: Intended purposes, beneficial uses, laws, norms, and deployment settings documented
- **MAP 1.2**: Interdisciplinary AI actors with demographic diversity participate and documented
- **MAP 1.3**: Organization's mission and goals for AI technology understood and documented
- **MAP 1.4**: Business value or context clearly defined or re-evaluated
- **MAP 1.5**: Organizational risk tolerances determined and documented
- **MAP 1.6**: System requirements elicited with socio-technical considerations

#### MAP 2: System Categorization
*Categorization of the AI system is performed.*

- **MAP 2.1**: Specific tasks and methods defined (classifiers, generative models, recommenders)
- **MAP 2.2**: System knowledge limits and human oversight documented
- **MAP 2.3**: Scientific integrity and Test, Evaluation, Verification, and Validation (TEVV) considerations identified

#### MAP 3: Capabilities and Costs
*AI capabilities, targeted usage, goals, expected benefits, and costs are understood.*

- **MAP 3.1**: Potential benefits of intended functionality examined and documented
- **MAP 3.2**: Potential costs (monetary and non-monetary) from AI errors documented
- **MAP 3.3**: Targeted application scope specified based on capability
- **MAP 3.4**: Operator and practitioner proficiency assessed
- **MAP 3.5**: Human oversight processes defined and documented

#### MAP 4: Component Risks
*Risks and benefits are mapped for all components including third-party.*

- **MAP 4.1**: Approaches for mapping technology and legal risks documented
- **MAP 4.2**: Internal risk controls for components identified and documented

#### MAP 5: Impact Characterization
*Impacts to individuals, groups, communities, organizations, and society are characterized.*

- **MAP 5.1**: Likelihood and magnitude of impacts (beneficial and harmful) documented
- **MAP 5.2**: Practices for regular engagement with relevant AI actors documented

---

### MEASURE Function

Employs tools, techniques, and methodologies to assess, benchmark, and monitor AI risk.

#### MEASURE 1: Methods and Metrics
*Appropriate methods and metrics are identified and applied.*

- **MEASURE 1.1**: Approaches and metrics selected starting with most significant risks
- **MEASURE 1.2**: Appropriateness of metrics regularly assessed and updated
- **MEASURE 1.3**: Internal experts or independent assessors involved in assessments

#### MEASURE 2: Trustworthiness Evaluation
*AI systems are evaluated for trustworthy characteristics.*

- **MEASURE 2.1**: Test sets, metrics, and tool details documented during TEVV
- **MEASURE 2.2**: Evaluations with human subjects meet requirements and represent relevant populations
- **MEASURE 2.3**: Performance or assurance criteria measured and demonstrated
- **MEASURE 2.4**: Functionality and behavior monitored in production
- **MEASURE 2.5**: System demonstrated valid and reliable with generalizability limitations documented
- **MEASURE 2.6**: System regularly evaluated for safety risks with residual risk within tolerance
- **MEASURE 2.7**: Security and resilience evaluated and documented
- **MEASURE 2.8**: Transparency and accountability risks examined
- **MEASURE 2.9**: AI model explained, validated, and output interpreted within context
- **MEASURE 2.10**: Privacy risk examined and documented
- **MEASURE 2.11**: Fairness and bias evaluated with results documented
- **MEASURE 2.12**: Environmental impact and sustainability assessed
- **MEASURE 2.13**: Effectiveness of TEVV metrics evaluated

#### MEASURE 3: Risk Tracking
*Mechanisms for tracking identified AI risks over time are in place.*

- **MEASURE 3.1**: Approaches track existing, unanticipated, and emergent risks
- **MEASURE 3.2**: Risk tracking considered for settings where assessment is difficult
- **MEASURE 3.3**: Feedback processes for end users to report problems and appeal outcomes

#### MEASURE 4: Measurement Efficacy
*Feedback about efficacy of measurement is gathered and assessed.*

- **MEASURE 4.1**: Measurement approaches informed by domain experts and end users
- **MEASURE 4.2**: Results validated for consistency with intended performance
- **MEASURE 4.3**: Measurable performance improvements or declines identified

---

### MANAGE Function

Allocates resources to mapped and measured risks on a regular basis.

#### MANAGE 1: Risk Prioritization
*AI risks based on assessments are prioritized, responded to, and managed.*

- **MANAGE 1.1**: Determination made whether AI system achieves intended purposes
- **MANAGE 1.2**: Treatment of risks prioritized based on impact, likelihood, and resources
- **MANAGE 1.3**: Responses to high-priority risks developed (mitigate, transfer, avoid, accept)
- **MANAGE 1.4**: Negative residual risks documented for downstream users

#### MANAGE 2: Benefit Maximization
*Strategies to maximize AI benefits and minimize negative impacts are planned and documented.*

- **MANAGE 2.1**: Resources to manage risks considered alongside non-AI alternatives
- **MANAGE 2.2**: Mechanisms to sustain value of deployed systems
- **MANAGE 2.3**: Procedures to respond to and recover from unknown risks
- **MANAGE 2.4**: Mechanisms to supersede, disengage, or deactivate inconsistent systems

#### MANAGE 3: Third-Party Risk Management
*AI risks and benefits from third-party entities are managed.*

- **MANAGE 3.1**: Third-party risks regularly monitored with controls applied
- **MANAGE 3.2**: Pre-trained models monitored as part of regular maintenance

#### MANAGE 4: Communication and Monitoring
*Risk treatments and communication plans are documented and monitored.*

- **MANAGE 4.1**: Post-deployment monitoring plans with user input, appeal, and decommissioning mechanisms
- **MANAGE 4.2**: Continual improvement activities integrated into updates
- **MANAGE 4.3**: Incidents communicated to relevant actors; tracking and recovery documented

---


## Assessment Procedure

Follow these steps systematically:

The checklist below is a curated sample of the 72 AI RMF subcategories; assess the remaining subcategories where relevant to the system's risk profile (see the framework sections above), and note any subcategories you determine not applicable.

### Step 1: System Understanding (15 minutes)

1. **Review AI system:**
   - Analyze `ai_system_description` and `system_lifecycle_stage`
   - Identify system type (classifier, generative, recommender, autonomous, etc.)
   - Document data sources, models, and deployment environment
   - Note stakeholders and affected communities

2. **Understand context:**
   - Review `organization_context` and regulatory environment
   - Identify applicable laws and standards
   - Note risk tolerance and existing controls

3. **Define scope:**
   - Determine which functions and categories to assess
   - Prioritize based on lifecycle stage and concerns

4. **Apply system-type conditions:**
   - If the system is generative (LLM, image/audio/video generation): additionally evaluate the items in `references/generative-ai-considerations.md` and add a Generative AI Considerations section to the report.
   - If the system supports critical infrastructure: additionally evaluate `references/critical-infrastructure-note.md`.

5. **Handle information gaps:**
   - If `ai_system_description` is missing or insufficient: proceed with explicitly stated assumptions first, and mark every assumption in the report; ask only if the specifics are genuinely unobtainable. (Assumptions field in the Executive Summary).

### Step 2: GOVERN Assessment (20 minutes)

Evaluate organizational governance:

- [ ] **G1**: Are AI risk policies in place and transparent?
- [ ] **G1.1**: Legal/regulatory requirements understood and documented?
- [ ] **G1.2**: Trustworthy AI characteristics in organizational policies?
- [ ] **G1.5**: Monitoring and review processes planned?
- [ ] **G1.6**: AI system inventory maintained?
- [ ] **G2**: Accountability structures defined?
- [ ] **G2.1**: Roles and responsibilities clear?
- [ ] **G2.3**: Executive leadership accountable?
- [ ] **G3.1**: Diverse team informing decisions?
- [ ] **G4**: Risk culture fostered?
- [ ] **G5**: Stakeholder engagement processes in place?
- [ ] **G6**: Third-party risks addressed?

### Step 3: MAP Assessment (20 minutes)

Evaluate risk identification and context:

- [ ] **M1.1**: Intended purposes and deployment context documented?
- [ ] **M1.5**: Risk tolerances determined?
- [ ] **M2.1**: AI tasks and methods defined?
- [ ] **M2.2**: Knowledge limits and human oversight documented?
- [ ] **M3.1**: Benefits examined and documented?
- [ ] **M3.2**: Costs from AI errors documented?
- [ ] **M3.5**: Human oversight processes defined?
- [ ] **M4.1**: Component risks mapped?
- [ ] **M5.1**: Impact likelihood and magnitude documented?

### Step 4: MEASURE Assessment (25 minutes)

Evaluate risk measurement and monitoring:

- [ ] **ME1.1**: Risk metrics selected and applied?
- [ ] **ME2.3**: Performance criteria measured?
- [ ] **ME2.4**: Production behavior monitored?
- [ ] **ME2.5**: Validity and reliability demonstrated?
- [ ] **ME2.6**: Safety risks evaluated?
- [ ] **ME2.7**: Security and resilience evaluated?
- [ ] **ME2.8**: Transparency and accountability risks examined?
- [ ] **ME2.9**: Model explainability documented?
- [ ] **ME2.10**: Privacy risk examined?
- [ ] **ME2.11**: Fairness and bias evaluated?
- [ ] **ME3.1**: Risk tracking in place?
- [ ] **ME3.3**: User feedback mechanisms established?

### Step 5: MANAGE Assessment (20 minutes)

Evaluate risk response and treatment:

- [ ] **MA1.1**: System achieves intended purposes?
- [ ] **MA1.2**: Risk treatment prioritized?
- [ ] **MA1.3**: Response plans for high-priority risks?
- [ ] **MA2.1**: Non-AI alternatives considered?
- [ ] **MA2.3**: Unknown risk response procedures?
- [ ] **MA2.4**: Deactivation mechanisms in place?
- [ ] **MA3.1**: Third-party risks monitored?
- [ ] **MA4.1**: Post-deployment monitoring implemented?
- [ ] **MA4.3**: Incident communication and recovery documented?

### Step 6: Report Generation (20 minutes)

Compile assessment findings with ratings and recommendations.

---


## Output Format

Generate a comprehensive NIST AI RMF assessment report:

```markdown
# NIST AI RMF Assessment Report

**AI System**: [Name/Description]
**Organization**: [Name]
**Date**: [Date]
**Lifecycle Stage**: [Design/Development/Deployment/Monitoring]
**Evaluator**: [AI Agent or Human]
**AI RMF Version**: 1.0 (January 2023)
**Assumptions**: [Explicitly stated assumptions used; "none" if none]

---


## Executive Summary

### Overall Risk Profile: [Low / Medium / High / Critical]

**System Type**: [Classifier / Generative / Recommender / Autonomous / Other]
**Deployment Context**: [Internal / Customer-facing / Public / Critical infrastructure]
**Regulatory Applicability**: [EU AI Act risk level, state laws, sector regulations]

### Key Findings
- **Total Issues**: [X]
  - Critical: [X] (immediate action required)
  - High: [X] (action required within 30 days)
  - Medium: [X] (action required within 90 days)
  - Low: [X] (improvements recommended)

### Trustworthiness Summary
- Valid & Reliable: status is [Status], rated [1-5] on a 1-5 scale.
- Safe: status is [Status], rated [1-5] on a 1-5 scale.
- Secure & Resilient: status is [Status], rated [1-5] on a 1-5 scale.
- Accountable & Transparent: status is [Status], rated [1-5] on a 1-5 scale.
- Explainable & Interpretable: status is [Status], rated [1-5] on a 1-5 scale.
- Privacy-Enhanced: status is [Status], rated [1-5] on a 1-5 scale.
- Fair (Bias Managed): status is [Status], rated [1-5] on a 1-5 scale.

---


## GOVERN Function Assessment

### GOVERN 1: Policies and Processes
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Finding 1 with evidence]
- [Finding 2 with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

### GOVERN 2: Accountability Structures
**Rating**: [Not Implemented / Partial / Substantial / Full]

[Continue for all GOVERN categories...]

---


## MAP Function Assessment

### MAP 1: Context Established
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MAP categories...]

---


## MEASURE Function Assessment

### MEASURE 1: Methods and Metrics
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MEASURE categories...]

---


## MANAGE Function Assessment

### MANAGE 1: Risk Prioritization
**Rating**: [Not Implemented / Partial / Substantial / Full]

**Findings:**
- [Findings with evidence]

**Gaps:**
- [ ] [Gap description]

**Recommendations:**
- [Recommendation with priority]

[Continue for all MANAGE categories...]

---


### Rating Aggregation

- **Subcategory → category → function**: aggregate upward by taking the lowest rating of the assessed items at each level (subcategory → category → function).
- **Function → overall risk profile**: if any function rates below Substantial, the overall profile is High or Critical; if all functions rate Substantial or Full and residual risks are tracked, rate Medium or lower. Document the reasoning in the Executive Summary.
- **Risk Register priority**: map Likelihood × Impact to Priority —

- Likelihood × Impact of H×H, H×M, M×H, or L×H is assigned priority P0 (immediate).
- Likelihood × Impact of H×L, M×M, or L×M is assigned priority P1 (30-90 days).
- Likelihood × Impact of L×L or M×L is assigned priority P2/P3 (as tracked).

Priorities are a reproducible heuristic, not a substitute for judgment — adjust with documented rationale.

---

## Risk Register

- R1: risk description is [Description], function is [G/M/ME/MA], likelihood is [L/M/H], impact is [L/M/H], priority is [P0-P3], and mitigation is [Strategy].
- R2: risk description is [Description], function is [G/M/ME/MA], likelihood is [L/M/H], impact is [L/M/H], priority is [P0-P3], and mitigation is [Strategy].

---


## Remediation Roadmap

### Phase 1: Critical (0-30 days)
1. [Action item with owner and deadline]
2. [Action item with owner and deadline]

### Phase 2: High Priority (30-90 days)
1. [Action item with owner and deadline]

### Phase 3: Medium Priority (90-180 days)
1. [Action item with owner and deadline]

### Phase 4: Continuous Improvement
1. [Ongoing practices]

---


## Compliance Alignment

### Regulatory Mapping
- EU AI Act maps to AI RMF functions GOVERN, MAP, MEASURE; status is [Status].
- NIST CSF 2.0 maps to AI RMF functions GOVERN, MANAGE; status is [Status].
- State AI Laws maps to AI RMF functions GOVERN, MAP; status is [Status].
- Sector Regulations maps to [Relevant functions]; status is [Status].

---


## Scope / Limitations

This skill provides AI risk assessment using the NIST AI RMF 1.0 framework. The RMF is voluntary and risk-based — not all subcategories apply to every system. Tailor the assessment depth, scope, and subcategory selection to the specific AI system under review, its use context, and the organization's risk appetite.

This skill does **not** provide legal advice or formal regulatory compliance certification (EU AI Act, state AI laws, sector regulations). The regulatory mapping in the output template is a starting point for gap analysis, not a legal opinion. It is not a substitute for a qualified compliance auditor, a third-party penetration test, or an organizational governance board review.

Do not use this skill for: non-AI systems (traditional rule-based software), purely hypothetical risk assessments with no real system context, or environments where the AI system's architecture and data flows are completely unknown (the assessment requires at least a basic system description).

## Reference Files

- **Best Practices**: see [references/best-practices.md](references/best-practices.md)
- **Critical Infrastructure Note**: see [references/critical-infrastructure-note.md](references/critical-infrastructure-note.md)
- **Generative AI Considerations**: see [references/generative-ai-considerations.md](references/generative-ai-considerations.md)
- **Next Steps**: see [references/next-steps.md](references/next-steps.md)
- **Resources**: see [references/resources.md](references/resources.md)
- **Scoring Guide**: see [references/scoring-guide.md](references/scoring-guide.md)
- **Version**: see [references/version.md](references/version.md)
```

---

## Scope and Limitations

**What this skill covers**: AI risk assessment using the NIST AI RMF 1.0 framework — the four core functions (GOVERN, MAP, MEASURE, MANAGE), their categories and subcategories, and a structured assessment report.

**What this skill does NOT do**:
- Does NOT apply to non-AI systems — the framework targets AI systems and their lifecycle; traditional rule-based software without AI components is out of scope.
- Does NOT constitute legal advice or replace a formal compliance audit — EU AI Act risk levels and other regulatory conclusions in the report require review by a qualified human expert before any action.
- Does NOT replace security or safety testing — penetration testing, red-teaming, and OWASP-class security assessments are complementary, not substitutes.
- Does NOT guarantee compliance status. The assessment is an input to governance, not a certification.

**Assessment depth**: The AI RMF is voluntary and risk-based. Not all subcategories apply to every system. Tailor the assessment depth to the risk profile, and state explicitly which functions, categories, or subcategories were assessed, reduced, or deemed not applicable.

**Assumptions**: Conclusions are based on the inputs available. Where information is missing, proceed with explicitly stated assumptions and mark every assumption in the report (see the Assumptions field in the Executive Summary).

