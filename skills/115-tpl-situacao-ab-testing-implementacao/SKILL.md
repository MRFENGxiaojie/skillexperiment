---
name: tpl-situacao-ab-testing-implementacao
description: Guides the agent in planning, implementing, and analyzing A/B tests with statistical rigor. Use when the user is implementing A/B tests, multivariate tests, or feature flag-driven experiments and needs hypothesis design, sample size calculation, significance testing, or clean winner deployment.
allowed-tools: Read, Write, Bash, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: A/B Testing Implementation

## Workflow

1. **Define the experiment.** Write the hypothesis, pick the one primary metric, and set the minimum detectable effect before any traffic is split.
2. **Calculate the sample size.** Run a power analysis (80% power, 95% confidence) and record the required sample size.
3. **Set up assignment.** Implement deterministic sticky bucketing behind a feature flag and define guardrail metrics.
4. **Run to completion.** Never stop early — keep the experiment running until the required sample size is reached, or a safety concern escalates it.
5. **Analyze.** Apply the two-proportion z-test from Statistical Analysis and compare the result against the plan.
6. **Deploy and clean up.** Ship the winning variant, remove the losing variant code and the feature flag.
7. **Report and verify.** Produce the Experiment Report and check every item in QUALITY GATES.

1. **One variable at a time.** An A/B test must change exactly one variable. Changing button color AND copy in the same test makes it impossible to attribute the result. If you need to test multiple things, run sequential or multivariate tests with proper design.

2. **Define the success metric before starting.** What exactly will you measure? What minimum effect size would justify shipping? What sample size do you need to detect it? These answers must exist before traffic is split. Post-hoc metric selection is p-hacking.

3. **Calculate minimum sample size before starting.** Use a power calculator. Typical parameters: 80% statistical power, 95% confidence level, effect size based on minimum meaningful change. Never end an experiment early because "it looks good."

4. **Sticky bucketing is non-negotiable.** A user assigned to variant A must always see variant A. Assignment must be deterministic (hash of user ID + experiment ID), not random per request. Changing assignment mid-experiment invalidates the data.

5. **Guard against novelty effect.** New UI elements always get more clicks initially due to novelty. Run experiments for at least one full business cycle (usually 1-2 weeks minimum) to account for day-of-week effects and novelty decay.

6. **Stop experiments only when sample size is reached or for safety.** Do not stop when you see a positive result "too early." Do not keep running indefinitely. Automated stopping rules (sequential testing) are valid only if configured before the experiment starts.

7. **Clean up experiment code.** A winner means: remove the losing variant, remove the feature flag, promote the winning code to be the permanent implementation. Technical debt from undead experiments compounds quickly.

## ROUTING TABLE

- When you encounter "Let's just run it and see": stop, and define hypothesis, primary metric, and sample size first.
- If an experiment changes 2+ things at once, split it into separate sequential experiments or design it as a proper multivariate test.
- If the sample size is below the calculated minimum, do not analyze; continue running until sample size is reached.
- If a user sees different variants across sessions, sticky bucketing is broken; fix the assignment logic before results are valid.
- If a metric is improving but only for 3 days, a novelty effect is suspected; continue to 2 full weeks.
- If "It's significant! Let's ship!": verify the correct one-tailed vs two-tailed test, no data leakage between variants, and that the experiment ran the full duration.
- If two experiments run on the same page/flow, there is an experiment interaction risk; analyze interaction effects or serialize the experiments.
- If a winning variant is deployed but the flag is left on, remove the flag and remove the losing variant code; the experiment must be fully cleaned up.
- If no holdback group is defined, maintain a holdback (no change) for long-running experiments to measure long-term effects.
- If bot/spider traffic is included in the experiment, filter non-human traffic before analysis; it inflates sample size and dilutes signal.
- If a guardrail metric (error rate / P95) degrades during the run, stop the experiment, roll back to control, and investigate before restarting; do not make a winner decision on degraded data.

If multiple rows apply, resolve in this order: (1) sticky bucketing broken — fix assignment first; (2) bot traffic included — filter before anything else; (3) sample size not reached — do not analyze, keep running; (4) safety concerns — stop and escalate; then follow the remaining rows.

## Experiment Design Template

```markdown
## Experiment: [Name]

**Hypothesis:**
If we [change X], then [metric Y] will [increase/decrease] by [Z%],
because [user psychology/behavior reason].

**Variants:**
- Control (A): [Current behavior - describe precisely]
- Variant B: [What changes - describe precisely]

**Primary Metric:** [One metric. If you have multiple, pick the most important.]
- Checkout completion rate

**Secondary Metrics (monitoring, not decision):**
- Revenue per visitor
- Bounce rate
- Time on page

**Guardrail Metrics (must not degrade):**
- Site error rate
- Page load time P95

**Minimum Detectable Effect:** 5% relative improvement
**Statistical Power:** 80%
**Confidence Level:** 95%
**Required Sample Size:** 12,400 users per variant (example — compute with required_sample_size in the Statistical Analysis section)
**Estimated Duration:** 10 days at current traffic volume

**Traffic Split:** 50% control / 50% variant
**Targeting:** All logged-in users on checkout page

**Assignment:** hash(user_id + "experiment_checkout_cta_v2") % 100 < 50 → control

**Start Date:** [date]
**Minimum End Date:** [start + duration. Never end before this.]
**Decision Date:** [start + duration + 2 days analysis buffer]
```

## Feature Flag Architecture

```typescript
interface ExperimentAssignment {
  variant: 'control' | 'treatment'
  experimentId: string
  userId: string
  assignedAt: string
}

class ExperimentService {
  /**
   * Deterministic, sticky assignment using user ID hash.
   * Same user always gets same variant for same experiment.
   */
  getVariant(userId: string, experimentId: string): 'control' | 'treatment' {
    // Hash must be consistent — not time-dependent
    // Requires murmurhash-js (npm i murmurhash-js)
    const hash = murmurhash(`${userId}:${experimentId}`)
    const bucket = hash % 100
    
    const experiment = this.getExperiment(experimentId)
    
    if (!experiment || !experiment.isActive) {
      return 'control' // Default: show control when no experiment
    }
    
    return bucket < experiment.treatmentPercentage ? 'treatment' : 'control'
  }

  /** Always log assignments for analysis */
  assignAndLog(userId: string, experimentId: string): ExperimentAssignment {
    const variant = this.getVariant(userId, experimentId)
    
    const assignment: ExperimentAssignment = {
      variant,
      experimentId,
      userId,
      assignedAt: new Date().toISOString()
    }
    
    // Log once per user per experiment (not every request)
    if (!this.hasLoggedAssignment(userId, experimentId)) {
      this.analyticsClient.track('experiment_enrolled', assignment)
      this.cacheAssignment(userId, experimentId)
    }
    
    return assignment
  }
}
```

## Statistical Analysis

```python
from scipy import stats
import numpy as np
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

def analyze_ab_test(
    control_conversions: int, 
    control_visitors: int,
    treatment_conversions: int,
    treatment_visitors: int,
    alpha: float = 0.05
) -> dict:
    """Returns analysis result with clear ship/no-ship recommendation."""
    
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors
    relative_lift = (treatment_rate - control_rate) / control_rate
    
    # Two-proportion z-test
    stat, p_value = stats.proportions_ztest(
        [treatment_conversions, control_conversions],
        [treatment_visitors, control_visitors]
    )
    
    is_significant = p_value < alpha
    
    return {
        'control_rate': f"{control_rate:.2%}",
        'treatment_rate': f"{treatment_rate:.2%}",
        'relative_lift': f"{relative_lift:+.1%}",
        'p_value': round(p_value, 4),
        'is_significant': is_significant,
        'recommendation': 'SHIP' if (is_significant and relative_lift > 0) else 'NO_SHIP'
    }


def required_sample_size(base_rate: float, mde: float, alpha: float = 0.05,
                         power: float = 0.8) -> int:
    """Sample size per variant from a two-proportion power analysis."""
    es = proportion_effectsize(base_rate, base_rate * (1 + mde))
    n = NormalIndPower().solve_power(es, power=power, alpha=alpha,
                                     ratio=1, alternative='two-sided')
    return int(n)
```

## DO NOT

- **DO NOT** analyze results before minimum sample size is reached
- **DO NOT** change the primary metric after the experiment starts
- **DO NOT** run an experiment on < 1 week of data (day-of-week effects)
- **DO NOT** make a decision based on secondary metrics if the primary metric is flat
- **DO NOT** leave losing variant code in the codebase after concluding the experiment
- **DO NOT** count the same user's sessions as independent samples
- **DO NOT** run experiments on new or infrequent users only (survivorship bias)
- **DO NOT** include bot/crawler traffic in experiment analysis

## OUTPUT FORMAT

At experiment conclusion, produce an **Experiment Report:**

```markdown
## Experiment Report: [Name]

**Duration:** 2024-01-01 to 2024-01-14 (14 days)
**Total Visitors:** 28,400 (14,200 per variant)

### Results

- Control had 14,200 visitors, 852 conversions, a 6.00% rate, and vs Control it is the baseline (—).
- Treatment had 14,200 visitors, 945 conversions, a 6.66% rate, and vs Control it was +10.9%.

**p-value:** 0.023 (statistically significant at 95% confidence)
**Relative Lift:** +10.9% on checkout completion rate

### Decision: **SHIP TREATMENT** ✅

### Next Steps
- [ ] Deploy treatment as permanent implementation
- [ ] Remove control variant code
- [ ] Archive experiment config (keep 90 days for reference)
- [ ] Remove feature flag
- [ ] Document learnings in team wiki
```

## SCOPE

This skill covers classic two-variant A/B experiments: hypothesis design,
sample size planning, deterministic assignment, two-proportion significance
testing, winner promotion, and cleanup.

It does NOT cover: A/A calibration tests, CUPED/stratified/regression-adjusted
analysis, multi-armed bandit or adaptive experiments, Bayesian methods,
non-experimental research (surveys, usability tests), or replacing the
product owner's business decision. For those, the agent should say so and
offer alternatives instead of applying this skill's procedure.

## QUALITY GATES

- [ ] Hypothesis written before experiment starts
- [ ] Primary metric defined before experiment starts
- [ ] Sample size calculated with power analysis before starting
- [ ] Minimum experiment duration respected (no early stopping except safety)
- [ ] Sticky bucketing verified: same user always gets same variant
- [ ] Bot traffic excluded from analysis
- [ ] One primary metric — not "any of these 5 look good"
- [ ] Both losing variant code AND feature flag removed after conclusion
- [ ] Experiment report documented and accessible to product/leadership
- [ ] Guardrail metrics checked: no degradation in error rate or performance

