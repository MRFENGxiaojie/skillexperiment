# Decision Matrix (Spec)

> Mandatory reading before recommending any tool or action. This matrix gives
> the selection criteria behind the principles in SKILL.md. Record every
> choice in `plan.json` → `.decisions[]` with the row(s) that drove it.

## 1. Process management

| Scenario | Tool | When to prefer |
|----------|------|----------------|
| Node.js app, single host | PM2 | Cluster mode, zero-downtime reload, built-in metrics |
| Any app on Linux | systemd | Native, survives reboots, no extra install |
| Containerized workload | Docker/Podman | Isolation, reproducible deploys |
| Multi-host orchestration | Kubernetes / Swarm | Auto-scaling, rolling updates, HA |

Decision rules:
- Single host + Node → PM2 unless the org standardizes on systemd.
- Already containerized → stay with containers; do not add a second layer.
- More than one host or rolling deploys needed → orchestration, not a bigger
  process manager.

## 2. Monitoring

| Need | Options |
|------|---------|
| Simple / free | PM2 metrics, htop, logwatch |
| Full observability | Grafana + Prometheus, Datadog |
| Error tracking | Sentry |
| Uptime | UptimeRobot, Pingdom |

Decision rules:
- Start with uptime checks + health endpoints; add deep metrics only when a
  symptom demands them.
- Metrics must map to alert severities (critical / warning / info), each with
  a defined response.

## 3. Logging

- Rotate logs (logrotate or app-level) before disk fills.
- Structured JSON logs for parseability.
- Levels: error / warn / info / debug; default info in production.
- No secrets or PII in logs.

## 4. Scaling

| Symptom | Response |
|---------|----------|
| High CPU, sustained | Horizontal (add instances) |
| High memory | Fix the leak or grow RAM; scale out only after profiling |
| Slow response | Profile first, then scale |
| Traffic spikes | Auto-scaling with defined min/max |

Decision rules:
- Vertical scaling is a quick fix for a single instance; horizontal is the
  sustainable path once the app is stateless (or sessions are externalized).
- Never scale blindly — profiling evidence first.

## 5. Health checks

- Simple: HTTP 200 on `/health` — enough for basic LB routing.
- Deep: also check DB connection and critical dependencies — when a service
  should be pulled from rotation on partial failure.
- Match the check depth to what the load balancer actually uses it for.

## 6. Troubleshooting order

1. Is it running? (process status)
2. Logs (error messages)
3. Resources (disk, memory, CPU)
4. Network (ports, DNS)
5. Dependencies (database, APIs)

The first evidence wins — do not skip steps.
