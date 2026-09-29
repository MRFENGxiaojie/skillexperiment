---
name: tpl-situacao-data-pipeline
description: "Guides the design and operation of production-grade data pipelines: ETL/ELT ingestion, transformation flows, event streaming consumers, and batch processing, with source immutability, idempotent re-runs, schema evolution handling, validation gates, dead-letter queues, checkpointing, and backfill strategy. Use when the user is building ETL/ELT pipelines, data ingestion systems, transformation flows, event streaming consumers, or batch processing jobs."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: Building a Data Pipeline

## Workflow

1. **Scope the pipeline** — identify source (system, extraction method, schedule), transformations, destination (load method, partitioning). Design for the pattern that fits: batch pull, streaming push, or lambda (see Architecture Patterns).
2. **Lock the invariants** — apply the seven principles: source is read-only, idempotent re-runs, schema evolution tolerance, validation gates, loud failures, backfill strategy, UTC timestamps.
3. **Implement with the templates** — checkpointing (resume-on-failure), validation gates (reject early), dead-letter queue (never swallow bad records).
4. **Produce the Pipeline Specification** — follow OUTPUT FORMAT; every section needs concrete values (system names, thresholds, SLOs).
5. **Verify against QUALITY GATES** — run the checklist; test idempotent re-run, backfill on staging, schema-evolution case, freshness alert.

1. **Immutability of source is sacred.** Never write to, modify, or delete source data. Always read-only. Create your own layer for transformed data. If you must archive source data, move → verify → delete, never overwrite.

2. **Idempotency is required, not optional.** Running the same pipeline twice (or 100 times) must produce the same result. Design for: unique keys on destination inserts, upsert semantics, checkpointing. A pipeline that creates duplicates on re-run is a liability.

3. **Schema evolution is a first-class concern.** Source data schemas change. Your pipeline must handle: new fields (ignore safely), removed fields (use defaults), type changes (explicit coercion with error on failure). Never deploy a pipeline that crashes on new schema versions.

4. **Validation gates are mandatory.** Add explicit quality checks at ingress: expected row counts, null checks on required fields, value range checks, referential integrity checks. Reject bad data early — downstream systems cannot clean up garbage.

5. **Data pipeline failures must be loud.** A failed pipeline that logs an error and continues is worse than one that stops. Configure: alerting on job failure, data freshness monitoring (alert if output not updated in N hours), row count anomaly detection.

6. **Backfill strategy must exist before production.** "What happens if we need to reprocess the last 90 days?" must have a clear answer before go-live. Design partition schemes and checkpointing to make backfill straightforward.

7. **Timestamps in UTC, always.** Never store timezone-ambiguous timestamps. Convert to UTC at ingestion. Store timezone information as a separate field if needed.

## ROUTING TABLE

- If you encounter duplicate records in destination: add idempotency key; use upsert (`INSERT ... ON CONFLICT DO UPDATE`) or a deduplication step.
- If you encounter missing records (silent data loss): add row count reconciliation; compare expected rows from source vs actual rows in destination; alert on mismatch.
- If the source schema changed unexpectedly: a schema registry or schema evolution strategy is needed; add schema validation at pipeline entry.
- If there are NULL values in required fields: reject the record at the validation gate; send to dead-letter queue for investigation.
- If the pipeline is taking too long: profile whether it is I/O-bound (batching too small) or CPU-bound (transformation logic); add parallelism at the bottleneck stage.
- If backfill is required after a bug fix: use partition-based reprocessing; never backfill the entire table if you can target a date range.
- If the source is an external API (rate limits): implement checkpointing; on rate limit, save progress, wait, and resume; don't re-fetch already-processed records.
- If files are large (GB+): use stream processing, never load to memory; use chunked reads; process, emit, then discard each chunk.
- If a transformation fails on 1 bad record: send it to the dead-letter queue; continue processing valid records; alert on DLQ growth.
- If data freshness is degrading: instrument and alert on lag, i.e., the time between event occurrence and destination visibility.

## Pipeline Architecture Patterns

```
Batch Pipeline (pull):
Source → Extract → Validate → Transform → Load → Verify

Streaming Pipeline (push):
Source Events → Kafka/SQS → Consumer → Validate → Transform → Sink

Lambda Architecture (both):
Streaming: realtime estimates (approximation)
Batch: reprocessing for accuracy (ground truth)
```

## Checkpoint Template

> The code below is an interface sketch — adapt storage, logging, and metrics dependencies to your environment before running.

```python
class PipelineCheckpoint:
    """Track pipeline progress for resume-on-failure and backfill."""
    
    def __init__(self, pipeline_id: str, storage: CheckpointStorage):
        self.pipeline_id = pipeline_id
        self.storage = storage
    
    def save(self, last_processed_id: str, processed_count: int) -> None:
        self.storage.set(self.pipeline_id, {
            "last_processed_id": last_processed_id,
            "processed_count": processed_count,
            "updated_at": datetime.now(timezone.utc).isoformat()
        })
    
    def load(self) -> dict | None:
        return self.storage.get(self.pipeline_id)
    
    def reset(self) -> None:
        """Clear checkpoint to trigger full reprocessing."""
        self.storage.delete(self.pipeline_id)
```

## Data Validation Gates

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    passed: bool
    errors: List[str]

def validate_payment_record(record: dict) -> ValidationResult:
    errors = []
    
    # Required fields
    for field in ['transaction_id', 'amount', 'currency', 'created_at']:
        if field not in record or record[field] is None:
            errors.append(f"Missing required field: {field}")
    
    # Type checks
    if 'amount' in record and not isinstance(record['amount'], (int, float)):
        errors.append(f"amount must be numeric, got: {type(record['amount'])}")
    
    # Range checks
    if 'amount' in record and record.get('amount', 0) <= 0:
        errors.append(f"amount must be positive, got: {record['amount']}")
    
    # Enum checks
    valid_currencies = {'USD', 'EUR', 'BRL'}
    currency = record.get('currency')
    if currency is not None and currency not in valid_currencies:
        errors.append(f"Invalid currency: {currency}")
    
    return ValidationResult(passed=len(errors) == 0, errors=errors)
```

## Dead Letter Queue Pattern

> The code below is an interface sketch — adapt storage, logging, and metrics dependencies to your environment before running.

```python
def process_record(record: dict, dlq: DeadLetterQueue) -> None:
    validation = validate_record(record)
    
    if not validation.passed:
        dlq.send(record, reason=validation.errors, pipeline_version=PIPELINE_VERSION)
        metrics.increment('pipeline.records.rejected')
        return  # Continue with next record, don't stop pipeline
    
    try:
        transformed = transform(record)
        destination.upsert(transformed, key='transaction_id')
        metrics.increment('pipeline.records.processed')
    except Exception as e:
        dlq.send(record, reason=str(e), exception_type=type(e).__name__)
        metrics.increment('pipeline.records.failed')
        logger.error({'event': 'record_failed', 'record_id': record.get('id'), 'error': str(e)})
```

## DO NOT

- **DO NOT** write to source tables — ever, for any reason
- **DO NOT** design a pipeline that can't be re-run safely (idempotency is mandatory)
- **DO NOT** load entire large files into memory — use streaming/chunked processing
- **DO NOT** ignore records that fail validation — route to dead-letter queue, alert on DLQ growth
- **DO NOT** hardcode transformation logic that depends on specific record counts or positions
- **DO NOT** store timezone-naive timestamps — use UTC everywhere
- **DO NOT** run backfill during peak traffic hours — it will compete with production workloads
- **DO NOT** skip the row count reconciliation step — it catches silent data loss

## Scope and Limitations

**What this skill covers:**
- Pipeline architecture decisions (batch / streaming / lambda), design principles, failure handling, and operational practices for ETL/ELT, ingestion, transformation, streaming consumption, and batch jobs
- Diagnosis of common pipeline failure modes via the routing table
- Deliverable: Pipeline Specification with Source / Transformations / Destination / Validation Gates / Failure Handling

**What this skill does NOT do:**
- No implementation of specific frameworks (Airflow, dbt, Spark, Kafka Streams) — code templates are interface sketches to adapt, not ready-to-run code
- No database administration, data modeling, or SQL tuning
- No real-time system internals (e.g., exactly-once semantics of a specific broker)
- Do NOT use when the user asks about pipeline tool installation or when the task is a one-off data transformation script (use a scripting skill)

## OUTPUT FORMAT

For each pipeline, produce:

**Pipeline Specification:**
```markdown
## Pipeline: [Name]

### Source
- System: PostgreSQL production DB (read replica)
- Table: transactions
- Extraction method: poll by updated_at (watermark)
- Schedule: every 15 minutes

### Transformations
1. Normalize currency codes to ISO 4217
2. Convert timestamps to UTC
3. Enrich with user country from users table
4. Filter out test transactions (amount = 0.01)

### Destination
- System: BigQuery
- Dataset: analytics.transactions_processed
- Load method: UPSERT on transaction_id
- Partitioned by: created_at DATE

### Validation Gates
- Required fields: transaction_id, amount (>0), currency, user_id, created_at
- Row count reconciliation: source count vs destination count within 0.1%
- Latency SLO: data visible in destination within 30 minutes of source

### Failure Handling
- Validation failures → DLQ bucket: gs://pipelines-dlq/transactions/
- Alert: PagerDuty if DLQ > 100 records in 1 hour
- Alert: PagerDuty if data freshness > 45 minutes
```

## QUALITY GATES

- [ ] Pipeline is idempotent: running twice produces identical destination state
- [ ] Source data is read-only: zero write traffic to source system
- [ ] Validation gates implemented with dead-letter queue for failed records
- [ ] Row count reconciliation runs after every batch
- [ ] Data freshness alert configured and tested
- [ ] Backfill tested for a 30-day date range on staging
- [ ] All timestamps stored in UTC
- [ ] Schema evolution tested: adding a new column to source doesn't crash pipeline
- [ ] Dead-letter queue has alert on accumulation (data quality monitoring)
- [ ] Checkpoint mechanism enables resume without reprocessing from beginning

