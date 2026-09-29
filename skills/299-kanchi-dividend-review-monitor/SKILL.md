---
name: kanchi-dividend-review-monitor
description: Monitor dividend portfolios with Kanchi-style forced-review triggers (T1-T6) and convert anomalies into OK/WARN/REVIEW states without auto-selling. Use when the user asks to detect dividend cuts, monitor 8-K governance filings, review dividend safety, automate a REVIEW queue, or run periodic dividend risk checks.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Kanchi Dividend Review Monitor

## Overview

Detect abnormal dividend-risk signals and route them into a human review queue.
Treat automation as anomaly detection, not automated trade execution.

## When to Use

Use this skill when the user needs:
- Daily/weekly/quarterly anomaly detection for dividend holdings.
- Forced review queueing for T1-T6 risk triggers.
- 8-K/governance keyword scans tied to portfolio tickers.
- Deterministic `OK/WARN/REVIEW` output before manual decision making.

## Prerequisites

Provide normalized input JSON that follows:
- `references/input-schema.md`

If upstream data is unavailable, provide at least:
- `ticker`
- `instrument_type`
- `dividend.latest_regular`
- `dividend.prior_regular`

## Non-Negotiable Rule

Never auto-sell based only on machine triggers.
Always create `WARN` or `REVIEW` evidence for human confirmation first.

## Scope and Limitations

This skill monitors dividend-risk signals and builds a human review queue. It does not:

- Make trades. The Non-Negotiable Rule above is the outer boundary — never auto-sell, never auto-buy.
- Handle tax treatment or account migration. Those belong to `kanchi-dividend-us-tax-accounting`.
- Cover non-dividend risk monitoring (credit lines, market beta, or portfolio concentration beyond dividend safety).
- Replace human underwriting. The `REVIEW` ticket exists because a human makes the final call.

Do not use this skill for one-off valuation questions, tickers with no dividend history, or situations that need immediate trade execution — it produces evidence for review, not actions.

Output files must land in the workspace `reports/` directory so the harness and reviewer can find them (see Workflow step 2).

## State Machine

- `OK`: no action.
- `WARN`: add to next check cycle and pause optional adds.
- `REVIEW`: immediate human review ticket + pause adds.

Use `references/trigger-matrix.md` for trigger thresholds and actions.

### Flat-dividend cadence caveat

T6 fires only when a dividend-basis flag is set (`cut_flag` / `variable_policy_flag` -> `REVIEW`, `freeze_flag` / `special_dividend_flag` -> `WARN`). A latest regular dividend equal to the prior regular dividend with no flags set is not a machine trigger on its own — the ticker stays `OK` unless another trigger fires, because many quarterly dividend payers repeat the same dividend for several quarters between annual raise cycles.

When a flat dividend is driven by `freeze_flag`, treat the `WARN` as a cadence confirmation request, not as proof of dividend deterioration. In reports, phrase this as "confirm next dividend-growth cadence / pause optional adds until checked" and avoid implying a cut or broken thesis unless T1/T2/T3/T4/T5 evidence also supports escalation.

## Monitoring Cadence

- Daily:
  - T1 dividend cut/suspension.
  - T4 SEC filing keyword scan (8-K oriented).
  - T6 dividend-policy change flags.
- Weekly:
  - T3 proxy credit stress checks.
- Quarterly:
  - T2 coverage deterioration and T5 structural decline scoring.

## Workflow

### 1) Normalize input dataset

Collect per ticker fields in one JSON document:
- Dividend points (latest regular, prior regular, missing/zero flag).
- Coverage fields (FCF or FFO or NII, dividends paid, ratio history).
- Balance-sheet trend fields (net debt, interest coverage, buybacks/dividends).
- Filing text snippets (especially recent 8-K or equivalent alert text).
- Operations trend fields (revenue CAGR, margin trend, guidance trend).

Use `references/input-schema.md` for field definitions
and sample payload.

### 2) Run the rule engine

Run:

```bash
python3 scripts/build_review_queue.py \
  --input <path-to-monitor-input>.json \
  --output-dir reports/
```

Run from the skill directory (the directory that contains `scripts/`). The script maps each ticker to `OK/WARN/REVIEW` based on T1-T6. Output files must land in the workspace `reports/` directory with the dated filenames shown (e.g., `review_queue_20260227.json` and `.md`).

### 3) Prioritize and deduplicate

If multiple triggers fire:
- Keep all findings for audit trail.
- Escalate final state to highest severity only.
- Store trigger reasons as single-line evidence.

### 4) Generate human review tickets

For each `REVIEW` ticker, include:
- Trigger IDs and evidence.
- Suspected failure mode.
- Required manual checks for next decision.

Use `references/review-ticket-template.md` output format.

## SEC Filing Guardrail

When implementing live SEC fetchers:
- Include a compliant `User-Agent` string (name + email).
- Use caching and throttling.
- Respect SEC fair-access guidance.
- In scheduled portfolio reviews where upstream filing snippets are empty, use SEC `company_tickers.json` plus `https://data.sec.gov/submissions/CIK##########.json` to enumerate recent 8-K / 8-K/A filings for each holding, then scan primary filing documents for the T4 keyword family (`Item 4.02`, non-reliance, restatement, material weakness, SEC investigation, subpoena, going concern, auditor resignation, internal control). Record the scan window, recent 8-K count, and whether hits were found. Treat "no keyword hits" as a narrow T4 scan result, not a full governance clearance.

## Output Contract

Always return:
1. Queue JSON with summary counts and ticker-level findings.
2. Markdown dashboard for quick triage.
3. List of immediate `REVIEW` tickets.

## Multi-Skill Handoff

- Consume the ticker universe and baseline assumptions from the upstream Kanchi dividend SOP pipeline (the external system that produces the normalized input).
- Feed `REVIEW` results back to that pipeline for re-underwriting and position-size review.
- Share account-type context with `kanchi-dividend-us-tax-accounting` when risk events imply account relocation decisions.

## Resources

- `scripts/build_review_queue.py`: local rule engine for T1-T6.
- `scripts/tests/test_build_review_queue.py`: unit tests for T1-T6 and report rendering (run with `pip install pytest`, then `python -m pytest scripts/tests`).
- `references/trigger-matrix.md`: trigger definitions, cadence, and actions.
- `references/input-schema.md`: normalized input schema and sample JSON.
- `references/review-ticket-template.md`: standardized manual-review ticket layout.

