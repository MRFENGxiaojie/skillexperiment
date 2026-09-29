---
name: startup-business-models
description: Analyzes and recommends startup revenue models, pricing design, and unit economics. Use when the user needs to choose or evaluate a revenue model, design pricing and packaging tiers, or calculate unit economics — including usage-based, credit-based, and AI pricing with variable compute cost constraints.
allowed-tools: Read, Write
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Startup Business Models

Systematic workflow for choosing revenue models, pricing, and unit economics.

## Quick Start (Inputs)

Ask for the smallest set of inputs that makes the decision meaningful:

- Business type: SaaS, usage-based/API, marketplace, services, hardware + service
- ICP/segment(s): SMB / mid-market / enterprise (and ACV/ARPA bands)
- Current pricing and packaging: value metric, tiers, limits, discount policy, billing cadence
- Unit economics drivers: fully-loaded CAC, gross margin/COGS (include LLM/infra/third-party), churn/retention, expansion (NRR)
- Constraints: sales motion (PLG vs sales-led), implementation constraints (billing metering, proration), gross margin floor, payback target

If numbers are missing, proceed with ranges + explicit assumptions and highlight what to measure next.

## Workflow

1) Classify the model
- Subscription, usage-based, freemium, marketplace take-rate, transaction fee, ads, outcome-based, credit-based, hybrid.

2) Build a segment-level unit economics snapshot
- Refer to `references/saas-metrics-playbook.md` for the standard formulas and benchmark ranges (LTV, CAC, payback, NRR, Quick Ratio, Magic Number).
- Prefer cohort/segment views over blended averages.

3) Evaluate model fit and risks
- Align price metric with value delivered and cost incurred (especially usage + AI compute).
- Identify failure modes: margin compression, adverse selection, channel conflict, support cost explosions, metering/overage friction.

4) Propose pricing + packaging changes
- Validate willingness to pay: check the value metric against what customers already pay for today, run pricing interviews with 5-8 current or prospective customers (state the current price, then a higher one, and watch for hesitation), and note competitive anchors.
- Draft tiers around the value metric: a clear free/entry tier, a paid tier priced well above it, limits and overage rules that map to usage units, upgrade triggers tied to measurable thresholds (seats, usage, features), and enforcement rules (hard limits vs. soft prompts, credit expiries, rate limits).

5) Define measurement and roll-out
- Define success metric + guardrails, evaluation design, and explicit lag windows (conversion now, retention later).

6) Deliver a decision-ready output
- Recommendation, rationale, assumptions, scenarios (base/best/worst), and next experiments.

## 2026 Heuristics (Context-Dependent)

- Prioritize payback and gross margin over a single ratio; LTV:CAC is easiest to game.
- Typical SaaS targets (directional, by segment/stage): LTV:CAC 3-5x, payback 6-12 months (PLG) or 12-18 months (sales-led early), NRR >100% (mid-market/enterprise) and gross margin >70% (software-only).
- For usage-based / AI products: model contribution margin per unit (token/job/workflow) and set pricing guardrails (rate limits, minimums, commit tiers, credit expiries).

## Related Skills (Routing)

- the `startup-idea-validation` skill
- the `startup-competitive-analysis` skill
- the `startup-fundraising` skill
- the `startup-go-to-market` skill

## Limitations

- Applies to digital business models (SaaS, usage-based, marketplace, subscription); not designed for manufacturing, retail, or heavy-asset industries.
- Provides analysis frameworks and benchmark references, not legal, tax, or accounting advice.
- Output accuracy depends on input data quality — when using assumption ranges, mark them transparently in the output.
- Does not execute pricing changes (A/B test platform setup, billing system integration, contract renegotiation).
- Does not replace a pricing consultant or revenue operations team — it structures the analysis, the company still runs it.

## Pricing Change Measurement & Experiment Design
Use this when you are changing pricing, packaging, value metric, limits, discounts, or billing cadence.

### 1) Define success and guardrails (before launch)
- Primary success metric: net revenue retention (NRR), ARPA/ARPU, gross margin %, payback period, upgrade rate, expansion MRR.
- Guardrails: new logo conversion, activation rate, refund rate, support load, churn (logo + revenue), sales cycle length.

### 2) Pick an evaluation design
- A/B (randomized) is best when the flow is self-serve / PLG; read results by comparing conversion, ARPA, refunds, and downstream retention by assignment.
- Holdout/control cohort is best when pricing is hard to randomize; read results by comparing treated vs. holdout cohorts matched on segment, channel, and start month.
- Step rollout (time-based) is best for enterprise contracts and invoicing cycles; read results by comparing pre/post with a parallel cohort (not exposed yet) to reduce seasonality bias.
- Geo/account rollout is best when regions/segments are separable; read results by comparing regions/segments and watching for channel mix shifts.

### 3) Use explicit lag windows (avoid premature conclusions)
- Short lag (days to 2 weeks): checkout conversion, activation, sales cycle friction, refund/support spikes.
- Medium lag (4 to 8 weeks): upgrades, expansion MRR, usage growth, discounting behavior, proration effects.
- Long lag (90 to 180+ days, B2B): churn, net revenue retention, renewal outcomes, contraction risk.

### 4) Report an "all-in" view (not just conversion)
- Revenue quality: net revenue after refunds, discounts, and credits; gross margin impact (including variable compute/COGS).
- Segments: break down by plan, seat band, channel, ACV/ARR band, and customer age (new vs. renewal).
- Decision rule: write a go/no-go threshold (example: "NRR +2pts with no >0.5pt drop in activation and no >10% increase in support load").

## SaaS Metrics (Read When Needed)

Use `references/saas-metrics-playbook.md` for definitions and templates (MRR/ARR, churn, NRR, Quick Ratio, Magic Number, burn multiple, stage focus).

## Output Format

Structure the deliverable with these sections:

1. **Executive Summary** — 3-5 sentence synthesis of the recommendation and key rationale.
2. **Model Classification** — which of the 9 model types applies, with justification.
3. **Segment-Level Unit Economics** — per segment: CAC, gross margin, churn, payback, NRR, LTV with cohort notes.
4. **Risk Assessment** — each of the 5 failure modes evaluated for this model.
5. **Pricing Recommendations** — proposed changes with rationale, tier design, and discount guardrails.
6. **Measurement Plan** — success metric, guardrails, evaluation design choice, lag windows, go/no-go threshold.
7. **Assumptions Register** — all assumptions in one place with ranges/sensitivities where data was missing.
8. **Next Experiments** — prioritized list of tests to run.

---

## Do / Avoid (2026)

### Do

- Define your value metric (seat/usage/outcome) and validate willingness-to-pay early.
- Include COGS drivers in pricing decisions (especially usage-based).
- Use discount guardrails and renewal logic (avoid ad-hoc deals).

### Avoid

- Pricing as an afterthought (“we’ll figure it out later”).
- Margin blindness (shipping usage growth that destroys gross margin).
- Misleading LTV calculations from immature cohorts.

## What Good Looks Like

- Packaging: a clear value metric, tier logic, and discount policy (with enforcement rules).
- Unit economics: CAC, gross margin, churn, payback, and retention defined and tied to cohorts.
- Assumptions: one inputs sheet, ranges/sensitivities, and scenarios (base/best/worst).
- Experiments: pricing changes tested with decision rules (not “gut feel” rollouts).
- Risks: margin compression, adverse selection, channel conflict, and support cost modeled.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant. If not explicitly
requested, do not use AI features — rely on the deterministic workflow above.

- Summarize pricing research and competitor snapshots; verify manually before acting.
- Draft pricing page copy; humans verify claims and consistency with contracts.

