# Trigger Matrix (T1-T6)

Apply these rules to route tickers into `OK`, `WARN`, or `REVIEW`.

## Severity Policy

- `OK`: no forced action.
- `WARN`: queue for next checkpoint and pause optional adds.
- `REVIEW`: immediate human review ticket and pause adds.

## Trigger Definitions

| Trigger | Core signal | Default machine rule | Frequency | Default action |
|---|---|---|---|---|
| T1 | Dividend cut or suspension | `latest_regular < prior_regular * 0.99` OR `latest_regular <= 0` OR missing dividend feed | Daily | `REVIEW` |
| T2 | Coverage deterioration | `denominator <= 0` with positive dividends OR coverage ratio `>1.0` for 2 periods | Quarterly | `WARN/REVIEW` |
| T3 | Credit stress proxy | Net debt rising 3 periods + weakening interest coverage and/or stretched capital return | Weekly + Quarterly confirm | `WARN/REVIEW` |
| T4 | Governance/accounting red flag | Filing text hits Item 4.02, non-reliance, restatement, material weakness, SEC investigation, subpoena, going concern, auditor resignation, internal control | Daily | `REVIEW` |
| T5 | Structural decline | 2+ simultaneous negatives (2 → `WARN`, 3+ → `REVIEW`): revenue CAGR <0, margin downtrend, guidance downtrend, stalled dividend growth | Quarterly | `WARN/REVIEW` |
| T6 | Dividend-policy change (dividend-basis flags) | `cut_flag` OR `variable_policy_flag` → `REVIEW`; `freeze_flag` OR `special_dividend_flag` → `WARN` | Daily | `WARN/REVIEW` |

T6 consumes the dividend-basis flags (`dividend.flags`) emitted by the
upstream Kanchi dividend SOP pipeline (an external system). Flags are read
from `dividend.flags` (preferred) or directly off `dividend`. A top-level
`schema_version` and any unknown fields are ignored, so a newer upstream
schema cannot silently break this monitor.

The engine is a stateless rule set; the Frequency column is the recommended
review cadence, not an engine behavior. T6 fires only when a flag is set —
a flat dividend with no flags is not a trigger.

## Denominator Mapping For T2

| Instrument | Denominator |
|---|---|
| Stock | FCF (`CFO - CapEx`) |
| REIT | FFO/AFFO |
| BDC | NII |
| ETF | Fund-level FCF fallback in the script; holdings-level quality proxies are a human supplement when fund coverage is unavailable |

## Escalation Rule

If multiple triggers fire, keep all findings and set final state to highest severity:
- `OK < WARN < REVIEW`.

Within T2 itself, sustained breach (`>1.0` for 2 periods) takes priority over single-period breach.
