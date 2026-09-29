---
name: social-media-analyzer
description: Social media campaign analysis and performance tracking. Calculates engagement rates, ROI, and cross-platform benchmarks. Use to analyze social media performance, calculate engagement rate, measure campaign ROI, compare platform metrics, or benchmark engagement against industry standards. Use when the user asks to analyze social media campaign performance, calculate engagement rates or ROI, compare platforms (Instagram, Facebook, TikTok, LinkedIn, Twitter), or benchmark engagement.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Social Media Analyzer

Campaign performance analysis with engagement metrics, ROI calculations, and platform benchmarks.

---

## Summary

- [Analysis Workflow](#analysis-workflow)
- [Engagement Metrics](#engagement-metrics)
- [ROI Calculation](#roi-calculation)
- [Platform Benchmarks](#platform-benchmarks)
- [Tools](#tools)
- [Examples](#examples)

---

## Analysis Workflow

Analyze social media campaign performance:

1. Validate input data completeness (reach > 0, valid dates)
2. Calculate engagement metrics per post
3. Aggregate metrics at the campaign level
4. Calculate ROI if ad spend provided
5. Compare against platform benchmarks
6. Identify top and bottom performers
7. Generate recommendations
8. **Validation:** Engagement rate < 100%, ROI matches spend data

### Input Requirements

- `platform` is required and must be one of: instagram, facebook, twitter, linkedin, tiktok.
- `posts[]` is required and is the array of post data.
- `posts[].likes` is required and is the likes/reactions count.
- `posts[].comments` is required and is the comments count.
- `posts[].reach` is required and is the unique users reached.
- `posts[].impressions` is optional and is the total views.
- `posts[].shares` is optional and is the shares/retweets count.
- `posts[].saves` is optional and is the saves/bookmarks count.
- `posts[].clicks` is optional and is the link clicks.
- `total_spend` is optional and is the ad spend (for ROI).

### Data Validation Checks

Before analysis, verify:

- [ ] Reach > 0 for all posts (avoid division by zero)
- [ ] Engagement counts are non-negative
- [ ] Date range is valid (start < end)
- [ ] Platform is recognized
- [ ] Spend > 0 if ROI requested

---

## Engagement Metrics

### Engagement Rate Calculation

```
Engagement Rate = (Likes + Comments + Shares + Saves) / Reach × 100
```

### Metric Definitions

- Engagement Rate = Engagements / Reach × 100; it measures the audience interaction level.
- CTR = Clicks / Impressions × 100; it measures the content click appeal.
- Reach Rate = Reach / Followers × 100; it measures the content distribution.
- Virality Rate = Shares / Impressions × 100; it measures the shareability.
- Save Rate = Saves / Reach × 100; it measures the content value.

### Performance Categories

- An Engagement Rate > 6% is rated Excellent: scale and replicate.
- An Engagement Rate of 3-6% is rated Good: optimize and expand.
- An Engagement Rate of 1-3% is rated Average: test improvements.
- An Engagement Rate < 1% is rated Poor: analyze and pivot.

---

## ROI Calculation

Calculate return on ad spend:

1. Sum total engagements across posts
2. Calculate cost per engagement (CPE)
3. Calculate cost per click (CPC) if clicks available
4. Estimate engagement value using benchmark rates
5. Calculate ROI percentage
6. **Validation:** ROI = (Value - Spend) / Spend × 100

### ROI Formulas

- Cost Per Engagement (CPE) = Total Spend / Total Engagements.
- Cost Per Click (CPC) = Total Spend / Total Clicks.
- Cost Per Mille (CPM) = (Spend / Impressions) × 1000.
- Return on Ad Spend (ROAS) = Revenue / Ad Spend.

### Engagement Value Estimates

- A Like is valued at $2.50 for brand awareness.
- A Comment is valued at $10.00 for active engagement.
- A Share is valued at $25.00 for amplification.
- A Save is valued at $15.00 as an intent signal.
- A Click is valued at $7.50 for traffic value.

### ROI Interpretation

- An ROI > 500% is rated Excellent: scale budget significantly.
- An ROI of 200-500% is rated Good: increase budget moderately.
- An ROI of 100-200% is rated Acceptable: optimize before scaling.
- An ROI of 0-100% is rated Break-even: review targeting and creative.
- An ROI < 0% is rated Negative: pause and restructure.

---

## Platform Benchmarks

### Engagement Rate by Platform

- Instagram: average engagement rate 1.22%, good 3-6%, excellent >6%.
- Facebook: average engagement rate 0.07%, good 0.5-1%, excellent >1%.
- Twitter/X: average engagement rate 0.05%, good 0.1-0.5%, excellent >0.5%.
- LinkedIn: average engagement rate 2.0%, good 3-5%, excellent >5%.
- TikTok: average engagement rate 5.96%, good 8-15%, excellent >15%.

### CTR by Platform

- Instagram: average CTR 0.22%, good 0.5-1%, excellent >1%.
- Facebook: average CTR 0.90%, good 1.5-2.5%, excellent >2.5%.
- LinkedIn: average CTR 0.44%, good 1-2%, excellent >2%.
- TikTok: average CTR 0.30%, good 0.5-1%, excellent >1%.

### CPC by Platform

- Facebook: average CPC $4.85, good <$2.50.
- Instagram: average CPC $6.00, good <$3.50.
- LinkedIn: average CPC $26.30, good <$15.00.
- TikTok: average CPC $5.00, good <$2.50.

See `references/platform-benchmarks.md` for full benchmark data.

---

## Tools

### Calculate Metrics

```bash
python scripts/calculate_metrics.py assets/sample_input.json
```

Calculates engagement rate, CTR, reach rate for each post and campaign totals.

### Analyze Performance

```bash
python scripts/analyze_performance.py assets/sample_input.json
```

Generates full performance analysis with ROI, benchmarks, and recommendations.

**Output includes:**
- Campaign-level metrics
- Post-by-post breakdown
- Benchmark comparisons
- Ranked top performers
- Actionable recommendations

---

## Examples

### Example Input

See `assets/sample_input.json`:

```json
{
  "platform": "instagram",
  "total_spend": 2500,
  "posts": [
    {
      "post_id": "post_001",
      "content_type": "image",
      "likes": 342,
      "comments": 28,
      "shares": 15,
      "saves": 45,
      "reach": 5200,
      "impressions": 8500,
      "clicks": 120
    }
  ]
}
```

### Example Output

See `assets/expected_output.json`:

```json
{
  "campaign_metrics": {
    "total_engagements": 1521,
    "avg_engagement_rate": 8.36,
    "ctr": 1.55
  },
  "roi_metrics": {
    "total_spend": 2500.0,
    "cost_per_engagement": 1.64,
    "roi_percentage": 660.5
  },
  "insights": {
    "overall_health": "excellent",
    "benchmark_comparison": {
      "engagement_status": "excellent",
      "engagement_benchmark": "1.22%",
      "engagement_actual": "8.36%"
    }
  }
}
```

### Interpretation

The example campaign shows:
- **Engagement rate 8.36%** vs 1.22% benchmark = Excellent (6.8x above average)
- **CTR 1.55%** vs 0.22% benchmark = Excellent (7x above average)
- **ROI 660%** = Exceptional return on $2,500 spend
- **Recommendation:** Scale the budget, replicate successful elements

---

## Reference Documentation

### Platform Benchmarks

`references/platform-benchmarks.md` contains:

- Engagement rate benchmarks by platform and industry
- CTR benchmarks for organic and paid content
- Cost benchmarks (CPC, CPM, CPE)
- Content type performance by platform
- Optimal posting times and frequencies
- ROI calculation formulas

## Proactive Triggers

- **Engagement rate below platform average** → Content is not resonating. Analyze top performers for patterns.
- **Stagnant follower growth** → Distribution or content frequency issue. Audit posting patterns.
- **High impressions, low engagement** → Reach without resonance. Content quality issue.
- **Competitor significantly outperforming** → Content gap. Analyze their successful posts.

## Output Artifacts

- When you ask for a "Social media audit", you get a cross-platform performance analysis with benchmarks.
- When you ask "What's performing?", you get top content analysis with patterns and recommendations.
- When you ask for "Competitor social analysis", you get a competitive social media comparison with gaps.

## Communication

All output goes through quality verification:
- Self-validation: source attribution, assumption audit, confidence scoring
- Output format: Conclusion → What (with confidence) → Why → How to Act
- Results only. Every finding marked: 🟢 verified, 🟡 medium, 🔴 assumed.

## Related Skills

- **social-content**: For creating social posts. Use this skill to analyze performance.
- **campaign-analytics**: For multi-channel analytics including social.
- **content-strategy**: For planning social content themes.
- **marketing-context**: Provides audience context for better analysis.

---

## Scope and Limitations

- Analyzes quantitative campaign performance for the five supported platforms (instagram, facebook, twitter, linkedin, tiktok) — it does not create content or write posts (use social-content) and does not plan multi-channel strategy (use campaign-analytics).
- Requires structured post-level input data (at minimum platform, likes, comments, reach); engagement rates, CTR, and ROI cannot be computed — or validated — from missing, estimated, or aggregated inputs.
- Benchmarks are industry averages that drift over time and vary by vertical and content type; they are directional references, not guarantees, and platform metric definitions can change.
- ROI figures are estimates built on per-action value assumptions ($ per like/comment/share/save/click); they inform prioritization but are not financial accounting — revenue attribution beyond clicks must come from the user.
- Does not cover qualitative analysis: sentiment, brand health, follower demographics, competitive listening, or influencer identification.

## Output Format

Deliverables of an analysis run:

- **Campaign-level metrics**: total engagements, average engagement rate, CTR, reach rate, virality rate, and save rate, each with the formula used.
- **ROI block** when `total_spend` is provided: CPE, CPC, CPM, and ROI % — or explicitly marked as not computed when spend is missing (never silently dropped).
- **Benchmark comparison**: actual vs platform average/good/excellent for engagement and CTR, with per-finding confidence tags (🟢 verified / 🟡 medium / 🔴 assumed).
- **Post-by-post breakdown** with ranked top and bottom performers and the patterns they share.
- **Recommendations** mapped to the performance categories (scale and replicate / optimize and expand / test improvements / analyze and pivot), presented as Conclusion → What (with confidence) → Why → How to Act.

