---
name: pricing-strategist
description: Builds comprehensive pricing strategies by reading business context and asking targeted questions interactively. Use when user needs pricing plans, tier structures, price points, pricing model recommendations, or any pricing-related strategy for their product or service.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Pricing Strategist

## Purpose
Build a comprehensive, justified pricing strategy — tier structures, price points, positioning, and revenue optimization — tailored to the business through context and conversation.

---

## Execution Logic

**Check $ARGUMENTS first to determine execution mode:**

### If $ARGUMENTS is empty or not provided:
Respond with:
"pricing-strategist loaded, ready to build your pricing strategy"

Then proceed from the request and available context; ask only if essential context is genuinely missing.

### If $ARGUMENTS contains content:
Proceed immediately to Task Execution (skip the "loaded" message).

---

## Task Execution

### 1. MANDATORY: Read FOUNDER_CONTEXT.md
**BLOCKING REQUIREMENT — DO NOT SKIP THIS STEP**

Before doing ANYTHING else, read `FOUNDER_CONTEXT.md` from the project root. Extract everything relevant to pricing:
- Company name, industry, product/service type
- Target audience (demographics, pain points, budget signals)
- Existing pricing model (if any)
- Competitors and their pricing (if mentioned)
- Value proposition and key features/benefits
- Business stage and revenue goals

**DO NOT PROCEED** to Step 2 until this file has been read.

### 2. Determine Which Questions to Ask
Cross-reference what FOUNDER_CONTEXT.md already provides against the Question Bank below. **Only ask questions where the answer is genuinely missing or unclear.** Never ask something the context already answers.

**Question Bank (priority order):**

- Ask whether the target is B2B or B2C; this matters because it changes deal size, tier logic, sales cycle, and everything. Skip it if the target audience section makes it obvious.
- Ask what pricing model the customer prefers or wants to avoid (subscription, one-time, usage-based, freemium, hybrid), since it determines the entire structure. Skip it if the pricing model is already stated in context.
- Ask what the primary value metric that scales with usage is (seats, API calls, storage, projects, transactions, etc.), since it drives tier differentiation and upgrade logic. Skip it if the product type plus features make it obvious.
- Ask about the target gross margin range (60-70%, 70-80%, 80%+, not sure), since it sets the floor for every price point. Skip it if a number or range is already given.
- Ask how price-sensitive the target customer is (very sensitive, moderate, willing to pay premium), since it calibrates price positioning and tier gaps. Skip it if audience detail plus industry norms make it clear.
- Ask who the closest competitors are and how they price, since this provides market anchoring and prevents under- or over-pricing. Skip it if the competitors section is filled.
- Determine the current stage or revenue target (pre-revenue, <$10K MRR, $10-50K MRR, $50K+ MRR) since it calibrates ambition and tier complexity. Skip it if the business goals mention revenue or stage.

**Derive inputs from the request and available context first.** Ask only the highest-priority genuinely missing questions, batched and minimal; stop as soon as you can build a strong strategy with what you have.

### 3. Determine Strategy Type
Based on all collected inputs, decide the structure. **Make this decision yourself — do not ask the user.** Explain why in the output.

- If the model is Subscription + B2B, use **SaaS Tiered**: Starter / Pro / Business / Enterprise.
- If the model is Subscription + B2C, use **Consumer Tiered**: Free / Basic / Premium.
- If usage-based is the primary model, use **Usage Tiers**: base fee + usage bands with overage pricing.
- If it is a one-time purchase, use **Package Pricing**: Good / Better / Best bundles.
- If freemium is preferred, use **Freemium**: generous free tier + 2-3 paid tiers.
- If signals are mixed, use **Hybrid**: combine structures as the inputs warrant.

### 4. Build the Pricing Strategy
For each tier, define:
- **Plan name** — descriptive, not generic. "Starter" beats "Plan A". "Growth" beats "Mid".
- **Price point** — monthly AND annual (annual ≈ 20% off monthly). Use specific numbers.
- **Price justification** — why this number. Anchor to: competitor benchmarks, value delivered, margin targets, or customer willingness to pay. Never leave a price unjustified.
- **Feature set** — what's in, and critically, what's deliberately left out to drive upgrades.
- **Target segment** — the specific customer who buys this tier and why.

### 5. Add the Strategic Layer
Beyond the tiers:
- **Positioning** — where this sits vs. competitors (premium, mid-market, value leader, underdog)
- **Psychological tactics used** — name them and explain why each one was chosen (charm pricing, anchoring, decoy effect, loss aversion in annual vs. monthly, etc.)
- **Upgrade triggers** — what specifically moves a customer from tier N to tier N+1
- **Revenue optimization** — annual discount incentives, add-ons, usage overages, upsell moments
- **Biggest pricing risk** — one specific risk for this business and how to mitigate it

### 6. Format and Verify
- Structure output per **Output Format** below
- Run through **Quality Checklist** before presenting

---

## Pricing Principles
Hard constraints. These exist because bad pricing destroys margins or kills growth.

- Price on value delivered. Never on cost to build.
- Every tier must have a clear reason to exist. If no real customer would buy it, cut it.
- The middle tier is the hero. Design the strategy so most customers land there.
- Annual pricing should feel like a no-brainer — 20-25% off. Monthly is the convenience premium.
- Never show more than 4 tiers. Paradox of choice kills conversion at the pricing page.
- Enterprise = "contact sales" unless the business is pre-revenue. Pre-revenue can skip Enterprise or price it transparently.
- Freemium only works if the free tier is genuinely useful AND the paid upgrade is obviously better. A crippled free tier is worse than no free tier.
- Specific numbers build credibility: $47/mo reads more trustworthy than $50/mo. Use this deliberately — not on every price point, but on the hero tier.
- B2B + deal size above $200/mo → seat-based pricing is almost always correct.
- B2C + habit-forming product → monthly subscription is the priority structure. Annual is secondary.
- Price anchoring matters. The highest tier primes the customer to see the middle tier as reasonable. Design for that.

---

## Output Format

```markdown
## Pricing Strategy for [Company Name]

**Strategy type:** [SaaS Tiered / Consumer Tiered / Usage Tiers / Package / Freemium / Hybrid]
**Why this structure:** [2-3 sentences. Why this model, not another.]

---

### [Tier 1 Name]
- **Price:** $X/mo | $Y/yr (save Z%)
- **Who it's for:** [Specific customer segment — not "small businesses"]
- **What's included:** [Concrete feature list]
- **Price justification:** [Why this number. Anchored to what.]

### [Tier 2 Name]
- **Price:** $X/mo | $Y/yr (save Z%)
- **Who it's for:** [Specific segment]
- **What's included:** [Feature list — highlight what's new vs. Tier 1]
- **Price justification:** [Why this number]

### [Tier 3 Name]
[same structure]

---

### Positioning & Psychology
- **Market position:** [Where you sit vs. named competitors]
- **Psychological tactics:** [List each one used and the specific reason]
- **Upgrade triggers:** [What moves customers between tiers — specific, behavioral]

### Revenue Optimization
- [Specific recommendation 1]
- [Specific recommendation 2]
- [Specific recommendation 3]

### Biggest Pricing Risk
[One specific risk for this business. Not generic. How to see it coming and what to do.]
```

---

## Quality Checklist (Self-Verification)

### Pre-Execution Check
- [ ] I read FOUNDER_CONTEXT.md before asking any questions
- [ ] I only asked questions the context didn't already answer
- [ ] Total questions asked: 7 or fewer

### Strategy Check
- [ ] Strategy type is justified (not a generic default)
- [ ] Each tier has a clear reason to exist
- [ ] Middle tier is the obvious "best value" — the hero
- [ ] Price points are anchored to competitors, value, or willingness to pay — not guessed
- [ ] Annual pricing is 20-25% below monthly
- [ ] 4 tiers or fewer

### Pricing Principles Compliance
- [ ] All prices are value-based
- [ ] Freemium tier (if present) is genuinely useful, not crippled
- [ ] B2B high-value products use seat-based logic where appropriate
- [ ] Psychological tactics are named and justified

### Output Check
- [ ] Every tier has a price justification — none are bare numbers
- [ ] Positioning is specific to this business and its competitors
- [ ] Revenue optimization is actionable, not generic
- [ ] The "biggest risk" is specific to this business — not boilerplate

**If ANY check fails → revise before presenting.**

---

## Defaults & Assumptions

Use these unless the user overrides:

- **Pricing model:** Subscription (most common for modern products)
- **Tiers:** 3 for most businesses. 4 only if B2B with a clear Enterprise segment.
- **Annual discount:** 20%
- **Target gross margin:** 75-80% (SaaS baseline; adjust for non-software)
- **Price sensitivity:** Moderate (mid-market default)
- **Currency:** USD
- **Billing cycle:** Monthly with annual option

Document any assumptions made in the output.

## Scope and Limitations

- Covers pricing strategy design and analysis — value-based, cost-plus, competitive, and usage-based models. Does not cover billing system implementation, payment processing, or revenue recognition accounting
- Pricing recommendations are based on market patterns and economic principles; actual price elasticity and customer willingness-to-pay can only be validated through real-world testing
- Does not provide legal or regulatory guidance on pricing practices (price fixing, predatory pricing, geographic price discrimination laws)
- Financial projections built from pricing assumptions are directional, not guaranteed

