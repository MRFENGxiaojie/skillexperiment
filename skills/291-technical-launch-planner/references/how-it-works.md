## How It Works

[Template section for the launch blog post and documentation. Technical architecture, with diagram.]

**Component view (replace with your own diagram):**

```
[Client / CLI] ──► [API Gateway] ──► [Core Service] ──► [Worker Pool]
                                          │                 │
                                          ▼                 ▼
                                     [State Store]    [Message Queue]
                                          │                 │
                                          ▼                 ▼
                                     [Monitoring]     [Durable Logs]
```

**Explain each component in one or two lines:**
- What it is and its responsibility
- How it connects to the neighbors
- The key design decision (why this shape)

**Walk through the main flows:**

1. **Happy path** — request comes in, what executes, what the developer observes.
2. **Failure path** — what happens when a step fails, how state is preserved, what retry looks like.
3. **Scaling path** — how the system behaves under load, where the bottlenecks are and how they are handled.

**Config and code shapes:** show the minimal config or API surface a developer actually writes, not the internals.

This section earns trust when it shows real mechanics (state transitions, data flow, guarantees) rather than a generic three-box architecture. If a guarantee is claimed (exactly-once, ordering, durability), show the mechanism that provides it.
