#!/usr/bin/env python3
"""Pricing scenario modeler: projects the revenue impact of a price increase.

Inputs (current state + planned increase):
    --mrr       current monthly recurring revenue (required)
    --arpa      current average revenue per account (required)
    --churn     current monthly churn rate, e.g. 0.03 (required)
    --increase  planned price increase as a decimal, e.g. 0.25 (default 0.20)
    --retention comma-separated customer-retention scenarios, e.g. "1.0,0.8,0.7"
                (default: "1.0,0.8,0.7" matching the 100%/80%/70% convention)

Output:
    For each retention scenario: customers kept, new MRR, revenue impact
    (delta and percent), and whether the increase nets positive.

Usage:
    python scripts/pricing_modeler.py --mrr 50000 --arpa 500 --churn 0.03 --increase 0.25
    python scripts/pricing_modeler.py --json --mrr 100000 --arpa 400 --increase 0.20
"""

import argparse
import json
import sys


def model(
    mrr: float,
    arpa: float,
    churn: float,
    increase: float,
    retentions: list[float],
) -> dict:
    """Return the scenario matrix as a dict."""

    if mrr <= 0:
        raise ValueError("--mrr must be positive")
    if arpa <= 0:
        raise ValueError("--arpa must be positive")
    if churn < 0 or churn >= 1:
        raise ValueError("--churn must be in [0, 1)")
    if increase < 0:
        raise ValueError("--increase must be non-negative")

    customers = mrr / arpa
    new_price_multiplier = 1.0 + increase

    scenarios = []
    for retention in retentions:
        if retention < 0 or retention > 1:
            raise ValueError("retention must be in [0, 1]")
        kept_customers = customers * retention
        # Customers who stay pay the new price; customers who churn pay nothing
        new_mrr = kept_customers * arpa * new_price_multiplier
        delta = new_mrr - mrr
        scenarios.append(
            {
                "retention": round(retention * 100),
                "customers_kept": round(kept_customers),
                "new_mrr": round(new_mrr, 2),
                "mrr_delta": round(delta, 2),
                "mrr_delta_pct": round((delta / mrr) * 100, 1) if mrr else 0.0,
                "net_positive": delta >= 0,
            }
        )

    # Baseline at current churn with no price change, for reference
    baseline_mrr = customers * (1 - churn) * arpa

    return {
        "inputs": {
            "mrr": mrr,
            "arpa": arpa,
            "customers": round(customers),
            "monthly_churn": churn,
            "price_increase": increase,
        },
        "baseline_mrr_after_current_churn": round(baseline_mrr, 2),
        "scenarios": scenarios,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Model the revenue impact of a price increase")
    parser.add_argument("--mrr", type=float, required=True, help="current monthly recurring revenue")
    parser.add_argument("--arpa", type=float, required=True, help="current average revenue per account")
    parser.add_argument("--churn", type=float, default=0.0, help="current monthly churn rate, e.g. 0.03")
    parser.add_argument("--increase", type=float, default=0.20, help="planned price increase as decimal, e.g. 0.25")
    parser.add_argument("--retention", type=str, default="1.0,0.8,0.7",
                        help="comma-separated retention scenarios, default 100%%,80%%,70%%")
    parser.add_argument("--json", action="store_true", help="output JSON instead of a table")
    args = parser.parse_args()

    try:
        retentions = [float(r) for r in args.retention.split(",")]
        result = model(args.mrr, args.arpa, args.churn, args.increase, retentions)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    inputs = result["inputs"]
    print(
        f"Current: MRR ${inputs['mrr']:,.0f} | {inputs['customers']} customers "
        f"at ${inputs['arpa']:,.2f} ARPA | churn {inputs['monthly_churn']:.1%}"
    )
    print(f"Price increase: {inputs['price_increase']:.0%} -> new ARPA ${inputs['arpa'] * (1 + inputs['price_increase']):,.2f}")
    print(f"Baseline MRR after current churn (no change): ${result['baseline_mrr_after_current_churn']:,.2f}")
    print()
    print("Retention | Customers kept | New MRR      | MRR delta    | % change | Net positive")
    print("----------|----------------|--------------|--------------|----------|-------------")
    for s in result["scenarios"]:
        print(
            f"{s['retention']:>8}% | {s['customers_kept']:>14,} | "
            f"${s['new_mrr']:>11,.2f} | ${s['mrr_delta']:>11,.2f} | "
            f"{s['mrr_delta_pct']:>7.1f}% | {str(s['net_positive']):>12}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
