---
name: tpl-situacao-deployment-devops
description: Guides the agent in setting up and improving deployment pipelines. Use when the user is configuring CI/CD, environments, secrets management, health checks, rollbacks, or preparing for a production go-live.
allowed-tools: Read, Write, Bash, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# SITUATION: Deployment & DevOps Pipeline Setup

## WORKFLOW

1. **Identify the situation.** Match the user's deployment problem to a row in the ROUTING TABLE; if several rows apply, use the priority note beneath it.
2. **Hold the seven principles.** Every plan must satisfy them: cattle not pets, environment parity, artifact deploys, feature flags, health checks, monitoring first, practiced rollback.
3. **Run the pre-deploy checklist.** Code, environment, monitoring, and rollback readiness all pass before anything ships.
4. **Choose a zero-downtime strategy.** If traffic must not drop, pick a strategy from the table and configure the matching readiness probes.
5. **Build the pipeline.** Adapt the GitHub Actions template — add concurrency control and a rollback entry point.
6. **Produce the Deployment Record.** Fill the OUTPUT FORMAT template: changes, pre-deploy checklist, timeline, post-deploy metrics.
7. **Verify the quality gates.** All ten must pass; if one fails, stop and fix before releasing.

1. **Every environment is cattle, not pets.** Environments must be reproducible from code and configuration. If a server needs manual steps to configure, that knowledge is lost when the server is replaced.

2. **Environment parity is non-negotiable.** Staging must mirror production in: OS, runtime versions, database engine and version, memory/CPU class (within budget). Any difference is a potential "works in staging" failure.

3. **Deploy from artifacts, not from source.** Build once, deploy the artifact. Never run `npm install` or build steps on production servers. The artifact that passes staging is the artifact deployed to production.

4. **Feature flags over long-lived branches.** If a feature is too risky to deploy to all users, use a feature flag. Don't maintain a branch for months. Dark launch → canary → full rollout.

5. **Health checks are load-balancer ready before deployment.** Every service must expose a `/health` endpoint that returns 200 when healthy. The load balancer must be configured to stop routing traffic to unhealthy instances.

6. **Monitoring is a prerequisite for go-live, not a follow-up task.** If you cannot observe the service after deployment, you cannot safely deploy. Error rate, latency P95, and CPU/memory must be visible on a dashboard before the first production deployment.

7. **Rollback must be practiced.** Run a rollback drill in staging before the first production deployment. The procedure must be documented and under 10 minutes.

## ROUTING TABLE

- If you encounter secrets in code or config files: stop everything, move to secrets manager (AWS Secrets Manager, Vault, GitHub Secrets), and rotate all exposed secrets.
- If you encounter `npm install` running on production server: it is the wrong pattern; build Docker image in CI, push to registry, deploy the image.
- If you encounter no staging environment: create one before continuing, because deployments without staging are exploratory surgery without anesthesia.
- If you encounter database migration as part of deployment: run migrations BEFORE deploying new code, using expand-contract, and never migrate during traffic spike.
- If you encounter manual approval gate before production: use protected environments in GitHub Actions and require explicit approval from named individuals.
- If you encounter "Works on my machine" reports: standardize on Docker for local development, since if it runs in Docker locally it runs the same way in CI.
- If you encounter no rollback procedure documented: write rollback procedure, test it in staging, and link it from deployment runbook.
- If zero-downtime deployment is needed: use rolling update, blue-green deployment, or canary deployment, and configure readiness probes.
- If long-running deploy causes downtime: implement graceful shutdown signal handling, connection draining (30s), and health check that returns unhealthy before process exits.
- If a new team member deploys for the first time: pair program the first deploy, and the runbook must be sufficient for them to do it alone the second time.

If multiple rows apply, resolve in this order: (1) secrets in code — stop everything; (2) missing staging — create first; (3) rollback missing — document before deploy; then follow remaining rows.

## Deployment Checklist (Pre-Deploy)

### Code Readiness
- [ ] All CI checks passing (lint, tests, build, security scan)
- [ ] PR reviewed and approved
- [ ] Database migrations written and tested on staging
- [ ] Feature flags configured (if applicable)
- [ ] `CHANGELOG.md` updated

### Environment Readiness
- [ ] Secrets updated in secrets manager (if changed in this release)
- [ ] External service credentials valid and tested
- [ ] Staging deployment successful with E2E smoke tests passing
- [ ] Database backup confirmed (before migration-heavy releases)

### Monitoring Readiness
- [ ] Dashboards displaying current baseline metrics
- [ ] Alert thresholds defined: error rate > 1%, P95 latency > 2s
- [ ] On-call person informed of deployment
- [ ] Runbook link bookmarked for quick access

### Rollback Readiness
- [ ] Previous version artifact available in registry
- [ ] Rollback procedure documented and accessible
- [ ] Database rollback script prepared (if migration involved)
- [ ] Decision criteria defined: what metric/threshold triggers rollback?

## Zero-Downtime Deployment Strategies

- Rolling Update is used for stateless services with N instances, has low complexity, and has fast rollback speed (redeploy old version).
- Blue-Green is used for critical services that need instant cutover, has medium complexity, and has instant rollback speed (switch load balancer).
- Canary is used for high risk change that needs gradual validation, has high complexity, and has fast rollback speed (remove canary).
- Feature Flag is used when code is shipped but not activated, has low complexity, and has instant rollback speed (toggle flag).

Quick verification commands:

```bash
docker build -t app:$SHA .
kubectl rollout status deploy/app --timeout=5m
curl -sf http://host/health && echo healthy
```

## CI/CD Pipeline Template (GitHub Actions)

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

concurrency:
  group: production-deploy
  cancel-in-progress: false

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build

  deploy-staging:
    needs: test
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging ${{ github.sha }}
      - name: Run smoke tests
        run: npm run test:smoke -- --env staging

  deploy-production:
    needs: deploy-staging
    environment: production  # Requires manual approval
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh production ${{ github.sha }}
      - name: Verify health checks
        run: ./scripts/verify-health.sh production

# Rollback entry point: pair this workflow with a rollback.yml (workflow_dispatch)
# that redeploys the previous version's artifact — rollback must stay under 10 minutes (Principle 7).
```

## DO NOT

- **DO NOT** deploy on Fridays or before holidays unless it's an emergency hotfix
- **DO NOT** deploy without a monitoring dashboard open and visible
- **DO NOT** deploy during high-traffic hours — choose low-traffic windows
- **DO NOT** skip staging — ever
- **DO NOT** manually modify production servers — all changes through code
- **DO NOT** store secrets in environment variables baked into Docker images
- **DO NOT** deploy without notifying the on-call person
- **DO NOT** run database migrations and deploy application code in the same step

## OUTPUT FORMAT

For each deployment, produce a **Deployment Record**:

```markdown
## Deployment Record

**Version:** v2.4.1
**Environment:** Production
**Date:** 2024-01-15 14:30 UTC
**Deployer:** [name]
**Changes:** [link to CHANGELOG / PR list]

### Pre-Deploy Checklist
[x] All CI checks passing
[x] Staging deployment successful
[x] Database migrations tested on staging
[x] On-call notified
[x] Rollback procedure accessible

### Deployment Timeline
- 14:30: Migration started
- 14:32: Migration complete. Row counts verified.
- 14:33: Rolling update started (3 of 5 instances updated)
- 14:36: Rolling update complete. All instances healthy.
- 14:37: Smoke tests passed.

### Post-Deploy Metrics (15 min observation)
- Error rate: 0.02% (baseline: 0.01%) ✅
- P95 latency: 245ms (baseline: 230ms) ✅
- CPU: 42% (baseline: 38%) ✅

**Status: Successful ✅**
```

## SCOPE AND LIMITATIONS

This skill covers deployment pipeline setup and improvement: CI/CD, environments, secrets management, health checks, zero-downtime strategies, and rollback.

It does NOT cover:
- **Infrastructure provisioning** — creating cloud resources (Terraform, VPCs, clusters) is a different task; this skill deploys into infrastructure that already exists
- **Security penetration testing** — secrets hygiene is in scope; vulnerability exploitation and security audits are not
- **Cost optimization / FinOps** — right-sizing, spend analysis, and budget guardrails are separate concerns
- **CI platforms other than GitHub Actions** — the template targets GitHub Actions; adapt it for GitLab CI, Jenkins, or CircleCI instead of using it as-is
- **On-call incident response** — this skill makes a deployment safe to release; it does not run the response when the release fails

The pipeline template assumes the repository provides `scripts/deploy.sh` and `scripts/verify-health.sh` (deploy: env + git SHA; verify: env + curl /health) — create them before using the template as-is.

## QUALITY GATES

- [ ] Deploy pipeline fully automated — zero manual SSH steps
- [ ] `/health` endpoint returns 200 on healthy instance, 503 on unhealthy
- [ ] Rollback tested in staging before first production deploy
- [ ] Zero secrets in codebase, config files, or Docker images
- [ ] Staging and production have matching runtime versions (verify: `node --version`)
- [ ] Monitoring dashboard created and showing pre-deploy baseline
- [ ] Deployment runbook accessible to all team members
- [ ] Recovery time < 10 minutes for standard rollback scenario
- [ ] CI build produces immutable artifact tagged with git SHA
- [ ] Deployment notification sent to team channel on success/failure

