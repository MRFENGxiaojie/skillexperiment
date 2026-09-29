# Incident notes — payment service outage (2026-08-09, evening)

Raw fragments from the on-call / support channel (edited only for readability).
Timestamps local (UTC+8). Gap indicates silence on channel.

---

**19:38** — @sarah (support): "customers calling in, can't complete checkout — 'payment method declined' on a lot of them, anything up?"

**19:41** — @dev-oncall: "checking pay-api… /health says UP. looking at metrics"

**19:44** — @sarah: "4 calls in last 10 min. escalating"

**19:50** — @dev-oncall: "ok found it. pay-api DB connection pool exhausted, connections queueing. error in logs: `pool_get_connection timed out after 10s`"

**19:52** — @sarah: "make it stop, we're getting one call every 2 minutes now"

**19:55** — @dev-oncall: "tried bumping pool size via config, needs restart. restarting pay-api instances (rolling)"

**20:02** — @dev-oncall: "restart done, pool error gone but now checkout calls are timing out at gateway — `503 gateway timeout`. orders still failing"

**20:08** — @sarah: "12 calls so far. any ETA? manager asking"

**20:11** — @dev-oncall: "working theory: connection pool exhaustion blew up some DB rows mid-write, now there's lock contention on orders table. `lock wait timeout exceeded` in logs. investigating"

**20:24** — @db-admin: "on it. saw long-running tx from pay-api held locks ~20min. killing those"

**20:31** — @db-admin: "killed 3 long-running transactions. locks released. orders table accessible again"

**20:40** — @dev-oncall: "traffic ramping back up slowly. checkout succeeding again but only ~40% of normal rate"

**20:52** — @sarah: "calls dropping off. maybe 18 total by now. keep me posted, drafting customer note"

**21:15** — @dev-oncall: "error rate < 1% now. monitoring"

**21:50** — @dev-oncall: "all clear. pay-api fully recovered, normal traffic. starting notes for postmortem"

**21:52** — @sarah: "thank you. total ~24 customer calls. mostly merchants asking about failed payments."

---

## Scraps for the postmortem

- Order failure counts (from dashboard, 5-min buckets): see `order-metrics.csv`
- Sample log lines: see `error-logs.txt`
- Summary: ~2h10m degraded/outage window (19:40 → 21:50), recovery at 21:50
