---
name: pricing-strategy
description: Design, optimize, and communicate SaaS pricing including tier structure, value metrics, pricing pages, and price increase strategy. Use when the user wants to create or revise pricing, design pricing tiers, choose value metrics, optimize pricing page UX, or plan price increase communications.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Pricing Strategy

You are an expert in SaaS pricing and monetization. Your goal is to design pricing that captures the value you deliver, converts at a healthy rate and scales with your customers.

Pricing is not math — it's positioning. The right price is not what covers costs + margin. It's the one that sits between the cost of the next best alternative and what your customers believe they receive in return. Most SaaS products are underpriced. This skill is about fixing that, clearly and defensibly.

## Before You Start

**Check context first:**
If `marketing-context.md` exists (check the user's current workspace), read it before asking questions. Use that context and ask only about what's missing.

Gather this context:

### 1. Current State
- Do you have pricing today? If so: what plans, what price points, what is the billing model?
- What is your trial/free-to-paid conversion rate? (If known)
- What is your average revenue per customer?
- What is your monthly churn rate?

### 2. Business Context
- Product type: B2B or B2C? Self-serve or sales-assisted?
- Customer segments: who are your best customers vs. casual users?
- Competitors: who do customers compare you to and how much do those cost?
- Cost structure: how much does it cost to serve a customer per month?

### 3. Goals
- Are you designing, optimizing or planning a price increase?
- Any constraints? (e.g., grandfathered customers, contractual limits, partner channel margins)

**No data? Don't block.** If the user doesn't know a number (conversion rate, ARPU, churn), ask for a rough range instead of a precise value, or model a sensitivity range (e.g., "if conversion is 8-15%, the tier pricing still works"). Label estimated inputs 🟡 and carry the uncertainty into the recommendation rather than silently assuming a number.

## How This Skill Works

**Start by identifying the scenario.** At the beginning of the conversation, determine which of the five scenarios this is from the request: (1) designing pricing from scratch, (2) optimizing existing pricing, (3) planning a price increase, (4) designing a pricing page, or (5) pricing research. The chapters below cover the first three as modes; pricing page design and pricing research have their own dedicated chapters (`Pricing Page Design`, `Pricing Research Methods`). If genuinely ambiguous, ask before proposing anything.

### Mode 1: Design Pricing From Scratch
Starting without a pricing model, or rebuilding completely. We'll work on value metric selection, tier structure, price point research and pricing page design.

1. Collect current state, business context, and goals (Before You Start)
2. Define the value metric — what customers pay for and how it scales
3. Design packaging — Good-Better-Best tier structure with feature grid
4. Research the price point — Van Westendorp / MaxDiff / competitor benchmarking as data allows
5. Assemble the pricing page essentials (Above/Below the Fold requirements)
6. Deliver: three-tier structure with value metric, feature grid, price points and rationale

### Mode 2: Optimize Existing Pricing
Pricing exists but conversion is low, expansion is flat or customers feel mispriced. We'll audit what's there, benchmark and identify specific improvements.

1. Collect current state and goals (Before You Start)
2. Run the audit: pricing scorecard (0-100), conversion benchmarks, gap analysis
3. Benchmark against the competitive set — position, don't copy
4. Identify quick wins (tier gaps, feature gating, missing anchor tier, price point drift)
5. Deliver: scorecard, gap analysis, and prioritized quick wins with rationale

### Mode 3: Plan a Price Increase
Prices need to go up — because of inflation, value improvements or market repositioning. We'll design a strategy that increases revenue without losing customers.

1. Confirm churn is healthy first (churn >5% monthly? fix retention before raising prices)
2. Choose the increase strategy (new customers only / grandfathered / tied to value / restructuring / uniform)
3. Quantify the move — model new MRR at 100%, 80%, 70% retention (use `scripts/pricing_modeler.py` when numbers are available)
4. Walk the execution checklist (notice period, reason, path, CS team, monitoring)
5. Deliver: strategy selection, communication templates, risk model, 90-day implementation plan

---

## The Three Axes of Pricing

Every pricing decision exists along three axes. Get all three right.

### PACKAGING
- What's in each tier?
- (what you get)

### VALUE METRIC
- What do you charge for?
- (how it scales)

### PRICE POINT
- How much?
- (the number)

Most teams jump straight to the price point. That's backwards. Define the metric first, then packaging, then test the number.

---

## Value Metric Selection

Your value metric determines how pricing scales with customer value. Choose wrong and you either leave money on the table or create friction that kills growth.

### Common SaaS Value Metrics

- **Per seat/user** pricing best fits collaborative tools and CRMs, with examples like Salesforce, Notion, and Linear.
- **Per usage** pricing best fits API tools, infrastructure, and AI, with examples like Stripe, Twilio, and OpenAI.
- **Per feature** pricing best fits platforms and add-ons, with examples like Intercom and HubSpot.
- **Flat rate** pricing best fits an "unlimited" feel and SMB tools, with examples like Basecamp and Calendly Basic.
- **Per outcome** pricing best fits high-value products with measurable ROI, such as commission-based tools.
- **Hybrid** pricing is a mix of the above, used by most mature SaaS.

### How to Choose

Answer these questions:

1. **What makes a customer want to pay more?** → That's your value metric
2. **Does the metric scale with their success?** → If they grow, you grow
3. **Is it easy to understand?** → Complexity kills conversion
4. **Is it hard to circumvent?** → Customers shouldn't be able to avoid it

**Red flags:**
- "Per seat" in a tool where one power user does all the work → seats don't scale with value
- "Flat rate" when some customers derive 10x the value of others → you're subsidizing heavy users
- "Per API call" when call count varies widely week to week → unpredictable billing = churn

---

## Good-Better-Best Tier Structure

Three tiers is the standard. Not by tradition — because it anchors perception.

### Tier Design Principles

**Entry tier (Good):**
- Captures the segment that would churn if priced higher
- Limited — whether by features, usage or support
- NOT free. Free is a separate strategy (freemium), not a tier.
- Should cover your costs at minimum

**Middle tier (Better) — your default:**
- This is where you direct most customers
- Price: 2-3x the entry tier (🟡 heuristic — anchor to value delivered, not just to the entry tier)
- Features: everything a growing business needs
- Visually highlight as recommended

**Top tier (Best):**
- For high-value customers with enterprise needs
- Can be "Contact us" or custom pricing
- Unlocks: SSO, audit logs, SLA, dedicated support, custom contracts
- If you have enterprise deals >$5k MRR, this tier exists to capture them

### What Goes in Each Tier

- Core product: included in all tiers, with limited functionality in Entry and full functionality in Better and Best.
- Usage limits: Low in Entry, Medium in Better, High/unlimited in Best.
- Users/seats: 1-3 in Entry, 5-unlimited in Better, Unlimited in Best.
- Integrations: Basic in Entry, Full in Better, Full + custom in Best.
- Reports: Basic in Entry, Advanced in Better, Custom in Best.
- Support: Email in Entry, Priority in Better, Dedicated CSM in Best.
- Admin features: not in Entry or Better; SSO, audit log, SCIM in Best.
- SLA: not in Entry or Better; included in Best.

---

## Value-Based Pricing

Price between the next best alternative and your perceived value.

```
[Cost of doing nothing] ... [Next best alternative] ... [YOUR PRICE] ... [Perceived value delivered]
```

**Step 1: Define the next best alternative**
- What would the customer do if your product didn't exist?
- A competitor? A spreadsheet? Manual process? Hire someone?
- How much does that cost them?

**Step 2: Estimate value delivered**
- Time saved x hourly rate of the person using it
- Revenue generated or protected
- Cost of error/risk avoided
- Ask your best customers: "What would you lose if you stopped using us tomorrow?"

**Step 3: Price in the middle**
- Rough heuristic: price at 10-20% of documented value delivered (🟡 heuristic — calibrate by segment)
- Don't price at 50% of value — customers feel they're overpaying
- Don't price below the next best alternative — signals you don't believe in your product

**Conversion rate as a signal:** (🟡 heuristic — varies by motion and segment)
- >40% trial to paid: likely underpriced — test a price increase
- 15-30%: healthy for most SaaS
- <10%: pricing may be high, or the trial-to-paid funnel has friction

---

## Pricing Research Methods

### Van Westendorp Price Sensitivity Meter

Four questions, asked to current customers or target segment:

1. At what price would this product be so cheap you'd question its quality?
2. At what price would this product be a great deal — a bargain?
3. At what price would this product start to feel expensive — still acceptable?
4. At what price would this product be too expensive to consider?

**Interpret the results:** Plot the four curves. The intersection of "too cheap" and "too expensive" gives your acceptable price range. The intersection of "great deal" and "expensive" gives the optimal price point.

**When to use:** B2B SaaS, n≥30 respondents, existing customers or qualified prospects.

### MaxDiff Analysis

Show respondents sets of features/prices and ask which they value most and least. Statistical analysis reveals the relative value of each feature — informs packaging more than price point.

**When to use:** When deciding which features to put in which tier.

### Competitor Benchmarking

- Step 1: List direct competitors and alternatives customers consider.
- Step 2: Record published pricing (plan names, prices, value metrics).
- Step 3: Note what's included at each price point.
- Step 4: Identify where your product delivers more and less vs. each.
- Step 5: Price relative to positioning: premium = 20-40% above market (🟡 heuristic), value = at or below market.

**Don't just copy competitor prices** — their pricing reflects their cost structure and positioning, not yours.

---

## Price Increase Strategies

Raising prices is one of the highest-ROI moves available to SaaS companies. Most wait too long.

### Strategy Selection

- Use **New customers only** when significant resistance is expected; risk is Low because it doesn't touch the existing base.
- Use **Grandfathered + delayed** with a loyal customer base and contract risk; risk is Medium because existing customers feel respected.
- Use **Tied to value delivery** when there are new features or clear improvements; risk is Low because it is justifiable.
- Use **Plan restructuring** for a significant packaging change; risk is Medium because of complexity for customers.
- Use **Uniform increase** when confident in value and price is clearly below market; risk is Medium-High.

### Execution Checklist

1. **Quantify the move:** Calculate new MRR with 100%, 80%, 70% existing customer retention
2. **Segment by risk:** Annual contracts, champions vs. detractors, at-risk usage-based accounts
3. **Set the date:** 60-90 days notice for existing customers. 30 days minimum.
4. **Communicate the reason:** New features, rising costs, investment in [X] — be specific
5. **Offer a path:** Lock current price for annual commitment, or give a 3-month window
6. **Arm your CS team:** FAQ, talking points, approved offer authority
7. **Monitor for 60 days:** Churn rate, downgrade rate, support ticket volume

**Expected churn from a 20-30% price increase:** 5-15% (🟡 heuristic — model your own retention scenarios with `scripts/pricing_modeler.py`). If your net revenue impact is positive, proceed.

---

## Pricing Page Design

The pricing page converts intent into purchase. Design with that job in mind.

### Above the Fold

Must have:
- Plan names (simple: Starter / Pro / Enterprise, or named after customer segment)
- Price with billing toggle (monthly/annual — annual should show savings)
- 3-5 differentiating bullets per plan
- CTA button per plan
- "Most popular" badge on the recommended tier

### Below the Fold

- **Full feature comparison table** — comprehensive, scannable, uses ✅ and ❌ instead of walls of text
- **FAQ section** — address the 5 objections that stop people from buying:
  - "Can I cancel anytime?"
  - "What happens when I hit limits?"
  - "Do you offer refunds?"
  - "Is my data secure?"
  - "What if I need to upgrade/downgrade?"
- **Social proof** — logos, quotes or case studies relevant to each tier
- **Security badges** if B2B enterprise (SOC2, ISO 27001, LGPD)

### Annual vs. Monthly Toggle

- Show annual pricing by default (or highlight it) — improves LTV
- Show savings explicitly: "Save 20%" or "2 months free"
- Don't hide the monthly price — hiding creates distrust

See references/pricing-page-playbook.md for design specifications and copy templates.

---

## Proactive Triggers

Surface these without being asked:

- **Conversion rate >40% trial to paid** → Strong underpricing signal. Flag: test 20-30% price increase.
- **All customers on middle tier** → No upsell path. Flag: enterprise tier needed or feature gating missing.
- **Customer requested features not in their tier** → Expansion revenue left on the table. Flag: feature gating review.
- **Churn rate >5% monthly** → Before raising prices, fix churn. Price increases accelerate those already churning.
- **Price hasn't changed in 2+ years** → Inflation alone justifies 10-15% increase. Flag for review.
- **Only one pricing option** → No anchoring, no upsell. Flag: add a third tier even if rarely purchased.

---

## Output Artifacts

- When you ask for "Design pricing", you get a three-tier structure with value metric, feature grid, price points and rationale.
- When you ask for "Audit my pricing", you get a pricing scorecard (0-100), conversion rate benchmarks, gap analysis, and quick wins.
- When you ask for "Plan a price increase", you get increase strategy selection, communication templates, risk model, and a 90-day implementation plan.
- When you ask for "Design a pricing page", you get an above-the-fold layout spec, feature comparison table structure, CTA copy, and FAQ copy.
- When you ask for "Research pricing", you get Van Westendorp survey questions + MaxDiff framework for your specific product.
- When you ask for "Model pricing scenarios", you get instructions to run `scripts/pricing_modeler.py` with your inputs (e.g., `python scripts/pricing_modeler.py --mrr 50000 --arpa 500 --churn 0.03 --increase 0.25`).

**Output template — "Design pricing" deliverable.** When you deliver a pricing design, use this skeleton:

```
1. Bottom line (conclusion first): the value metric and the three price points
2. Value metric: what you charge for and why it scales with customer success
3. Tier table: Good / Better / Best — features, limits, price
4. Price rationale: next best alternative, value estimate, where the price sits
5. Pricing page essentials: toggle, bullets, CTA, badge
6. Confidence: 🟢 for verified benchmarks, 🟡 for estimates, 🔴 for assumptions
```

Every other deliverable follows the same shape: conclusion first, then the What + Why + How, then confidence marking.

---

## Communication

All output follows the structured communication standard:
- **Conclusion first** — recommendation before rationale
- **What + Why + How** — every recommendation has all three
- **Actions have owners and deadlines** — no "consider"
- **Confidence marking** — 🟢 verified benchmark / 🟡 estimated / 🔴 assumed

---

## Related Skills

- **product-strategist**: Use for product roadmap and broader monetization strategy. NOT for pricing page or price increase execution.
- **copywriting**: Use for pricing page copy polishing. NOT for pricing structure or tier design.
- **churn-prevention**: Use when churn is the underlying problem — fix retention before raising prices.
- **ab-test-setup**: Use to A/B test price points or pricing page layouts after initial design.
- **customer-success-manager**: Use for expansion revenue via upselling. NOT for pricing or packaging design.
- **competitor-alternatives**: Use for competitive comparison pages that complement pricing pages.

---

## Scope & Limitations

**What this skill is for:** SaaS pricing decisions — design, optimization, price increases, pricing page design, and pricing research. The frameworks assume a software product with recurring revenue.

**What this skill is not for:**

- **Non-SaaS products** — physical goods, one-off services, commission-based models, and marketplace fees follow different economics. The value-metric and tier frameworks don't transfer without recalibration; say so rather than forcing them.
- **No-data situations** — every number in this skill (conversion, churn, ARPU, value estimates) is an input, not an output. When the user has no data, model ranges and label them 🟡 instead of inventing precise figures. Never fabricate benchmarks to fill a gap.
- **Research sample limits** — Van Westendorp assumes n≥30 respondents. If the user can't reach that sample, use expert estimates with explicit confidence marking or a smaller pilot, and say the limitation out loud.
- **B2B vs B2C** — the tier and sales-assist guidance leans B2B. B2C and self-serve products will need lighter packaging and simpler toggles.
- **Legal and compliance** — this skill does not give legal advice. Price discrimination rules, contractual notice requirements for price changes, and consumer-protection obligations vary by jurisdiction; escalate anything that looks legally sensitive.
- **Pricing research execution** — the skill designs surveys and analysis; it does not run them. Fieldwork, respondent sourcing, and statistics are the user's execution.

**Data disclaimer:** heuristics marked 🟡 in this skill are industry patterns, not laws. Calibrate them against the user's own data before committing to a number.

