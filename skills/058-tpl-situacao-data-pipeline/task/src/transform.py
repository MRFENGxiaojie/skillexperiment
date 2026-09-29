"""Transform layer sketch for the redesigned supplier-orders pipeline.

Stubs only. The legacy ad-hoc script scripts/sync_orders.py inlines this logic
today, hardcoded to vendor field names. The redesign moves it here as a
versioned, validated transform step (see PIPELINE_SPEC.md).
"""


def normalize_order(raw: dict) -> dict:
    """Normalize one raw order record into the canonical warehouse shape.

    Expected output keys: order_no, amount, currency, created_at, source,
    synced_at (UTC ISO string).

    The redesign should drive field mapping from a schema_version registry
    instead of hardcoded vendor names, so a vendor field rename never crashes
    the caller. Unknown or renamed fields must be ignored or defaulted, and
    schema changes surfaced via schema_version.
    """
    raise NotImplementedError("implemented in the pipeline redesign")


def validate_order(record: dict) -> list:
    """Validate one normalized record; return a list of error strings.

    An empty list means the record is valid. Required-field, type/range, and
    currency-enum checks belong here. Bad records should be routed to a
    dead-letter queue and reported, not allowed to fail the whole batch.
    """
    raise NotImplementedError("implemented in the pipeline redesign")
