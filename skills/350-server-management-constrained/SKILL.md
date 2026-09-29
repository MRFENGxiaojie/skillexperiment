---
name: server-management-constrained
description: Server management principles and decision making. Process management, monitoring strategy, and scalability decisions. Teaches reasoning, not commands. Use when the user asks about managing production servers, choosing a process manager (PM2, systemd, Docker), monitoring or logging, health checks, scaling, or troubleshooting server issues.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Server Management

> Server management principles for production operations.
> **Learn to THINK, don't memorize commands.**

---

## Mandatory Workflow

Before giving any server recommendation, you MUST:

1. **Create the decision record** at `.workflow/.scratchpad/server-plan-{timestamp}/plan.json` with:
   ```json
   {"status": "init", "inventory": {}, "requirements": [], "decisions": [], "verification": null}
   ```
2. **Read the decision matrix** at `specs/decision-matrix.md` — do not recommend any tool before reading it
3. **Record every decision** in `plan.json` → `.decisions[]` with fields: `decision_id`, `topic`, `options_considered`, `chosen`, `rationale`
4. **After all decisions made**, verify consistency and update `plan.json` → `.verification` with `{"consistent": true/false, "warnings": []}`
5. **Do not skip the decision record** — if `.workflow/` is not writable, create it first

---

## 1. Process Management Principles

### Tool Selection

- For Node.js apps, use PM2 (clustering, reload).
- For any app, use systemd (Linux native).
- For containers, use Docker/Podman.
- For orchestration, use Kubernetes or Docker Swarm.

### Process Management Goals

- Restart on failure means auto-recovery.
- Reload without downtime means no service interruption.
- Clustering means using all CPU cores.
- Persistence means surviving server reboots.

---

## 2. Monitoring Principles

### What to Monitor

- Monitor availability via uptime and health checks.
- Monitor performance via response time and throughput.
- Monitor errors via error rate and error types.
- Monitor resources via CPU, memory, and disk.

### Alert Severity Strategy

- Critical alerts require immediate action.
- Warning alerts require investigation soon.
- Info alerts require daily review.

### Monitoring Tool Selection

- For simple/free monitoring, use PM2 metrics or htop.
- For full observability, use Grafana or Datadog.
- For error tracking, use Sentry.
- For uptime monitoring, use UptimeRobot or Pingdom.

---

## 3. Log Management Principles

### Log Strategy

- Application logs are used for debugging and audit.
- Access logs are used for traffic analysis.
- Error logs are used for problem detection.

### Log Principles

1. **Rotate logs** to prevent disk fill
2. **Structured logging** (JSON) for parsing
3. **Appropriate levels** (error/warn/info/debug)
4. **No sensitive data** in logs

---

## 4. Scalability Decisions

### When to Scale

- If CPU is high, add instances (horizontal scaling).
- If memory is high, increase RAM or fix the leak.
- If response is slow, profile first, then scale.
- If traffic spikes, use auto-scaling.

### Scalability Strategy

- Vertical scaling is a quick fix for a single instance.
- Horizontal scaling is sustainable and distributed.
- Auto scaling is for variable traffic.

---

## 5. Health Check Principles

### What Makes a Healthy Service

- HTTP 200 means the service is responding.
- Database connected means data is accessible.
- Dependencies OK means external services are accessible.
- Resources OK means CPU/memory are not exhausted.

### Health Check Implementation

- Simple: Just return 200
- Deep: Check all dependencies
- Choose based on load balancer needs

---

## 6. Security Principles

- Access: use SSH keys only, no passwords.
- Firewall: keep only necessary ports open.
- Updates: apply regular security patches.
- Secrets: use environment variables, not files.
- Audit: log access and changes.

---

## 7. Troubleshooting Priority

When something isn't working:

1. **Check if it's running** (process status)
2. **Check logs** (error messages)
3. **Check resources** (disk, memory, CPU)
4. **Check network** (ports, DNS)
5. **Check dependencies** (database, APIs)

---

## 8. Anti-patterns

- Don't run as root; use a non-root user.
- Don't ignore logs; configure log rotation.
- Don't skip monitoring; monitor from the start.
- Don't use manual restarts; configure auto-restart.
- Don't go without backups; maintain a regular backup schedule.

---

> **Remember:** A well-managed server is boring. That's the goal.

## Output Format

When providing server management guidance, structure the response as:

- **Decision summary**: What action to take and why, referencing the relevant decision table from this skill
- **Reasoning**: Which principle, scalability pattern, or troubleshooting step led to the recommendation
- **Implementation notes**: Relevant warnings from the anti-patterns table (no root, use auto-restart, verify backups) and any environment-specific considerations
- **Verification**: How to confirm the action worked — health check commands, log checks, or metric validation

## Limitations

This skill provides a reasoning framework, not a command reference:

- Does not provide operating-system-specific commands — it teaches the diagnostic thought process, not memorized CLI recipes
- Does not handle hardware-level or network-infrastructure issues (router configuration, physical server maintenance)
- Does not replace infrastructure-as-code tools (Ansible, Terraform, Puppet) — it helps decide what to do, not automate the doing
- Is designed for production server operations, not development environments
- Does not cover application-level debugging — server health is distinct from application bugs

