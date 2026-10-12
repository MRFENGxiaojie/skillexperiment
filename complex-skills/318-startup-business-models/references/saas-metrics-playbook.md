## SaaS Metrics Playbook

Definitions, formulas, and directional benchmarks for the unit economics work
in the main workflow. Use cohorts where possible — blended averages hide
whether recent cohorts are better or worse than old ones.

### Core formulas

- **MRR / ARR** — Monthly recurring revenue: sum of recurring subscription fees
  (billed monthly). ARR = MRR × 12, used for annual framing.
- **ARPA / ARPU** — Average revenue per account (or per user): total MRR ÷
  paying accounts (or active users). Segment by plan, seat band, and channel.
- **CAC** — Customer acquisition cost: (sales + marketing spend over a period)
  ÷ new customers acquired in that period. Fully-loaded CAC includes sales
  comp, marketing, and allocated GTM overhead.
- **LTV** — Lifetime value: (ARPA × gross margin %) ÷ monthly churn rate.
- **Payback period** — CAC ÷ (ARPA × gross margin %), in months. How long a
  customer takes to repay their acquisition cost.
- **Logo churn vs revenue churn** — Logo churn: % of customers lost per month.
  Revenue churn: % of MRR lost to churn (excluding downgrades, which count as
  contraction). Track both — they diverge when small accounts churn fast.
- **NRR (net revenue retention)** — (Starting ARR + expansion − contraction −
  churn) ÷ Starting ARR, over a 12-month window. NRR > 100% means expansion
  outpaces losses.
- **Quick Ratio** — (new ARR + expansion ARR) ÷ (churned ARR + contraction
  ARR). Above 4 is strong for venture-backed SaaS; below 1 means you are
  treading water.
- **Magic Number** — (net new ARR in the quarter × 4) ÷ (sales + marketing
  spend in the prior quarter). Above 1.0 means each GTM dollar returns more
  than a dollar of annualized revenue.
- **Burn multiple** — net cash burn ÷ net new ARR. 1.0 is efficient for
  growth stage; much above 2.0 needs a close look.

### Directional benchmarks (by segment/stage)

- **LTV:CAC** — 3–5x is the common target range; below 2x is hard to defend.
- **Payback** — 6–12 months for PLG; 12–18 months early for sales-led.
- **NRR** — >100% expected at mid-market/enterprise; lower is common at SMB
  where expansion is slower.
- **Gross margin** — >70% for software-only; usage-based/AI products must
  model contribution margin per unit (token/job/workflow) because COGS scales
  with usage.

### Stage focus

- **Pre-seed / seed:** CAC, payback, gross margin. LTV is mostly noise on
  immature cohorts — say so rather than computing a misleading number.
- **Growth:** NRR, Quick Ratio, expansion behavior by segment.
- **Late / scale:** Magic Number, burn multiple, cohort-level payback and LTV.

### Template: unit economics snapshot

- Segment: [segment name, e.g., enterprise >$50k ACV]
- ARPA: [$X] — Cohort: [which cohort, e.g., Q3 2025]
- Gross margin: [X%] (include variable compute/COGS)
- CAC: [$X]
- Payback: [X months]
- Logo churn: [X%/mo] — Revenue churn: [X%/mo]
- NRR: [X%]
- LTV: [$X] — LTV:CAC: [Nx]
- Data gaps: [what is estimated vs measured, and what to measure next]
