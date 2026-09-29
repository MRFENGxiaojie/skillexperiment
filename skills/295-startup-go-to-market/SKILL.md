---
name: startup-go-to-market
description: Go-to-market strategy design and execution. Use when designing go-to-market strategy, selecting GTM motion (PLG/sales-led), defining ICP, planning product launches, or implementing AI-powered GTM automation. Covers channel selection, growth loops, RevOps alignment, and market entry execution.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Startup Go-to-Market

Systematic workflow for designing and executing market entry, launch, and growth.

**Modern Best Practices**: Start from ICP + positioning, pick 1-2 channels to sequence, instrument the funnel end-to-end, use AI for execution (not strategy), align RevOps across sales/marketing/CS.

---

## When to Use

- Designing go-to-market strategy for new product
- Choosing between PLG and sales-led motion
- Planning product launches (soft, beta, ProductHunt, full)
- Defining ICP and channel strategy
- Implementing AI-powered GTM automation

## When NOT to Use

- Positioning and messaging deep dive -> `marketing-content-strategy` (use `startup-competitive-analysis` for differentiation inputs)
- Competitive intelligence -> `startup-competitive-analysis`
- Fundraising strategy -> `startup-fundraising`
- Pricing and revenue models -> `startup-business-models`

---

## Quick Start (Inputs)

Ask for the smallest set of inputs that makes decisions meaningful:

- Stage: pre-PMF, early PMF, growth, scale
- Product and category: what it is, who uses it, and what "first value" looks like
- ICP and buyer: firmographics, pains, procurement constraints, economic buyer vs champion
- Pricing and economics: current/target ACV/ARPA, COGS drivers (include variable compute), payback constraints
- Motion constraints: self-serve possible, sales cycle expectations, implementation/onboarding complexity
- Channel constraints: budget, time, audience access (communities, lists, partnerships), geo, compliance limits
- Baseline metrics: traffic, signup/demo rate, activation, retention, win rate, sales cycle length, pipeline
- Team and tooling: who executes (founder/marketing/sales/CS), CRM + analytics stack

If numbers are missing, proceed with ranges + explicit assumptions and list what to measure next.

## Workflow

1) Define ICP and the buying path
- Primary/secondary ICP, anti-ICP, trigger events, and an "activation" definition.
- Use `assets/icp-definition.md` to draft.

2) Align on positioning and proof
- If positioning is unclear, use the `startup-competitive-analysis` skill to map alternatives + differentiation, then the `marketing-content-strategy` skill to express it as messaging.

3) Choose the motion (PLG / sales-led / hybrid)
- Use the decision tree below for a fast cut.
- For details: `references/plg-implementation.md` and `references/sales-motion-design.md`.

4) Pick 1-2 channels to sequence (not parallelize)
- Use a bullseye-style test plan: quick tests, measure, double down.
- Set channel test criteria before spending: define the success metric and threshold in advance (for example, demo rate >= 2% and CAC within target on the first small spend), double down only on channels that hit threshold, kill any channel that misses its threshold twice in a row, and revisit the plan after 2-4 weeks instead of optimizing forever.

5) Define measurement and RevOps alignment
- Define shared lifecycle stages and the "one source of truth" for metrics (product + CRM).
- Ensure handoffs are measurable (e.g., PQL -> SQL routing rules and SLAs for hybrid).

6) Produce deliverables + operating cadence
- Draft GTM plan (`assets/gtm-strategy.md`) and launch plan (`assets/launch-playbook.md`).
- Run a weekly GTM review: 30 minutes on pipeline + funnel, 30 minutes on experiments, 30 minutes on decisions.

---

## Deliverable Format

Two deliverables come out of this workflow: the GTM strategy and the launch playbook. Both are drafted in step 6 and kept as living documents.

**GTM Strategy** (`assets/gtm-strategy.md`): executive summary, ICP and segmentation, positioning and proof, motion and economics, channels (1-2, each with budget, test plan, and stop/pivot triggers), measurement, launch, RevOps alignment, risks.

**Launch Playbook** (`assets/launch-playbook.md`): launch type and goal, success criteria (minimum and stretch numbers), audience and channels, assets checklist, timeline with owners, launch-day checklist, post-launch review.

**Quality bar for both** (see What Good Looks Like): one primary ICP with anti-ICP and measurable triggers, a motion decision with explicit economics and defined handoffs, one primary channel with a test plan and stop/pivot triggers, an instrumented funnel from source to revenue, and a weekly operating cadence with a decision log.

---

## Decision Tree

```
Motion: ACV < $5K and self-serve possible?
  - yes -> PLG (add sales-assist for expansion) -> Channel Strategy
  - no -> is the buyer technical?
      - yes -> developer/community-led (bottom-up) -> Channel Strategy
      - no -> sales-led -> Sales Motion Design (references/sales-motion-design.md)

Channel: where does the ICP already pay attention?
  - Pre-PMF -> founder sales + communities
  - Early -> content, outbound, founder network
  - Growth -> paid, SEO, partnerships
  - Scale -> all channels, optimized

Launch: what is the goal?
  - Test and iterate -> soft launch (2-4 weeks)
  - Build waitlist and feedback -> beta (4-8 weeks)
  - Awareness and early adopters -> ProductHunt (1 day + prep)
  - Maximum awareness -> full launch (1-2 weeks)

ICP: who do we serve first? -> primary ICP + anti-ICP, tiered by fit + intent
Scale: what loop compounds? -> Growth Loops (pick one to invest in)
```

---

## GTM Motion Types

- **PLG**: Product drives acquisition, conversion, expansion. Best for SMB, developers. Examples: Slack, Figma.
- **Hybrid (PLG + Sales-Assist)**: Product drives acquisition; sales assists conversion/expansion. Best for mid-market, higher ACV PLG. Examples: Atlassian, Notion.
- **Sales-Led**: Reps drive deals through outbound/inbound. Best for enterprise, complex sales. Examples: Salesforce.
- **Community-Led**: Community drives awareness and adoption. Best for developer tools, OSS. Examples: MongoDB.
- **Partner-Led**: Partners drive distribution. Best for enterprise, geographic expansion. Examples: Microsoft.

### Motion Selection Framework

```
ACV < $5K and self-serve possible?
  - yes: PLG (add sales-assist for expansion)
  - no: is buyer technical?
      - yes: developer/community-led (bottom-up)
      - no: sales-led
```

---

## ICP Components

- **Firmographics**: Size, industry, geography. Example: 50-500 employees, B2B SaaS, US.
- **Technographics**: Tech stack, tools. Example: Uses Salesforce, modern data stack.
- **Pain indicators**: Symptoms of problem. Example: Growing support tickets.
- **Success indicators**: Signs of good fit. Example: Strong product-market alignment.

### ICP Scoring

- Budget available: 20% weight.
- Problem severity: 25% weight.
- Technical fit: 15% weight.
- Decision timeline: 15% weight.
- Champion identified: 15% weight.
- Expansion potential: 10% weight.

---

## Channel Strategy

- **Organic**: SEO, content, social, community. Best for long-term.
- **Paid**: SEM, paid social, display. Best for fast, scalable.
- **Outbound**: Email, cold calls, LinkedIn. Best for enterprise, high ACV.
- **Product**: Viral, freemium, PLG. Best for self-serve.

### Channel Sequencing by Stage

- **Pre-PMF**: Founder sales, communities.
- **Early**: Content, outbound, founder network.
- **Growth**: Paid, SEO, partnerships.
- **Scale**: All channels optimized.

---

## Measurement (Minimum Viable GTM Analytics)

- Prefer lifecycle + cohorts over vanity metrics. Always break down by ICP/segment + channel.
- Define a single funnel per motion (PLG vs sales-led) with clear stage definitions and owners.
- Track leading indicators (activation/retention, PQL, win rate) before "scale" decisions.

**PQL (Product Qualified Lead) Score**:
```
PQL = (Engagement * 0.4) + (Fit * 0.3) + (Intent * 0.3)
```

### Product-Led Sales (Sales-Assist) Basics

Use when PLG brings users in, but conversion/expansion benefits from a human touch.

**PQL -> SQL routing checklist**:
- [ ] Define PQL triggers (events) and thresholds (e.g., 3 key actions in 7 days)
- [ ] Define disqualifiers (students, competitors, tiny companies, unsupported geo)
- [ ] Set an SLA for first touch (e.g., <24 hours for high-intent PQLs)
- [ ] Define handoff criteria to AE (PQL -> meeting booked, security/procurement requested)
- [ ] Instrument outcomes (PQL->meeting->pipeline->won) and review weekly

### AI for Execution (Not Strategy)

Humans own strategy; AI carries the execution load. Practical starting points:

- Score leads and PQLs from product + CRM signals instead of manual triage
- Automate channel reporting and anomaly alerts so the weekly review reads numbers, not builds them
- Draft A/B variants (copy, landing pages, emails) for the experiment backlog
- Summarize call and ticket themes into the decision log

Every AI output gets a human review before it enters the plan or the decision log.

---

## Launch Types

- **Soft launch**: Goal is test, iterate. Timeline: 2-4 weeks.
- **Beta launch**: Goal is build waitlist, feedback. Timeline: 4-8 weeks.
- **ProductHunt**: Goal is awareness, early adopters. Timeline: 1 day + prep.
- **Full launch**: Goal is maximum awareness. Timeline: 1-2 weeks.

---

## Growth Loops

- **Viral**: Mechanism is user invites users. Example: Dropbox referrals.
- **Content**: Mechanism is content -> SEO -> users. Example: HubSpot.
- **UGC**: Mechanism is users create content. Example: YouTube.
- **Paid**: Mechanism is revenue -> ads -> users. Example: Performance marketing.
- **Sales**: Mechanism is pipeline -> close -> revenue -> hiring -> more pipeline. Example: Sales-led SaaS.
- **Partner**: Mechanism is enable partners -> referrals -> deals -> partner revenue -> more partners. Example: Cloud marketplaces.

---

## Do / Avoid

### Do

- Define activation as concrete "first value moment"
- Track leading indicators (activation, PQL, retention)
- Use AI for execution while humans own strategy
- Tier ICP based on fit + intent signals

### Avoid

- Content spam without measurement
- "Do all channels" in parallel
- Vanity metrics without retention context
- Over-automating without human oversight
- Scaling paid before activation/retention is stable
- Treating benchmarks as targets without segmenting by ICP/channel

---

## Resources

- [assets/icp-definition.md](assets/icp-definition.md): ICP draft template (Workflow step 1).
- [assets/gtm-strategy.md](assets/gtm-strategy.md): GTM strategy template (Workflow step 6).
- [assets/launch-playbook.md](assets/launch-playbook.md): Launch playbook template (Workflow step 6).

## Templates

- [references/plg-implementation.md](references/plg-implementation.md): PLG build order, free tier decisions, metrics (Workflow step 3).
- [references/sales-motion-design.md](references/sales-motion-design.md): Sales motion roles, routing rules, SLAs (Workflow step 3).

## Data

- [sources.json](data/sources.json): Starting points for GTM research.

---

## Related Skills

- `startup-competitive-analysis`: Market mapping, battlecards.
- `startup-business-models`: Pricing, unit economics.
- `marketing-ai-search-optimization`: GEO/AI search visibility for content-led GTM.
- `marketing-social-media`: Social channel execution.
- `marketing-leads-generation`: Lead acquisition.

---

## What Good Looks Like

- One primary ICP with clear anti-ICP and measurable triggers (signals) for targeting.
- A motion decision with explicit economics (ACV, payback, touch model) and defined handoffs.
- One primary channel with a test plan, success metrics, and stop/pivot triggers.
- Instrumented funnel from source -> activation/value -> revenue/expansion (by segment + channel).
- A weekly operating cadence with a backlog of experiments and a written decision log.

