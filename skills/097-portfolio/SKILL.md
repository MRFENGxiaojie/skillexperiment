---
name: portfolio
description: Manages the IP portfolio — registrations, renewals, maintenance fees, and use declarations. Use when the user is checking what's renewing, adding or updating an asset, recording a maintenance filing, or auditing the register for gaps, lapses, and use-in-commerce questions. Receives handoffs from prosecution and clearance work.
argument-hint: "[--report [--days N] | --add | --update | --audit]"
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Portfolio

Surfaces what's renewing, adds assets, records filings, and audits the register.


## Instructions

1. **Follow the workflow below** and read the portfolio register
   (`~/.claude/plugins/config/claude-for-legal/ip-legal/portfolio.yaml`; if that
   location is not reachable — e.g. a sandboxed workspace — use `portfolio.yaml`
   in the current working directory instead).

2. **Default (no args):** equivalent to `--report` — show deadlines in the
   next 90 days grouped by urgency (🔴 lapsed/grace, ⏰ due within window,
   🟡 upcoming, 🌐 agent-managed, ❓ unknown).

3. **`--report [--days N]`:** Mode 2. Change the window with `--days`
   (30 / 60 / 90 / 180 typical). Always prepend the work-product header
   per CLAUDE.md → Outputs. Always close with the verification caveat.

4. **`--add`:** Mode 3. Walk through a new asset interactively — type,
   jurisdiction, number, dates, owner, business owner. Capture a custom
   rule if the jurisdiction isn't built in.

5. **`--update`:** Mode 4. Record that a maintenance filing or fee payment
   was made, sync with the IP management system, or change an asset's
   status. Enforce the consequential-action gate before setting any
   deadline to `filed`.

6. **`--audit`:** Mode 5. Broader health check — deadline hygiene,
   registration gaps, use-in-commerce questions on §8-approaching marks,
   owner inconsistencies, expiration horizon, unwatched marks.

7. **If the register is empty and an IP management system is connected:**
   Offer Mode 1 — pull the portfolio from the system of record and
   initialise the register.

8. **Guardrail reminder:** Computed deadlines are reference only. Every
   output closes with a line directing verification against the USPTO
   TSDR, WIPO, or relevant registry before filing or paying. A
   docketed-but-wrong deadline creates false confidence; do not let the
   user treat this as the system of record unless the IP management
   system is sync-integrated.


## Examples

```
/ip-legal:portfolio
```

```
/ip-legal:portfolio --report --days 180
```

```
/ip-legal:portfolio --add
```

```
/ip-legal:portfolio --update
```

```
/ip-legal:portfolio --audit
```

---


## Works better connected

This skill tracks deadlines from what you tell it. It works much better
connected to:

- **An IP management system (IPMS) via MCP** — Anaqua, Clarivate IPfolio,
  AppColl, Patrix, Alt Legal, FoundationIP. A connected IPMS gives you the
  full docket, maintenance fee schedules, and incoming correspondence in one
  place, instead of the register being whatever the lawyer remembers to
  paste. Ask your IPMS vendor if they have an MCP connector, or see
  `CONNECTORS.md` at the repo root for how to get one added.
- **USPTO directly via customer number** — pulls status, deadlines, and
  correspondence for your whole portfolio rather than one application at a
  time. Not currently available as an MCP; on the wish list in
  `CONNECTORS.md`.

Without either, paste your docket or upload a spreadsheet and I'll track from
there.


## Purpose

A trademark registration that isn't renewed on time can be cancelled. A patent
without its maintenance fee paid lapses. A domain that expires can be sniped
within the hour. All of this is avoidable, and all of it depends on one thing:
the right deadline is on someone's calendar, tied to the right registration
number, in the right jurisdiction.

This skill maintains that calendar.


## Important: deadline reference caveat

> The deadline rules this skill applies reflect publicly available requirements
> as of the skill's build date. IP office requirements, grace periods, fee
> structures, and maintenance schedules change. **Always confirm computed
> deadlines against the USPTO TSDR / Patent Center, WIPO Madrid Monitor /
> Patentscope, EUIPO eSearch, UKIPO online records, or the relevant national
> registry before acting.** If you use Anaqua, CPA Global, Clarivate, Alt Legal,
> or another IP management system, their docket is authoritative for your
> assets — use this tracker to organize and surface their data, not to replace
> it.
>
> A docketed-but-wrong deadline is worse than an undocketed one: it creates
> false confidence. "No deadline soon" outputs especially deserve a second
> look before you rely on them.


## Jurisdiction and type assumptions

Maintenance mechanics vary by jurisdiction and asset type:

- **US trademarks:** §8 Declaration of Use between 5th and 6th anniversary of
  registration (or §71 for Madrid designations), then combined §8/§9 renewal
  at 10 years and every 10 years thereafter. §15 Incontestability available
  after 5 years of continuous use. 6-month grace period with surcharge for §8
  and §9; no grace for the underlying use itself.
- **Madrid International trademarks:** 10-year registration term renewable at
  WIPO; individual designated countries may have local use or declaration
  requirements (e.g., US §71).
- **EUIPO trademarks:** 10-year renewal; 6-month grace with surcharge.
- **US utility patents:** Maintenance fees due at 3.5, 7.5, and 11.5 years
  from grant. 6-month grace window with surcharge; after that, potential
  revival by petition if lapse was unintentional.
- **US design patents:** No maintenance fees — 15-year term from grant for
  applications filed on or after May 13, 2015 (14 years if earlier). No action
  required mid-term.
- **EPO / national patents:** Annuities typically due annually from filing or
  from national phase entry. National rules vary — confirm per jurisdiction.
- **US copyright:** No maintenance for works created 1978 or later.
  Pre-1978 works may have had renewal obligations; flag for attorney review
  if the asset pre-dates 1964 (rarely in scope for modern portfolios).
- **Domains:** Annual or multi-year renewal per registrar; typical 30-day
  grace then redemption period (~30 days at high fee) then drop.

If the portfolio includes assets in jurisdictions not listed above, capture
the maintenance mechanic in the register's `custom_rules` block and the
report will surface them as `agent_managed` — confirm status with the
foreign associate rather than computing a date this skill doesn't understand.

---


## The register

Lives at `~/.claude/plugins/config/claude-for-legal/ip-legal/portfolio.yaml`
(fallback when that path is not reachable: `portfolio.yaml` in the current
working directory).
Structure:

```yaml
# IP Portfolio Register
# Generated: [date]
# Last updated: [date]
# Disclaimer: computed deadlines are reference only — confirm with USPTO/WIPO/
# relevant registry or the IP management system of record before acting.

metadata:
  company: "[Company Name]"
  generated: "[date]"
  last_updated: "[date]"
  last_audit: "[date or null]"
  source_system: "[Anaqua / CPA Global / manual / none]"

custom_rules:   # non-built-in jurisdictions captured manually
  []

assets:
  - id: "TM-US-001"
    type: "trademark"                          # trademark / patent / copyright / design / domain
    jurisdiction: "US"
    mark_or_title: "[Mark or title]"
    owner: "[Record owner — registered entity name]"
    status: "registered"                       # pending / registered / lapsed / abandoned / cancelled
    application_number: "[number or null]"
    registration_number: "[number or null]"
    classes: ["9", "42"]                       # Nice classes for TM; CPC/IPC for patents; null otherwise
    filing_date: "[YYYY-MM-DD or null]"
    registration_date: "[YYYY-MM-DD or null]"
    priority_date: "[YYYY-MM-DD or null]"
    grant_date: "[YYYY-MM-DD or null]"         # patents
    next_deadlines:                            # computed; refreshed on --report and --audit
      - type: "§8 Declaration of Use"
        due_date: "[YYYY-MM-DD]"
        grace_end: "[YYYY-MM-DD or null]"
        basis: "5th-6th anniversary of registration"
        action: "File §8 Declaration of Use (or excusable nonuse)"
        status: "upcoming"                     # upcoming / due_soon / overdue / grace / filed
    use_in_commerce: true                      # TM only — drives §8 analysis
    agent_managed: false                       # true for foreign associate / outside counsel managed
    local_agent: null
    docket_id: "[IP-mgmt-system ID or null]"
    outside_counsel: "[firm or null]"
    business_owner: "[email or team]"
    notes: ""

  - id: "PAT-US-001"
    type: "patent"
    jurisdiction: "US"
    mark_or_title: "[Invention title]"
    owner: "[Owner]"
    status: "granted"
    application_number: "[number]"
    registration_number: "[patent number]"
    filing_date: "[YYYY-MM-DD]"
    grant_date: "[YYYY-MM-DD]"
    priority_date: "[YYYY-MM-DD or null]"
    expiration_date: "[YYYY-MM-DD]"            # 20 years from earliest non-provisional filing
    next_deadlines:
      - type: "3.5-year maintenance fee"
        due_date: "[YYYY-MM-DD]"
        grace_end: "[YYYY-MM-DD]"
        basis: "3.5 years from grant"
        action: "Pay maintenance fee (small/micro entity if applicable)"
        status: "upcoming"
    claims_count: 20
    entity_size: "large"                       # large / small / micro (drives USPTO fees)
    docket_id: null
    outside_counsel: null
    business_owner: null
    notes: ""
```

Status values for `next_deadlines`:
- `upcoming` — more than 90 days out
- `due_soon` — due within 90 days, not yet filed
- `overdue` — past the primary due date, within grace window (if any)
- `grace` — in the grace period (explicit flag — carries surcharge)
- `lapsed` — past grace with no action; asset effectively lost unless revivable
- `filed` — action completed this cycle

---


## Mode 1: Initialise

Run when no register exists, or with `--rebuild`.

### Step 1: Determine the source

Read the practice config (`~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`; if it is not reachable, skip it and use the defaults below):
- **IP management system connected** (Anaqua, CPA Global, etc.): pull the portfolio via its integration. The IP system is the authoritative source; this register mirrors it and adds no deadlines the system doesn't already have.
- **No IP management system, but spreadsheet / export available:** import what's present; flag any asset missing a registration or grant date as `unknown` for deadline computation.
- **Nothing at hand:** walk through assets interactively — type, jurisdiction, number, key dates, owner.

### Step 2: For each asset, compute deadlines

Apply the rules at the top of this file. Populate `next_deadlines` with the
two or three closest upcoming items — further-out deadlines (10-year renewals
decades away) are computed on demand during reports rather than stored
speculatively.

**For assets the skill cannot confidently schedule:**
- Unknown jurisdiction rules → add a stub under `custom_rules` and flag the
  asset `agent_managed: true` with a TODO to confirm with the foreign associate.
- Missing dates needed for computation (no grant date for a patent, no
  registration date for a TM) → set `next_deadlines` empty with a note in
  `notes`, and list the asset as `unknown` in the initialisation summary.

### Step 3: Write the register

Generate `portfolio.yaml` at the config path. Show a summary:

```
Portfolio register initialised.

Assets: [N]
  Trademarks: [N]   ([N registered] / [N pending])
  Patents:    [N]   ([N granted] / [N pending])
  Copyrights: [N]
  Designs:    [N]
  Domains:    [N]

Deadlines computed: [N]
Agent-managed / jurisdiction TBC: [N] — confirm with foreign associates
Unknown (missing key dates): [N] — fill in before relying on reports

Run /ip-legal:portfolio --report to see what's due.
```

---


## Mode 2: Report

```
/ip-legal:portfolio --report [--days 30|60|90|180]
```

Default window: 90 days. Refresh computed deadlines for every asset before
producing the report — don't rely on stored dates alone.

Output (prepend the work-product header per CLAUDE.md → Outputs when that config is reachable):

```
IP PORTFOLIO DEADLINE REPORT — [date]
[Company Name] — window: next [N] days

🔴 LAPSED / IN GRACE ([N])
  [Asset ID] / [Jurisdiction] / [Type] / [Mark or title]
    [Action] — original due [date], grace ends [date]
    Status: [grace / lapsed]

⏰ DUE WITHIN [N] DAYS ([N])
  [Asset ID] / [Jurisdiction] / [Type] / [Mark or title]
    [Action] — due [date]
    Basis: [e.g., "5th-6th anniversary of registration"]
    [Agent: firm / docket: id — if present]

🟡 UPCOMING (next window beyond 30 days, within [N] days)
  [list]

🌐 AGENT-MANAGED ([N])
  [Asset ID] / [Jurisdiction] — managed by [local agent]; confirm directly
  [Asset ID] / [Jurisdiction] — no local agent recorded; add with --update

❓ UNKNOWN ([N])
  [Asset ID] — missing [field]; cannot compute deadline
  Confirm with [IP management system / USPTO TSDR / relevant registry] before relying on this report.

SUMMARY
  Total assets tracked: [N]
  Deadlines in window: [N]
  Last audit: [date]
```

Close the report with the caveat line: *"Computed from portfolio register. Verify each deadline against the USPTO/WIPO/registry of record before filing or paying."*

If the report lists more than ~10 assets, or any time the user asks: offer the dashboard (see CLAUDE.md `## Outputs → Dashboard offer for data-heavy outputs`). Shape the offer for this output — counts by registration status (live / in grace / lapsed / pending), a deadline timeline, and a sortable portfolio table with jurisdiction, type, and next-action date.

---


## Mode 3: Add

```
/ip-legal:portfolio --add
```

Interactive add of a single asset. Ask for:
1. Type (trademark / patent / copyright / design / domain)
2. Jurisdiction
3. Mark or title / invention name
4. Owner (record owner — matters for §8 filings and assignments)
5. Key dates (per type: filing, registration, grant, priority, expiration)
6. Number(s)
7. Classes / claims count
8. Source — is this being tracked in the IP management system under a docket ID?
9. Outside counsel / foreign associate, if any
10. Business owner (who does this matter to — product line, brand manager)

After capture:
- Compute next deadlines per the rules at the top of this file.
- If jurisdiction rules aren't built in, walk through the `custom_rules` capture flow (see below).
- Append to `assets:` in `portfolio.yaml`.

### Custom rules capture

When a jurisdiction isn't in the built-in list:

> I don't have maintenance rules for [Jurisdiction] / [Asset type] built in.
> Let me capture them so we can track this going forward.
>
> 1. What maintenance events apply? (Renewal every N years? Annuities annually?
>    Declarations of use? Something else?)
> 2. What triggers the due date — filing date, registration date, grant date,
>    national phase entry, anniversary of something else?
> 3. Is there a grace period? At what cost?
> 4. Is there a foreign associate or local agent managing this?

Store under `custom_rules:` and apply to future assets in that jurisdiction.

---


## Mode 4: Update

```
/ip-legal:portfolio --update
```

### Consequential-action gate

**Before recording that a maintenance filing or fee payment was made:** Read
`## Who's using this` in the practice config (`~/.claude/plugins/config/claude-for-legal/ip-legal/CLAUDE.md`). If the config is not reachable, treat the role as unknown and apply the gate conservatively. If the Role is **Non-lawyer**:

> Recording a §8 declaration, a §9 renewal, a patent maintenance fee payment,
> or an international annuity as "filed" has consequences. If the record is
> wrong — missed due date, wrong entity size, wrong specimen of use — the
> deadline doesn't move, and the asset can still lapse. Have you confirmed
> this with the attorney or foreign associate who actually made the filing
> (or with the USPTO TSDR / WIPO Madrid Monitor / relevant registry)? If yes,
> proceed. If no:
>
> - Do not record as filed yet.
> - Here is what to bring to the attorney: asset ID, jurisdiction, deadline
>   type, what the IP management system shows, what you believe was filed and
>   when, and the source of that belief.
>
> If you need to find a licensed attorney, solicitor, barrister, or other authorised legal professional in your jurisdiction: your professional regulator's referral service
> is the fastest starting point (state bar in the US, SRA/Bar Standards Board in England & Wales, Law Society in Scotland/NI/Ireland/Canada/Australia, or your jurisdiction's equivalent).

Do not set a deadline's `status` to `filed` past this gate without an
explicit yes. Status refresh, report generation, and upcoming-deadline
surfacing do not require the gate.

### Sub-modes

**Manual update:** "We filed the §8 for TM-US-001 on March 4, specimen
attached." Update the matching deadline: `status: filed`, `filed_date`,
and compute the next deadline in its lifecycle (for §8 that's the §9
renewal 10 years out).

**From IP management system sync:** If Anaqua / CPA Global / similar is
connected, pull the latest docket and reconcile. Flag mismatches between
the register and the system of record — the system of record wins; update
the register to match and surface anything the register had that the
system doesn't.

**Status change:** "Mark TM-US-004 as abandoned." Update `status`, clear
`next_deadlines`, note the date abandoned.

---


## Scope / What This Skill Does Not Do

- It does not file anything. Every action it surfaces is for the attorney or foreign associate to execute.
- It does not verify deadlines against the USPTO TSDR, WIPO, or any other registry. It computes them from the dates you give it. The register is a working copy; the registry is the source of truth.
- It does not decide whether to renew. This skill surfaces the deadline and the cost; the business and attorney decide.
- It does not replace an IP management system for multi-hundred-asset portfolios. Best suited for smaller portfolios, or as a lightweight layer surfacing what the system of record shows.
- It does not read office records to verify status. A §8 shown as "filed" here means someone told it so — not that the USPTO accepted it.

## Reference Files

- **Handoffs**: see [references/handoffs.md](references/handoffs.md)
- **Integration Ip Renewal Watcher Agent**: see [references/integration-ip-renewal-watcher-agent.md](references/integration-ip-renewal-watcher-agent.md)
- **Mode 5 Audit**: see [references/mode-5-audit.md](references/mode-5-audit.md)
