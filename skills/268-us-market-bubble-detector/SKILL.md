---
name: us-market-bubble-detector
description: Evaluates market bubble risk through quantitative data-driven analysis using the revised Minsky/Kindleberger framework v2.1. Prioritizes objective metrics (Put/Call, VIX, margin debt, breadth, IPO data) over subjective impressions. Features strict qualitative adjustment criteria with confirmation bias prevention. Supports practical investment decisions with mandatory data collection and mechanical scoring. Use when user asks about bubble risk, valuation concerns, or profit-taking timing.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Us Market Bubble Detector


## Key Revisions in v2.1

**Critical Changes from v2.0:**
1. ✅ **Mandatory Quantitative Data Collection** - Use measured values, not impressions or speculation
2. ✅ **Clear Threshold Settings** - Specific numerical criteria for each indicator
3. ✅ **Two-Phase Evaluation Process** - Quantitative evaluation → Qualitative adjustment (strict order)
4. ✅ **Stricter Qualitative Criteria** - Max +3 points (reduced from +5), requires measurable evidence
5. ✅ **Confirmation Bias Prevention** - Explicit checklist to avoid over-scoring
6. ✅ **Granular Risk Phases** - Added "Elevated Risk" phase (8-9 points) for nuanced risk management

---


## When to Use This Skill

Use this skill when:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions

**Japanese:**
- User asks "Is the current market a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User observes social phenomena (non-investors entering, media frenzy, IPO flood) and expresses concern
- User reports situations where narratives like "this time is different" or "revolutionary technology" are becoming mainstream
- User consults about risk management for existing positions

---


## Evaluation Process (Strict Order)

### Phase 1: Mandatory Quantitative Data Collection

**CRITICAL: Always collect the following data before starting evaluation**

#### 1.1 Market Structure Data (Highest Priority)
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: web_search "CBOE put call ratio" or the CBOE public options data page
    (CBOE DataShop requires an account and API access; use public pages instead)
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value (the 3-month percentile is context only, not used in scoring)

□ Price Acceleration (Indicator 6)
  - Source: historical index closing prices (e.g., Yahoo Finance full price history
    for ^GSPC) or web_search "S&P 500 3 month return vs 10 year average"
  - Collect: past 3-month return of the major index
  - Compute: percentile of that return within the past 10 years of 3-month rolling
    returns (use monthly closes; 3-month returns, not annualized)
```

#### 1.2 Leverage & Positioning Data
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO & New Issuance Data
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ CRITICAL: Do NOT proceed with evaluation without Phase 1 data collection**

**If a specific data point cannot be obtained:** record it as "unavailable" with the
reason, score the affected indicator conservatively (qualitative adjustments score
+0 without measured evidence), and state the gap explicitly in the report. Do not
guess or estimate values.

---

### Phase 2: Quantitative Evaluation (Quantitative Scoring)

Score mechanically based on collected data using the following criteria:

#### Indicator 1: Put/Call Ratio (Market Sentiment)
```
Scoring Criteria:
- 2 points: P/C < 0.70 (excessive optimism, call-heavy)
- 1 point: 0.70 ≤ P/C ≤ 0.85 (slightly optimistic)
- 0 points: P/C > 0.85 (healthy caution)

Rationale: P/C < 0.7 is historically characteristic of bubble periods
```

#### Indicator 2: Volatility Suppression + New Highs
```
Scoring Criteria:
- 2 points: VIX < 12 AND major index within 5% of 52-week high
- 1 point: VIX 12-15 AND index within 10% of 52-week high, OR VIX < 12 AND index
  more than 5% from 52-week high
- 0 points: VIX > 15 OR index more than 10% from 52-week high

Rationale: Extreme low volatility + highs indicates excessive complacency
```

#### Indicator 3: Leverage (Margin Debt Balance)
```
Scoring Criteria:
- 2 points: YoY +20% or more AND new all-time high
- 1 point: YoY above +10% up to +20%, OR YoY +20% or more without a new all-time high
- 0 points: YoY +10% or less OR negative

Rationale: Rapid leverage increase is a bubble precursor
```

#### Indicator 4: IPO Market Overheating
```
Scoring Criteria:
- 2 points: Quarterly IPO count > 2x 5-year average AND median first-day return +20%+
- 1 point: Quarterly IPO count > 1.5x 5-year average
- 0 points: Normal levels

Rationale: Poor-quality IPO flood is characteristic of late-stage bubbles
```

#### Indicator 5: Breadth Anomaly (Narrow Leadership)
```
Scoring Criteria:
- 2 points: New high AND < 45% of stocks above 50DMA (narrow leadership)
- 1 point: 45% ≤ breadth ≤ 60% above 50DMA (somewhat narrow)
- 0 points: breadth > 60% above 50DMA (healthy breadth)

Rationale: Rally driven by few stocks is fragile
```

#### Indicator 6: Price Acceleration
```
Scoring Criteria:
- 2 points: Past 3-month return exceeds the 95th percentile of the past 10 years
- 1 point: Past 3-month return in the 85th-95th percentile (both inclusive)
- 0 points: Below the 85th percentile

Rationale: Rapid price acceleration is unsustainable
```

---

### Phase 3: Qualitative Adjustment (REVISED v2.1)

**Limit: +3 points maximum (REDUCED from +5 in v2.0)**

**⚠️ CONFIRMATION BIAS PREVENTION CHECKLIST:**
```
Before adding ANY qualitative points:
□ Do I have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Am I avoiding double-counting with Phase 2 scores?
□ Have I documented specific evidence with sources?
```

#### Adjustment A: Social Penetration (0-1 points, STRICT CRITERIA)
```
+1 point: ALL THREE criteria must be met:
  ✓ Direct user report of non-investor recommendations
  ✓ Specific examples with names/dates/conversations
  ✓ Multiple independent sources (minimum 3)

+0 points: Any criteria missing

⚠️ INVALID EXAMPLES:
- "AI narrative is prevalent" (unmeasurable)
- "I saw articles about retail investors" (not direct report)
- "Everyone is talking about stocks" (vague, unverified)

✅ VALID EXAMPLE:
"My barber asked about NVDA (Nov 1), dentist mentioned AI stocks (Nov 2),
Uber driver discussed crypto (Nov 3)"
```

#### Adjustment B: Media/Search Trends (0-1 points, REQUIRES MEASUREMENT)
```
+1 point: BOTH criteria must be met:
  ✓ Google Trends showing 5x+ YoY increase (measured)
  ✓ Mainstream coverage confirmed (Time covers, TV specials with dates)

+0 points: Search trends <5x OR no mainstream coverage

⚠️ CRITICAL: "Elevated narrative" without data = +0 points

HOW TO VERIFY:
1. Search "[topic] Google Trends" and document numbers
2. Search "[topic] Time magazine cover" for specific dates
3. Search "[topic] CNBC special" for episode confirmation

Google Trends reports a 0-100 relative search index, not absolute volumes.
Record the ratio of the current value to the same period one year ago, using the
same topic and the same comparison window.

✅ VALID EXAMPLE:
"Google Trends: 'AI stocks' current index 100 vs 19 one year ago (5.2x).
Time cover 'AI Revolution' (Oct 15, 2025).
CNBC 'AI Investment Special' (3 episodes Oct 2025)."

⚠️ INVALID EXAMPLE:
"AI/technology narrative seems elevated" (unmeasurable)
```

#### Adjustment C: Valuation Disconnect (0-1 points, AVOID DOUBLE-COUNTING)
```
+1 point: ALL criteria must be met:
  ✓ P/E >25 (P/E is not part of Phase 2 scoring, so there is nothing to double-count;
    verify narrative dependence instead)
  ✓ Fundamentals explicitly ignored in mainstream discourse
  ✓ "This time is different" documented in major media

+0 points: P/E <25 OR fundamentals support valuations

⚠️ SELF-CHECK QUESTIONS (if ANY is YES, score = 0):
- Is P/E already in Phase 2 quantitative scoring?
- Do companies have real earnings supporting valuations?
- Is the narrative backed by fundamental improvements?

✅ VALID EXAMPLE for +1:
"S&P P/E = 35x (vs historical 18x).
CNBC article: 'Earnings don't matter in AI era' (Oct 2025).
Bloomberg: 'Traditional metrics obsolete' (Nov 2025)."

⚠️ INVALID EXAMPLE:
"P/E 30.8 but companies have real earnings and AI has fundamental backing"
(fundamentals support = +0 points)
```

**Phase 3 Total: Maximum +3 points**

---

### Phase 4: Final Judgment (REVISED v2.1)

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (0 to +3 points)
Range: 0 to 15 points

Judgment Criteria (with Risk Budget):
- 0-4 points: Normal (Risk Budget: 100%)
- 5-7 points: Caution (Risk Budget: 70-80%)
- 8-9 points: Elevated Risk (Risk Budget: 50-70%) ⚠️ NEW in v2.1
- 10-12 points: Euphoria (Risk Budget: 40-50%)
- 13-15 points: Critical (Risk Budget: 20-30%)
```

**Boundary rule:** when a score or measured value falls exactly on a boundary
between two phases or two score levels, take the lower (more conservative) level.

**Key Change in v2.1:**
- Added "Elevated Risk" phase (8-9 points) for more nuanced positioning
- 9 points is no longer extreme defensive zone (was 40% risk budget)
- Now allows 50-70% risk budget at 8-9 point level
- More gradual transition from Caution to Euphoria phases

---


## Data Sources (Required)

### US Market
- **Put/Call**: https://www.cboe.com/tradable_products/vix/
- **VIX**: Yahoo Finance (^VIX) or https://www.cboe.com/
- **Margin Debt**: https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **Breadth**: https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**: https://www.renaissancecapital.com/IPO-Center/Stats

### Japanese Market
- **Nikkei Futures P/C**: https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**: https://www.investing.com/indices/nikkei-volatility-historical-data
- **Margin Debt**: JSF (Japan Securities Finance) Monthly Report
- **Breadth**: https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**: https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---


## Scope and Limitations

- **Markets covered:** U.S. large-cap indices (S&P 500, NASDAQ, and related
  breadth data) and, via the data sources above, Japanese large-cap indices
  (Nikkei 225, TOPIX). The Phase 2 thresholds are calibrated for U.S. market
  data. When applying them to Japanese data, state the differences in the
  report (for example, Nikkei futures P/C normal levels differ from U.S.
  equity P/C), or restrict the evaluation to the U.S. market.
- **Not covered:** single-stock timing, bonds, commodities, and crypto assets.
  The historical crypto cases are reference material only; the Phase 2
  indicator set is not adapted to crypto market data.
- **Data freshness:** this skill depends on external data. Monthly series
  (FINRA margin debt) are published with a lag of roughly three weeks; IPO
  counts are quarterly. Use the most recent published values and record the
  publication date in the report.
- **Not investment advice:** short-selling and position recommendations in the
  output are framework outputs based on the composite conditions, not
  independent investment advice. Final decisions rest with the user.
- **When not to use this skill:** when the user wants a quick opinion without
  data collection, or when the evaluation would have to rely purely on
  impressions without verifiable data.

---


## Implementation Checklist

Verify the following when using:

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +3 point limit?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---


## Important Principles (Revised)

### 1. Data > Impressions
Ignore "many news reports" or "experts are cautious" without quantitative data.

### 2. Strict Order: Quantitative → Qualitative
Always evaluate in this order: Phase 1 (Data Collection) → Phase 2 (Quantitative) → Phase 3 (Qualitative Adjustment).

### 3. Upper Limit on Subjective Indicators
Qualitative adjustment has a total limit of +3 points. It cannot override quantitative evaluation.

### 4. "Taxi Driver" is Symbolic
Do not readily acknowledge mass penetration without direct recommendations from non-investors.

---


## Common Failures and Solutions (Revised)

### Failure 1: Evaluating Based on News Articles
❌ "Many reports on Takaichi Trade" → Media saturation 2 points
✅ Verify Google Trends numbers → Evaluate with measured values

### Failure 2: Overreaction to Expert Comments
❌ "Warning of overheating" → Euphoria zone
✅ Judge with measured values of Put/Call, VIX, margin debt

### Failure 3: Emotional Reaction to Price Rise
❌ 4.5% rise in 1 day → Price acceleration 2 points
✅ Verify position in 10-year distribution → Objective evaluation

### Failure 4: Judgment Based on Valuation Alone
❌ P/E 35 → Valuation disconnect +1 point (without checking narrative dependence)
✅ Check P/E > 25 AND fundamentals actively ignored in mainstream discourse
before awarding the point

---


## Recommended Actions by Bubble Stage (REVISED v2.1)

### Normal (0-4 points)
**Risk Budget: 100%**
- Continue normal investment strategy
- Set ATR 2.0× trailing stop
- Apply stair-step profit-taking rule (+20% take 25%)

**Short-Selling: Not Allowed**
- Composite conditions not met (0/7 items)

### Caution (5-7 points)
**Risk Budget: 70-80%**
- Begin partial profit-taking (20-30% reduction)
- Tighten ATR to 1.8×
- Reduce new position sizing by 50%

**Short-Selling: Not Recommended**
- Wait for clearer reversal signals

### Elevated Risk (8-9 points) ⚠️ NEW in v2.1
**Risk Budget: 50-70%**
- Increase profit-taking (30-50% reduction)
- Tighten ATR to 1.6×
- New positions: highly selective, quality only
- Begin building cash reserves for future opportunities

**Short-Selling: Consider Cautiously**
- Only after confirming at least 2/7 composite conditions
- Small exploratory positions (10-15% of normal size)
- Strict stop-loss (ATR 2.0×)

**Rationale for NEW phase:**
This zone represents heightened caution without extreme defensiveness.
Market shows warning signs but not imminent collapse.
Maintain exposure to quality positions while building flexibility.

### Euphoria (10-12 points)
**Risk Budget: 40-50%**
- Accelerate stair-step profit-taking (50-60% reduction)
- Tighten ATR to 1.5×
- No new long positions except on major pullbacks

**Short-Selling: Active Consideration**
- After confirming at least 3/7 composite conditions
- Small positions (20-25% of normal size)
- Defined risk only (options, tight stops)

### Critical (13-15 points)
**Risk Budget: 20-30%**
- Major profit-taking or full hedge implementation
- ATR 1.2× or fixed stop-loss
- Cash preservation mode - prepare for major dislocation

**Short-Selling: Recommended**
- After confirming at least 5/7 composite conditions
- Scale in with small positions, pyramid on confirmation
- Tight stop-loss (ATR 1.5× or higher)
- Consider put options for defined risk

---


## Composite Conditions for Short-Selling (7 Items)

Only consider shorts after the phase-specific minimum number of conditions below
is met:

```
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicators drop sharply (margin debt decline)
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges (+30% or more)
7. Fed/policy shift signals
```

**Minimum conditions by phase (matches "Recommended Actions by Bubble Stage"):**

- In the Normal phase (composite score 0-4, minimum conditions met: 0/7), short-selling is not allowed.
- In the Caution phase (composite score 5-7, minimum conditions met: 2/7), short-selling is not recommended; wait for clearer signals.
- In the Elevated Risk phase (composite score 8-9, minimum conditions met: 2/7), short-selling may be considered cautiously.
- In the Euphoria phase (composite score 10-12, minimum conditions met: 3/7), short-selling is under active consideration.
- In the Critical phase (composite score 13-15, minimum conditions met: 5/7), short-selling is recommended.

---


## Output Format

### Evaluation Report Structure (v2.1)

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.1)


## Overall Assessment
- Final Score: X/15 points
- Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical]
- Risk Level: [Low/Medium/Medium-High/High/Extremely High]
- Evaluation Date: YYYY-MM-DD


## Quantitative Evaluation (Phase 2)

- For the Put/Call indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.
- For the VIX + Highs indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.
- For the Margin YoY indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.
- For the IPO Heat indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.
- For the Breadth indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.
- For the Price Accel indicator, record the measured [value], assign a score of [0-2], and note the [reason] as the rationale.

**Phase 2 Total: X/12 points**


## Qualitative Adjustment (Phase 3) - STRICT CRITERIA

**⚠️ Confirmation Bias Check:**
- [ ] All qualitative points have measurable evidence
- [ ] No double-counting with Phase 2
- [ ] Independent observer would agree

### A. Social Penetration (0-1 points)
- Evidence: [REQUIRED: Direct user reports with dates/names]
- Score: [+0 or +1]
- Justification: [Must meet ALL three criteria]

### B. Media/Search Trends (0-1 points)
- Google Trends Data: [REQUIRED: Measured numbers, YoY multiplier]
- Mainstream Coverage: [REQUIRED: Specific Time covers, TV specials with dates]
- Score: [+0 or +1]
- Justification: [Must have 5x+ search AND mainstream confirmation]

### C. Valuation Disconnect (0-1 points)
- P/E Ratio: [Current value]
- Fundamental Backing: [Yes/No - if Yes, score = 0]
- Narrative Analysis: [REQUIRED: Specific media quotes ignoring fundamentals]
- Score: [+0 or +1]
- Justification: [Must show fundamentals actively ignored]

**Phase 3 Total: +X/3 points (max reduced from +5 in v2.0)**


## Recommended Actions

**Risk Budget: X%** (Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical])
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Short-Selling: [Not Allowed/Consider Cautiously/Active/Recommended]**
- Composite conditions: X/7 met
- Minimum required: [0/2/3/5] for current phase


## Key Changes in v2.1
- Stricter qualitative criteria (max +3, down from +5)
- Added "Elevated Risk" phase for 8-9 points
- Confirmation bias prevention checklist
- All qualitative points require measurable evidence
```

---


## Reference Files

- **Reference Documents**: see [references/reference-documents.md](references/reference-documents.md)
- **Summary Essence Of V2 1 Revision**: see [references/summary-essence-of-v2-1-revision.md](references/summary-essence-of-v2-1-revision.md)

