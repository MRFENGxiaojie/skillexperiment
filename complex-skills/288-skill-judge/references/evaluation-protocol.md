## Evaluation Protocol

### Step 1: First Pass — Knowledge Delta Scan

Read SKILL.md completely and for each section ask:
> "Does Claude already know this?"

Mark each section as:
- **[E] Expert**: Claude genuinely does not know this — value add
- **[A] Activation**: Claude knows but brief reminder is useful — acceptable
- **[R] Redundant**: Claude definitely knows this — should be deleted

Calculate approximate ratio: E:A:R
- Good Skill: >70% Expert, <20% Activation, <10% Redundant
- Mediocre Skill: 40-70% Expert, high Activation
- Poor Skill: <40% Expert, high Redundant

### Step 2: Structure Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and their sizes
[ ] Identify which pattern the Skill follows
[ ] Check load triggers (if references exist)
```

### Step 3: Score Each Dimension

For each of the 8 dimensions:
1. Find specific evidence (cite relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < maximum

### Step 4: Calculate Total and Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8
Maximum = 120 points
```

**Grade Scale** (percentage-based):
| Grade | Percentage | Meaning |
|------|-----------|-----------|
| A | 90%+ (108+) | Excellent — Production-ready expert Skill |
| B | 80-89% (96-107) | Good — minor improvements needed |
| C | 70-79% (84-95) | Adequate — clear improvement path |
| D | 60-69% (72-83) | Below Average — significant issues |
| F | <60% (<72) | Poor — needs fundamental redesign |

### Step 5: Generate Report

Assemble the report following the **Output Format** section in SKILL.md: Summary (total score, grade, pattern, E:A:R ratio, verdict), Dimension Scores table, Critical Issues, Top 3 Improvements, and Detailed Recommendations with line references. Use the templates in `summary.md`, `dimension-scores.md`, `critical-issues.md`, `top-3-improvements.md`, and `detailed-recommendations.md` for consistent structure:

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/120 (X%)
- **Grade**: [A/B/C/D/F]
- **Pattern**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Verdict**: [One-sentence assessment]

## Dimension Scores
[Table with all 8 dimensions, their scores, and notes]

## Critical Issues
[Issues that must be fixed and significantly impact effectiveness]

## Top 3 Improvements
[Prioritized, specific improvement suggestions]

## Detailed Recommendations
[Specific, actionable suggestions with line references]
```