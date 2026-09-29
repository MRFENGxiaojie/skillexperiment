---
name: startup-idea-validation
description: Startup idea validation with an evidence-based GO/NO-GO decision framework. Use when validating a startup idea before building. Produces evidence-based GO/NO-GO decisions using a weighted 9-dimension scorecard and a riskiest-assumption-first validation ladder.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Startup Idea Validation

Systematic validation for testing ideas before building: define hypotheses, collect evidence, score the opportunity, and make a decision you can defend.

## Operating Principles (2026)

- Prefer decisions over inventories: each dimension ends with `GO / CONDITIONAL / PIVOT / NO-GO` and a next action.
- Separate evidence quality from confidence: weak evidence cannot justify a high score.
- Pre-register thresholds and stop rules before running experiments (avoid moving goalposts).
- Validate willingness-to-pay and time-to-value early (price is part of the product).
- Calibrate thresholds to the target outcome (venture-scale vs cash-flow business) and business model (B2B SaaS, B2C, marketplace, services).
- Stay safe and ethical: no misrepresentation, respect ToS, and handle customer data with minimization and retention limits.

## Intake Checklist (Ask First)

- One-sentence idea + target user + job-to-be-done
- Business model: B2B/B2C, SaaS/usage-based/marketplace/services, ACV/ARPU range
- Geography, constraints (regulated domain, procurement/security requirements, data access)
- Target outcome: venture-scale, profitable small business, or thesis-driven R&D
- Current evidence: interviews, pilots, pre-sales, traffic, competitor list, pricing assumptions

## Choose the Right Output

- If the user asks to validate a full idea before building, produce a 9-dimension scorecard + verdict using the 9-Dimension Scorecard.
- If the user asks what is the riskiest assumption, produce a RAT + test plan using Workflow steps 2-4.
- If the user asks to design experiments or hypotheses, produce a Hypothesis canvas using Workflow step 4 + Validation Ladder.
- If the user asks how big the market is, produce a market sizing using the Market size dimension + Evidence Rules.
- If the user asks whether the unit economics are viable, produce unit economics + runway using the Unit economics dimension + AI cost notes.
- If the user asks to compare two or more ideas, produce a comparative scorecard using the 9-Dimension Scorecard applied to each option.

## Workflow

1. Clarify the target outcome (venture-scale, cash-flow business, or R&D) and business model with the intake checklist.
2. Identify the riskiest assumption (RAT) — the assumption that kills the business if wrong — and choose the cheapest test that can falsify it first, starting at the top of the validation ladder.
3. Prioritize evidence collection around the RAT: gather only the evidence needed to pass or fail it. Typical riskiest assumptions are that customers will pay (willingness-to-pay), that the product can be acquired cheaply (CAC), that the workflow actually saves time (time-to-value), and that data access is legal and reliable.
4. Run the cheapest falsifiable test first; pre-register PASS/FAIL thresholds and stop rules.
5. Score all 9 dimensions using the rubric below; downgrade scores when evidence is weak (opinions and hypotheticals).
6. Produce a decision memo: verdict, why, what would change the decision, and the next smallest reversible step.

## 9-Dimension Scorecard

- Problem severity has a weight of 15% and measures urgency, cost of inaction, and current workarounds.
- Market size has a weight of 12% and measures sufficient demand for the target outcome.
- Market timing has a weight of 10% and measures a clear "why now" and tailwinds.
- Competitive moat has a weight of 12% and measures defensibility over time.
- Unit economics has a weight of 15% and measures the profit path (incl. payback and margins).
- Founder-market fit has a weight of 8% and measures access, expertise, and execution capability.
- Technical feasibility has a weight of 10% and measures buildability, dependencies, and constraints.
- GTM clarity has a weight of 10% and measures ICP, channels, motion, and first customers.
- Risk profile has a weight of 8% and measures what can kill it and likelihood.

**Scoring scale:** Score each dimension 0-100. The composite is the weighted average — the sum of weight × score across all nine dimensions, divided by 100 — so the total stays on the same scale as the thresholds.

**Rubric anchors:**
- 70-100 (strong): behavioral commitment with cost — real spend, signed commitments, repeated use, validated willingness-to-pay; claims triangulated across at least two sources
- 40-69 (partial): some signal — a single interview, expressed interest, proxy metrics, or competitor validation
- 0-39 (weak): opinions, hypotheticals, and untested assumptions

A 70+ score per dimension typically requires: problem severity — repeated pain with real workarounds and current spend; market size — a credible TAM from two or more sources; timing — a concrete "why now"; moat — defensibility that holds beyond launch; unit economics — a plausible profit path including payback; founder-market fit — direct access, expertise, or a track record; technical feasibility — a realistic build path with known dependencies; GTM clarity — a named ICP, channel, and first customers; risk profile — the main kill risks identified with a mitigation or exit.

**Verdict thresholds (default)**:
- `80-100`: GO — proceed to the next smallest reversible step (expand the test, start pre-sales)
- `60-79`: CONDITIONAL — validate the RAT first, then re-score
- `40-59`: PIVOT — restate the hypothesis, change the riskiest dimension, and retest
- `<40`: NO-GO — stop investing; record the failure evidence and lessons for the next idea

## Evidence Rules

- Strong evidence is behavioral commitment with cost (time, money, switching, access); weak evidence is opinions and hypotheticals.
- Triangulate important claims across at least two sources (especially market sizing and competitor state).
- Keep an evidence trail: link + capture month; separate "fact" vs "assumption". For example: `[G2 reviews analysis](https://example.com/g2) — capture 2026-07 — fact`, `ACV $15K assumed from 2 interviews — capture 2026-06 — assumption`.

## Validation Ladder (Default)

- Interviews: goal is to validate the problem and context; a strong signal is repeated pain with real workarounds and spend.
- Smoke test: goal is to validate demand; a strong signal is qualified conversion with price shown.
- Concierge/WoZ: goal is to validate workflow value; a strong signal is users complete the job and return.
- Paid pilot: goal is to validate willingness-to-pay; a strong signal is paid, renewed, or expanded.

## AI / Automation Notes (2026)

If the idea depends on AI (agents, copilots, automation), validate these explicitly:

- Data rights and access: can you legally and reliably access required data?
- Reliability: define success metrics, failure modes, and human fallback; validate on real workflows.
- Cost-to-serve: estimate inference + retrieval + human-in-the-loop costs per active user per month and compare against expected revenue per user; a concierge pilot with real AI outputs is the cheapest way to get an actual number.
- Run AI-specific experiments on real workflows: a concierge/WoZ setup that ships real model outputs, a smoke test with a priced landing page, or a limited paid pilot. Pre-register success metrics, failure modes, and the human fallback before starting.

## Decision Memo

Finish every validation with a one-page decision memo:

- Verdict: GO / CONDITIONAL / PIVOT / NO-GO, with the composite score
- Why: one-line evidence summary per dimension, tagged fact or assumption
- What would change the decision: the specific evidence that would flip the verdict
- Next smallest reversible step: the cheapest action that produces new evidence

The memo is a decision record the founder can revisit as new evidence arrives, not a report.

## Scope / Limitations

This skill validates ideas before building. It does not:

- Produce a build roadmap, feature plan, or product spec
- Write a full business plan or a deep financial model
- Replace real customer interviews, pilots, or legal and compliance review
- Guarantee success — a verdict reflects the current evidence, not the future

Scores rest on evidence, not confidence: when behavioral evidence is missing, the verdict lands at CONDITIONAL or NO-GO, never GO.

## Integration Points

### Receives From

- the `discovery-interviews-surveys` skill - Pain point evidence
- the `startup-trend-prediction` skill - Market timing inputs
- the `competitive-landscape` skill - Competitor landscape

### Feeds Into

- the `product-manager-toolkit` skill - Validated requirements and roadmap inputs
- the `startup-business-models` skill - Monetization and packaging decisions
- the `startup-go-to-market` skill - Validated ICP, demand, and positioning inputs

