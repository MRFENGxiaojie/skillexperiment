---
name: demand-received
description: Triage an inbound demand letter — extract fields, cross-check the portfolio, assess merit, present response options with a recommendation, and hand off to matter-intake or demand-intake if escalation is warranted. Use when the user says "we got a demand letter", "triage this demand", or shares an incoming demand to evaluate.
argument-hint: "[path-to-incoming] [--slug=custom-slug]"
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

## Quick Start

Quick reference — full detail in `## Workflow` Steps 1–7.

1. Read the incoming document from provided path.
2. Load `~/.claude/plugins/config/claude-for-legal/litigation-legal/matters/_log.yaml` for portfolio cross-check.
3. Load `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` → risk calibration, landscape, demand-letter practice.
4. Follow the workflow and reference below.
5. Extract fields; cross-check portfolio; assess merit; present options with recommendation.
6. Write `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/[slug]/triage.md`. Copy or link incoming to `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/[slug]/incoming.[ext]`. If the plugin inbound directory is unreachable, write to `./inbound/[slug]/triage.md` in the workspace instead.
7. Hand off per user choice:
   - Create matter → `matter-intake` pre-populated
   - Respond with counter-demand → `demand-intake` pre-populated
   - Link to existing matter → update `related_matters` in log
   - Standalone → no further action

# Demand Received

## Purpose

Inbound demand letters are the bread and butter of an in-house litigation practice. A small fraction need escalation; most can be handled with a structured response or a holding letter. The failure mode is treating them all alike. This skill triages, cross-checks the portfolio, and produces options.

## Load context

- The incoming document (user provides path or drops it in-session)
- `~/.claude/plugins/config/claude-for-legal/litigation-legal/matters/_log.yaml` — scan for related matters (same counterparty, overlapping counterparties via entity relationships, or matter type + recent date)
- `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` → risk calibration (for merit assessment), landscape (is the sender a frequent adversary?), demand-letter practice (house tone and response defaults)

If the plugin configuration at `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` exists, load it and follow its `## Risk calibration`, `## Landscape`, and `## Demand-letter practice` sections. If it does not exist (no firm config mounted), proceed with the session-provided facts and note at the top of the triage: "Firm config not loaded — risk calibration and landscape defaults per this skill applied."

## Workflow

### Step 1: Read the demand

Extract from the incoming:

- **Sender** — entity, signer, counsel (if signed by outside firm)
- **Recipient** — which entity/person at our company
- **Delivery** — certified, email, courier (matters for deadline calculation)
- **Date received** vs. **date signed**
- **Demand type** — payment, breach/cure, C&D, preservation, settlement, other
- **Specific asks** — what they want, by when
- **Facts alleged** — their version of what happened
- **Legal basis** — statutes, contract provisions, theories they cite
- **Threats** — what they say they'll do if we don't comply
- **Settlement-communication framing** — research the settlement-communication protections applicable in the forum (FRE 408 in federal, the state equivalent otherwise). Note whether the demand is marked as a settlement communication, but remember: protection attaches from conduct and context, not merely from labeling. Capture both the label (if any) and a first-pass read of whether the substance is in fact a compromise discussion.

### Step 2: Portfolio cross-check

Search `_log.yaml` for:

- **Direct match** — matter with same counterparty (their slug matches the sender)
- **Type match** — similar matter type with this counterparty in the past (closed matters count — they inform pattern)
- **Subject overlap** — matters where the subject might be the same dispute (e.g., same contract, same product, same project)

Present findings:

- If the incoming demand is a direct match and the existing matter is active, it is almost certainly the same matter; add the incoming to the existing matter rather than creating a new one, and update `related_matters` if the incoming demand is a tangent (different subject but same counterparty) rather than the same dispute.
- If the incoming demand is a direct match and the existing matter is closed, the counterparty is back — it may be a new dispute or a resurrected one; open a new matter, or reopen/amend the closed one, as the user decides.
- If the incoming demand is a type match, it is precedent or context; it is probably a distinct matter, and it should inform the response strategy.
- If there is no match, the demand is novel; treat it as fresh.

If `_log.yaml` does not exist or is empty, state "Portfolio log not loaded — cross-check unavailable" in the triage's Portfolio cross-check section and proceed with the direct-match / type-match analysis based on session knowledge, each finding tagged `[model knowledge — verify]`.

### Step 3: Merit assessment

Not a legal opinion — a structured read:

- **Facts** — do the alleged facts align with what we know? Where's the disconnect?
- **Legal basis** — are the cited provisions/statutes actually applicable? (Flag cites for user verification — do not attempt to validate law autonomously.)
- **Strength on their side** — if they went to court tomorrow, what's their story?
- **Strength on our side** — what are our likely defenses?
- **Damages demanded vs. likely** — is the ask proportionate to what a court would award if they won?
- **Leverage and pressure** — are they credibly prepared to sue? Do they have capacity? Are they a repeat-litigant adversary per `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md`?

Output a triage rating: **substantial merit / debatable / weak / frivolous**. Be blunt. The user is triaging, not writing the brief.

### Step 4: Response options

Present 3-4 options with tradeoffs:

- Option A — substantive response: use it when the demand has merit or is at least debatable and a reasoned reply protects the record; the tradeoff is that it commits us to a position in writing; the next step is `/demand-intake` with pre-populated fields for a counter-response letter.
- Option B — holding letter: use it when you need time to investigate and don't want to concede anything or trigger their deadline math; it doesn't resolve anything but buys 2-4 weeks; the next step is a short acknowledgment draft.
- Option C — settlement response: use it when early resolution is cheaper than litigation and you are willing to discuss without admitting; it requires a settlement-communication posture — research the applicable rule (FRE 408 or state equivalent) and structure the response so the substance, not just the label, qualifies as a compromise discussion, and be careful not to waive claims; the next step is `/demand-intake` with `type: settlement-response`.
- Option D — ignore + preserve: use it when the demand is frivolous or the deadline doesn't create legal prejudice; note that silence can be used against us in some contexts (e.g., account stated) and a legal hold is still required; the next step is to issue a legal hold via `/legal-hold --issue` if not already done, then log the demand and move on.

Recommend one. Be specific about why.

### Step 5: Deadline triage

- **Their stated deadline** — note it, but it doesn't bind us
- **Our internal deadline** — when we must decide (often: stated deadline minus 5 business days to draft + approve)
- **Legal deadlines** — statute of limitations, contractual cure periods, procedural requirements

Flag any legal deadlines that are tight. Calendar them.

**No silent supplement.** If the inbound demand cites rules, cases, or statutes that require verification, and a research query to the configured legal research tool (Westlaw, CourtListener, Trellis, Descrybe, or firm platform) returns few or no results for a given authority, report what was found and stop. Do NOT fill the gap from web search or model knowledge without asking. Say: "The search returned [N] results from [tool]. Coverage appears thin for [cite / doctrine]. Options: (1) broaden the search query, (2) try a different research tool, (3) search the web — results will be tagged `[web search — verify]` and should be checked against a primary source before relying, or (4) leave the `[SME VERIFY]` flag and stop here. Which would you like?" A lawyer decides whether to accept lower-confidence sources; the skill does not decide for them.

**Source attribution.** Tag every citation carried into the triage — including the sender's cited authorities, our response-option rationales, and any research pulled for merit assessment — with where it came from: `[Westlaw]`, `[CourtListener]`, `[Trellis]`, `[Descrybe]`, or the MCP tool name for citations retrieved from a legal research connector; `[web search — verify]` for web-search citations; `[model knowledge — verify]` for citations recalled from training data; `[user provided]` for citations supplied in the demand itself. Citations tagged `verify` carry higher fabrication risk and should be checked first. Never strip or collapse the tags. The template's `## Legal basis cited` section carries these tags inline with each citation.

### Step 6: Write triage

Output: `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/[slug]/triage.md`, per the template in `## Output format`. If the plugin inbound directory is unreachable, write to `./inbound/[slug]/triage.md` in the workspace and note the relocation in the triage header.

If the plugin `## Outputs` section is unavailable, use the header format shown in the template and note "house header conventions not loaded" in the triage header.

### Step 7: Hand off

Handoff pipeline: this skill ends at the triage decision → `demand-intake` pre-populates the counter-response intake (Options A/C) → letter drafting happens in `demand-draft`. `matter-intake` is only for new-matter creation.

Based on recommendation and user confirmation:

- Matter creation → hand off to `/matter-intake` with: counterparty, type, `source: demand-letter` (inbound), initial theory framed defensively, pre-populated.
- Counter-response as outbound demand → hand off to `/demand-intake` with: counterparty, context from triage, desired outcome as the response.
- Link to existing matter → update that matter's `related_matters` in `_log.yaml`; append event to its `history.md`.
- Standalone → leave in `~/.claude/plugins/config/claude-for-legal/litigation-legal/inbound/`; no portfolio change.

## Output format

Write the triage in exactly this format:

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role; see `## Who's using this`]

> **Privilege inheritance.** This triage is derived from the inbound demand and from the portfolio log, and it records our first-pass merit read and response posture. Those internal analyses are attorney-client and/or work-product material. Distributing this triage beyond the privilege circle — including forwarding it to the business lead without marking, sharing with the counterparty, or attaching to an insurance tender without scrubbing — can waive protection over both this document and the reasoning inside it. Store with privileged matter material, mark consistently with house privilege conventions, and make distribution decisions deliberately.

# Demand Received — Triage

> **READ FOR TRIAGE, NOT OPINION.** This document is an intake scan and an options analysis — not a legal merit opinion. The `Triage rating` below is a structured read to support the counsel's decision on how to route the demand. It is not a recommendation on the merits and does not substitute for case-specific legal analysis. Every cited statute, rule, or case is flagged for SME verification; every merit call is the counsel's, not this skill's.

**Slug:** [slug]
**Received:** [YYYY-MM-DD]
**Received by:** [entity / person]
**Incoming file:** [path]

---

## The demand

**Sender:** [entity, signer, counsel]
**Demand type:** [type]
**Specific asks:** [list]
**Their stated deadline:** [date]
**Settlement-communication framing:** [labeled / substantively / neither / ambiguous] — *protection turns on conduct and context, not the label; `[SME VERIFY]` against the forum's applicable rule*

## Facts alleged

[their version, in one paragraph]

## Legal basis cited

[citations — each tagged with its source tag (`[Westlaw]`, `[CourtListener]`, `[Trellis]`, `[Descrybe]`, MCP tool name, `[web search — verify]`, `[model knowledge — verify]`, or `[user provided]`) plus the verification flag `[SME VERIFY: applicability / currency / jurisdiction]` — do not rely on any citation here without independent check]

Example: `[citation]` — tagged `[user provided]`, `[SME VERIFY: applicability / currency / jurisdiction]`

## Threats / next steps they state

[list]

---

## Portfolio cross-check

**Direct match:** [slug if exists, or "none"]
**Type match / precedent:** [list or "none"]
**Subject overlap:** [list or "none"]
**Recommendation:** [new matter / add to existing / link via related_matters / standalone inbound]

---

## Merit assessment

**Facts:** [alignment with our version; disconnects]
**Legal basis:** [applicability, with flags — each citation tagged with its source first, then `[SME VERIFY]`]
**Their case if litigated:** [one paragraph]
**Our defenses:** [one paragraph]
**Damages proportionality:** [assessment]
**Credibility of threat:** [will they sue? capacity? repeat litigant?]

**Triage rating:** [substantial / debatable / weak / frivolous] — *structured read for routing, not a merit opinion; `[SME VERIFY: counsel to confirm before relying on this]`*

---

## Response options

### A. Substantive response
[Rationale, tradeoffs, next step]

### B. Holding letter
[Rationale, tradeoffs, next step]

### C. Settlement response
[Rationale, tradeoffs, next step]

### D. Ignore + preserve
[Rationale, tradeoffs, next step]

**Recommendation:** [A/B/C/D] — [two sentences why] — `[SME VERIFY: counsel to confirm before executing]`

---

## Deadlines

- **Their stated deadline:** [date]
- **Our internal decision deadline:** [date]
- **Legal deadlines:** [SoL, cure periods, procedural — with dates]

---

## Immediate actions

- [ ] Legal hold issued — [yes/no] — if no, run `/legal-hold [slug] --issue`
- [ ] Matter created in log — [yes/no/TBD]
- [ ] Counsel assigned — [who]
- [ ] Insurance tendered — [yes/no/N-A]
- [ ] Internal escalation (GC/CFO/business lead) — [who/when]
```

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options to what this skill just produced — the five default branches (draft the X, escalate, get more facts, watch and wait, something else) are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- **Validate cited law.** Flags cites for the user to run through a citator (verify it is good law) or check with outside counsel. Inventing legal analysis on inbound demands is malpractice exposure.
- **Send a response.** Drafts are drafted in `demand-draft`; this skill stops at the triage decision.
- **Decide merit definitively.** The rating is a read for triage; a formal merit opinion lives with outside counsel or more thorough analysis.
- **Make the matter-creation call.** Surfaces the recommendation; user decides.

