# Supplier Orders Data Pipeline (legacy)

`scripts/sync_orders.py` is the ad-hoc daily sync: vendor open API orders plus a
`SELECT * FROM transactions` read of the production replica, into BigQuery. It
has known problems (no rate-limit/timeout handling, full pulls with no watermark
= duplicate rows, one bad record stalls the batch, `insert_rows_json` with no
UPSERT, hardcoded vendor field names). A redesign is planned in `PIPELINE_SPEC.md`.
