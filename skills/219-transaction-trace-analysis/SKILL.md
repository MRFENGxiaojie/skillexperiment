---
name: transaction-trace-analysis
description: Teaches evidence-based analysis of transaction logs and traces. Use when reconstructing transaction behavior from tables, TSV/CSV files, timestamps, counters, object histories, validation records, abort records, retries, partial logs, or when producing classified transaction outputs from trace evidence.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Transaction Trace Analysis

Use this skill when the task provides concrete logs, tables, counters, timestamps, or partial records and asks you to infer transaction behavior.

This skill is about *reconstruction under partial evidence*:

- normalize columns into a stable event vocabulary
- reconstruct per-transaction intent and per-object version timelines
- join them through explicit fields (not through row order guesses)
- produce a minimal, auditable classification for the required output

## Quick Reference (pick the next file to read)

- If you need help mapping weird columns into tx/key/op/timestamp/counter/status/reason, read [trace-schema-normalization.md](references/trace-schema-normalization.md).
- If you need help grouping events per transaction and avoiding "attempt vs request" mixups, read [transaction-history-reconstruction.md](references/transaction-history-reconstruction.md).
- If you need help reconstructing a per-key version timeline from writes/validation, read [object-version-history.md](references/object-version-history.md).
- If you need help interpreting timestamp/counter semantics and scope correctly, read [timestamp-and-ordering-fields.md](references/timestamp-and-ordering-fields.md).
- If you need help understanding validation failures, abort reasons, and conservative checks, read [validation-and-abort-records.md](references/validation-and-abort-records.md).
- If you need help avoiding overclaims when the trace is incomplete, read [evidence-quality-and-uncertainty.md](references/evidence-quality-and-uncertainty.md).
- If you need help emitting deduped/sorted ids and minimal justifications, read [output-classification-patterns.md](references/output-classification-patterns.md).

## Trace Ledger (what you build first)

Build two tiny ledgers before doing any deep inference:

### Transaction ledger

```text
txn_id -> {
  seen_keys: [...],
  read-evidence: (key, observed_version_fields...),
  write-evidence: (key, installed_version_fields...),
  validation/abort-evidence: [...],
  candidate_commit_fields: ...,
}
```

### Object ledger

```text
key -> timeline [
  { event: write/abort/validate, txn_id, version_fields, counter_fields },
  ...
]
```

Only after both exist should you attempt joins like “did T’s read become stale?” or “could an aborted T have committed?”

## Workflow (operational)

1. **Schema normalization**: name every column; identify scope for each counter/timestamp.
2. **Per-txn reconstruction**: summarize each txn’s evidence and candidate serialization point fields.
3. **Per-key reconstruction**: build a timeline per key; validate what orders it (wts? counter?).
4. **Decision modeling**: re-express the protocol’s decision rule in terms of trace fields.
5. **Classification**: prove “must abort” vs “could commit” vs “unknown from evidence.”
6. **Output**: dedupe ids, sort if required, write exact format.

## Common Pitfalls

- **Treating per-key counters as global order.**
- **Using file row order as time order without justification.**
- **Calling something ‘unnecessary’ without exhibiting a safe order consistent with evidence.**

## Scope and Limitations

This skill teaches evidence-based analysis of transaction traces: reconstructing transaction behavior from tables, TSV/CSV files, timestamps, counters, object histories, validation records, abort records, retries, and partial logs. It produces classified transaction outputs — committed, aborted, indeterminate, missing — backed by trace evidence.

It does not perform real-time monitoring, distributed tracing instrumentation, or log aggregation. It works with the trace data provided; it cannot recover data that was never logged. The analysis is only as good as the trace coverage — gaps in instrumentation produce gaps in the reconstruction.

