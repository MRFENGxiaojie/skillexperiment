"""Legacy daily ad-hoc sync of supplier order data into BigQuery (known flaws; redesign planned in PIPELINE_SPEC.md)."""

import os
import datetime
import psycopg2

import requests
from google.cloud import bigquery

VENDOR_API = os.environ.get("VENDOR_API_URL", "https://api.vendor.example/v2/orders")
VENDOR_TOKEN = os.environ.get("VENDOR_API_TOKEN", "")
REPLICA_DSN = os.environ.get("REPLICA_DSN", "postgresql://readonly:ro@replica/db")
PROJECT = os.environ.get("BQ_PROJECT", "acme-analytics")
DATASET = os.environ.get("BQ_DATASET", "raw")
TABLE = os.environ.get("BQ_TABLE", "supplier_orders")

# Hardcoded vendor API field mapping.
# TODO(ops): the vendor occasionally renames these fields and the sync breaks
# until someone hand-edits the mapping; should be a schema-version registry.
FIELD_ORDER_NO = "order_no"          # vendor has used "orderId"/"no" before
FIELD_ORDER_AMOUNT = "order_amount"  # vendor has used "amount_total" before
FIELD_CREATED_AT = "created_at"

def fetch_vendor_orders():
    """Pull every order page from the vendor open API."""
    orders = []
    page = 1
    while True:
        # FLAW: no rate-limit handling (no 429 backoff, no exponential retry)
        # and no timeout -> a throttled or hung request kills the whole run.
        resp = requests.get(
            VENDOR_API,
            params={"page": page, "page_size": 500, "api_key": VENDOR_TOKEN},
        )
        resp.raise_for_status()
        payload = resp.json()
        orders.extend(payload.get("results", []))
        if not payload.get("has_more"):
            break
        page += 1
    return orders

def fetch_replica_transactions(conn):
    """Read the full transactions table from the read-only replica."""
    cur = conn.cursor()
    # FLAW: SELECT * with no watermark/incremental cursor. Every run re-reads
    # all history and re-inserts it, so re-runs duplicate rows at volume.
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in rows]

def normalize(orders, transactions):
    """Combine vendor + replica records into BigQuery-ready rows."""
    rows = []
    for order in orders:
        # FLAW: no per-record try/except. One malformed record (e.g. a vendor
        # field rename) raises KeyError and aborts the entire batch.
        rows.append({
            "source": "vendor",
            "order_no": order[FIELD_ORDER_NO],
            "amount": order[FIELD_ORDER_AMOUNT],
            "currency": order.get("currency", "USD"),
            "created_at": order.get(FIELD_CREATED_AT),
            "synced_at": datetime.datetime.utcnow().isoformat() + "Z",
        })
    for txn in transactions:
        rows.append({
            "source": "replica",
            "order_no": txn["transaction_id"],
            "amount": txn["amount"],
            "currency": txn.get("currency", "USD"),
            "created_at": txn["created_at"],
            "synced_at": datetime.datetime.utcnow().isoformat() + "Z",
        })
    return rows

def load_to_bigquery(client, rows):
    """Insert all rows into the destination BigQuery table."""
    table_id = f"{PROJECT}.{DATASET}.{TABLE}"
    # FLAW: insert_rows_json with no dedup/UPSERT key, so re-running the job
    # duplicates every row already present in the table.
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        raise RuntimeError(f"BigQuery insert failed: {len(errors)} errors")
    return len(rows)

def main():
    client = bigquery.Client(project=PROJECT)
    conn = psycopg2.connect(REPLICA_DSN)

    orders = fetch_vendor_orders()
    transactions = fetch_replica_transactions(conn)
    conn.close()

    # FLAW: naive UTC from datetime.utcnow() stamped on the app host.
    rows = normalize(orders, transactions)
    count = load_to_bigquery(client, rows)
    print(f"[sync] inserted {count} rows from {len(orders)} vendor orders + {len(transactions)} transactions")

if __name__ == "__main__":
    main()
