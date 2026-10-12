## Getting Started

[Template section for the launch blog post and documentation. Code sample showing basic usage.]

**Install:**

```bash
# pip / npm / homebrew / curl — one command only
pip install your-product
```

**First use — the shortest path to something real:**

```python
from your_product import Client

client = Client(api_key="your_key")

# 1. Create your first resource
job = client.jobs.create(name="import-orders", schedule="0 2 * * *")

# 2. Check it runs
print(job.status)   # "scheduled"
```

**What the developer should see within 5-10 minutes:**
- A successful call with a real result
- A clear way to check status or logs
- The docs page that explains the next step

**Rules of thumb:**
- Time from copy-paste to first successful call should be under 10 minutes (see Metrics Frameworks).
- Include the exact output the code produces, so developers can confirm it worked.
- Link forward, not sideways: one link to the next section (integration guide, API reference), not a wall of links.

**Common gotchas** (things that tripped early users, with the fix) — put them here rather than burying them in the FAQ.
