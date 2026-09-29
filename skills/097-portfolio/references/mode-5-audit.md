## Mode 5: Audit

```
/ip-legal:portfolio --audit
```

Broader health check beyond this month's deadlines:

**Deadline hygiene**
- Any deadlines in `grace` status right now? (In progress but surcharge-costing.)
- Any `lapsed` assets that aren't marked `abandoned` or `cancelled`? Either
  revive or update status.
- Any assets with no `next_deadlines` computed? Either missing data or a
  jurisdiction the skill doesn't know.

**Registration gaps**
- Trademark applications filed more than 18 months ago still `pending`?
  Flag for status check at the office — may need response to an action.
- Patents filed more than 4 years ago still `pending`? Flag for prosecution
  check.

**Use-in-commerce (TM only)**
- §8 approaching on a mark flagged `use_in_commerce: false` or uncertain?
  The §8 requires use; mark needs a use audit before filing or an excusable
  nonuse declaration.

**Ownership hygiene**
- Any assets where the `owner` is not a currently active entity per the
  entity register (if available)? Flag — may need recordal of assignment.
- Owner name inconsistencies across assets (same entity, different name
  strings)? Surface for cleanup.

**Expiration horizon**
- Any patents expiring in the next 24 months? Even without a maintenance
  deadline, the business may want to know — product planning, continuation
  strategy, licensing window.

**Unwatched assets**
- Any registered marks not on the watch list in CLAUDE.md → Brand protection?
  Flag as a gap for the attorney to decide whether to add.

Output format:

```
IP PORTFOLIO AUDIT — [date]

DEADLINE HYGIENE
  In grace: [N] — acting now avoids lapse
  Lapsed (not marked abandoned): [N] — confirm status
  Missing next-deadline computation: [N] — fill data or mark agent-managed

REGISTRATION GAPS
  TM applications pending >18 months: [list]
  Patent applications pending >4 years: [list]

USE IN COMMERCE (TM)
  §8 approaching on uncertain-use marks: [list]

OWNERSHIP
  Assets with unrecognised owner strings: [N]
  Owner name inconsistencies: [list]

EXPIRATION HORIZON (24 months)
  Patents expiring: [list]

BRAND WATCH
  Registered marks not on watch list: [list]

RECOMMENDED ACTIONS
  1. [highest priority]
  2. [etc.]
```

---