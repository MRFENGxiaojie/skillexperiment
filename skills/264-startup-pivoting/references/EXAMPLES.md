# Examples

**Example 1 (B2B SaaS stuck pre-PMF):** “We built an AI support copilot for SMBs. Trials convert, but retention is poor and sales cycles are long. We have 6 months of runway. Should we pivot, and if so how?”  
Expected: a Pivot Decision & Execution Pack with an exhaustion check (pricing/onboarding/ICP), 4–8 pivot options including at least one 200% pivot, a chosen thesis with metrics/kill criteria, and a 4–6 week pivot sprint plan.

**Example 2 (Consumer plateau):** “Our language learning app growth stalled and D30 retention is low. We suspect our promise is wrong. Create a pivot options map and a validation plan.”  
Expected: a 4P pivot grid that includes positioning/package changes and at least one new persona/problem angle, plus a time-boxed validation plan with decision gates.

**Boundary example:** “Just tell us what to pivot to—no metrics, no customers, no constraints.”  
Response: explain that pivoting without evidence is guesswork; ask up to 5 intake questions, propose a discovery/validation sprint, and only then produce a pivot thesis and plan.

---

# Filled Example Pack (Example 1 — B2B SaaS stuck pre-PMF)

Prompt: “We built an AI support copilot for SMBs. Trials convert, but retention is poor and sales cycles are long. We have 6 months of runway. Should we pivot, and if so how?”

## 1) Context snapshot

- **Product today:** AI support copilot that answers customer tickets for SMB teams.
- **Target customer (current):** SMBs (10-50 employees) with a support inbox but no dedicated support team.
- **Current promise:** “Your support tickets resolve themselves.”
- **Stage:** pre-PMF.
- **Runway / decision date:** 6 months; decision gate at end of Week 6 of the sprint.
- **Non-negotiables:** no compliance-heavy verticals; maintain product-led signup; team of 3 (2 eng, 1 design/marketing).
- **Decision owner + stakeholders:** Founder (owner); 2 co-founders aligned by Week 2.

## 2) Stuck diagnosis

- **Symptoms:** trials convert (35% start paid trial), but D30 retention 18%; sales cycle 6-10 weeks; 60% of trials never answer a single ticket with the product.
- **Hypothesized causes (ranked):**
  1. Wrong promise — SMBs expect “tickets resolved,” but the product only drafts replies; their real job is triage/routing, not resolution.
  2. Wrong persona — buyer is the office manager (low budget authority); actual user is the customer-facing rep who doesn't set up tools.
  3. Onboarding gap — first-value comes only after connecting 3+ channels; most trials connect one and churn.
- **Evidence we have:** trial funnel data, 12 churned-customer interviews, session recordings.
- **Evidence gaps:** what happens in the first 48h of successful trials; whether the rep vs manager pain differs; willingness to pay for a triage-only product.

## 3) Exhaustion check

| Lever | Have we tried it well? | Evidence/result | Why it did/didn’t work | Best next attempt (time-boxed) |
|---|---|---|---|---|
| ICP refinement | Partially | Tried ecommerce and agency segments | Churn pattern identical across both | None — segmentation alone won't fix retention |
| Positioning/promise | No | Copy still promises “resolution” | Product can't deliver fully automated resolution | 2-week repositioning test on trial landing page |
| Pricing/packaging | No | Single tier, free trial | No signal on price sensitivity | None before validation |
| Onboarding/time-to-value | No | Setup requires 3 integrations | First value not reached in first session | 1-week guided setup for next 20 trials |
| Distribution/channel | Partially | Content + marketplace listing | Slow, low volume | None — direction question first |
| Reliability/trust | Yes | Uptime fine | Not the blocker | None |

**Last best non-pivot moves (time-boxed):** repositioning copy test (2 weeks) + guided setup (1 week). If neither moves D30 retention past 25% by Week 3, pivot.

## 4) Pivot options map (4P grid)

| Option | Problem | Persona | Product | Positioning/Package | 10% or 200% | Why this could win | What must be true | Biggest risks |
|---|---|---|---|---|---|---|---|---|
| A | Keep | Keep | Triage + routing layer, human-in-the-loop | “Run your support triage” | 200% | Solves the actual daily job; demoable in first session | Reps will adopt a tool that routes/prioritizes tickets | We can't build a routing engine well enough in 6 months |
| B | Keep | Keep | Improve answer quality with more models | “Fully automated support” | 10% | Better answers raise perceived value | Retention is answer-quality driven (evidence says no) | Wastes 2 months on the wrong lever |
| C | Keep | Shift to product-led ecommerce stores | Keep copilot, add refund/order handling | “Ecommerce support copilot” | 200% | Pain is acute; buyers are solo founders with authority | Ecommerce churn pattern differs from current data | Rebuild integrations for Shopify/Stripe |
| D | Shift to internal ops teams | Keep | Ticket tagging + analytics for ops | “Support intelligence” | 200% | Higher budget authority, clearer ROI story | Ops teams buy mid-market tools at this stage | Long sales cycles again |
| E | Keep | Keep | Keep | Package as agency add-on (white-label) | 10% | Agency channel could distribute | Agencies have clients who need this | Channel build-out longer than runway |

## 5) Chosen pivot thesis + metrics + kill criteria

- **Thesis:** SMB support reps will adopt a triage-and-route copilot (Option A) because their daily bottleneck is prioritization, not drafting. The 200% bet: reposition from “answers tickets” to “runs your triage.”
- **North Star:** % of weekly active trials that reach “routed 10+ tickets in a week”.
- **Leading indicators (2-5):** activation (first route within 48h), 10-ticket week rate, W4 retention, trial→paid conversion on repositioned landing page.
- **Guardrails:** support workload per agent ≤ current manual time; no security/compliance exposure.
- **Kill criteria:** by Week 6, if fewer than 8 of 20 new trials reach the 10-ticket week, or W4 retention < 30%, shut down and evaluate Option C.

## 6) Validation plan

| Learning goal | Method | Sample/target | Success threshold | Decision if fails | Owner | Date |
|---|---|---|---|---|---|---|
| Do reps adopt routing in first session? | Guided setup + session recordings on 10 trials | 10 trials | ≥5 route 3+ tickets in 48h | Reposition again or switch option | Eng | Week 2 |
| Willingness to pay for triage promise | Pricing page A/B on trial start | 100 visitors | ≥20% click-through to trial | Weaker signal; rely on activation | Design | Week 3 |
| W4 retention under new promise | Cohort measurement | 20 new trials | ≥30% W4 retention | Kill criteria triggers | Eng | Week 6 |

## 7) Execution plan (pivot sprint)

- **Scope (build):** routing/triage inbox view; guided setup; repositioned landing page.
- **Cut list:** answer-drafting polish; mobile app; marketplace listing work.
- **Timeline:** Week 1-2 build routing MVP + guided setup; Week 3-4 run 20-trial cohort + A/B; Week 5-6 analyze, decide at gate.
- **Comms:** team weekly (decision gate preview); 12 interviewed customers notified of the shift; investors updated at Week 6 gate.

## 8) Risks / Open questions / Next steps

- **Risks:** routing engine quality slips; repositioning confuses existing trial users; runway is only 6 months — a second 200% pivot is not possible.
- **Open questions:** Does the rep actually open the triage view daily? Is the buyer still the office manager in ecommerce?
- **Next steps:** owner confirms decision date; design ships repositioned landing page (Week 1); eng starts routing MVP (Week 1); update this memo at the Week 6 gate.
