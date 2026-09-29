## The Problem

[Template section for the launch blog post and messaging. Describe the developer pain point in technical detail.]

**Write it like an engineer would:**

1. **Name the pain concretely** — the task that takes too long, the failure mode that costs time, the workaround developers are stuck with.
   - Weak: "Developers struggle with slow data pipelines."
   - Strong: "Teams spend 2+ hours a day hand-repairing failed pipeline runs and replaying stuck jobs — errors surface in logs hours after the fact."

2. **Give it numbers** — latency, error rates, hours lost, or team size involved. Numbers make the problem measurable and the solution credible.
   - "p99 recovery time is 40 minutes per incident, and a typical team sees 6-8 incidents per week."

3. **Say who it hurts** — the specific developer persona (backend engineers, platform teams, ML engineers) and why existing alternatives fall short.
   - "Off-the-shelf schedulers assume single-run jobs; retries either replay the whole run or require hand-written idempotency logic."

4. **Connect it to business impact** — in one line: what the pain costs the team or the company.

Keep this section factual. If you can't state the problem in concrete terms, the rest of the announcement will not land.
