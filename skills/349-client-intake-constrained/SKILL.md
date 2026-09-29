---
name: client-intake-constrained
description: Structured intake — practice-area templates, cross-area issue spotting, conflict flags, and triage classification. Produces a formatted case summary the student analyzes and the professor reviews. Does NOT decide case acceptance. Use when the user starts a new client intake, runs an intake interview, or needs a write-up of a new client's situation.
argument-hint: "[optional: practice area hint]"
allowed-tools: Read, Write, Glob, Grep
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Client Intake

## Purpose

Intake is one of the biggest bottlenecks in clinics. A student might spend 45 minutes interviewing, another hour writing it up, more time spotting the issues. Meanwhile the waitlist grows.

This skill structures the conversation, produces the write-up, spots issues across practice areas, and flags conflicts — so the student's time goes to analysis, not transcription.

**What it doesn't do:** decide whether to take the case. That's the student's analysis and the professor's judgment. Claude accelerates the information-gathering and structuring, not the lawyering.

---

## Mandatory Workflow

Before presenting any intake results to the user, you MUST:

1. **Create the intake record** at `.workflow/.scratchpad/intake-{timestamp}/intake.json` with:
   ```json
   {"status": "draft", "client": {}, "issues": [], "conflict_check": null, "triage": null}
   ```
2. **Run conflict check** before accepting any case — write results to `intake.json` → `.conflict_check` with `{"cleared": true/false, "flags": []}`
3. **Read the practice-area templates** at `specs/practice-areas.md` — do not classify issues before reading it
4. **After intake complete**, update `intake.json` → `.status` to `"complete"` and write the formatted case summary
5. **Do not skip the intake record** — if `.workflow/` is not writable, create it first

---

## Load context

This skill is invoked by the plugin command `/legal-clinic:client-intake`. The clinic config provides practice areas, intake templates (per practice area if multiple), supervision style, jurisdiction, and flag triggers.

If `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` exists, load it and follow its practice areas, templates, supervision style, jurisdiction, and flag triggers. If it does not exist (no clinic config mounted), proceed with the generic defaults below and note at the top of the summary: "Clinic config not loaded — generic defaults applied."

## Read the supervisor guide

Check for a practice-area guide at `~/.claude/plugins/config/claude-for-legal/legal-clinic/guides/<practice-area>.md`. If one exists, use its intake questions, red flags, and good-fit criteria instead of the generic defaults below. If one doesn't exist, use the generic intake and note at the end of the intake summary: "This was a generic intake — your supervisor can tailor the questions for your clinic type with `/legal-clinic:build-guide`."

When the intake starts before the practice area is routed (Step 1 of the workflow below), re-check for the guide after routing — the guide path depends on which practice area the intake landed in.

## Workflow

### Step 1: Practice area routing

Which practice area does this intake start in? The client may not know — they know their problem, not the legal category.

> "Tell me what's going on — what brought you to the clinic today?"

From the answer, route to the appropriate intake template. If the clinic handles multiple areas and the problem spans them (housing client mentions immigration status, family client mentions domestic violence), note all relevant areas — cross-area issue spotting is a feature, not a bug.

### Step 2: Practice-area-specific intake

Each practice area asks different questions. Use the template from `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` for this area. Defaults if none provided:

**Immigration:**
- Current status and how entered
- Any prior applications, removals, encounters with ICE/CBP
- Country conditions relevant to any asylum/withholding claim
- Family members and their statuses
- Criminal history (sensitive — explain why asking)
- Timeline urgency: any pending hearings, deadlines, NTAs

**Housing:**
- Type of housing (private, subsidized, public)
- What happened: notice received, lockout, conditions problem, deposit dispute
- Lease terms and payment history
- Habitability issues (repairs requested, landlord response, documentation)
- Timeline urgency: notice date, court date if any

**Family:**
- Relationship and what's at issue (custody, support, divorce, protection)
- Children involved — ages, current arrangement
- Safety: any violence, threats, fear (handle carefully — see cross-area flags)
- Existing court orders
- Timeline urgency: any hearings scheduled

**Consumer:**
- Type of debt or dispute
- Who's contacting them and how (FDCPA relevance)
- Documentation: contracts, statements, collection letters
- Has anything been filed against them
- Timeline urgency: answer deadlines, garnishment, judgment

### Step 3: Cross-practice-area issue spotting

While running the practice-area template, listen for issues outside that area:

- If the client says "I'm worried about my immigration status", flag an immigration issue — even in a housing intake.
- If the client says "My partner [threatening behavior]", flag DV / family law / protective order — even in a consumer intake.
- If the client says "I can't work because of my injury", flag a possible benefits/disability claim.
- If the client says "They're taking money from my paycheck", flag garnishment — a consumer/employment overlap.
- If the client says "The landlord said he'd call ICE", flag housing + immigration + possible retaliation claim.

Note every cross-area issue in the summary. The clinic may handle it, refer it, or both — that's the professor's call. The student should see it.

### Step 4: Conflict check flags

Per whatever conflict-check process `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` describes — if no config is loaded, use the generic conflict checklist below. At minimum:

- Opposing party name(s) — does the clinic represent or have represented them?
- Related parties — anyone else the student or clinic might have a conflict with?
- Positional conflicts — is this case asking for something that would hurt another clinic client?

Flag for professor review. Don't resolve the conflict — surface it.

### Step 5: Triage classification

Not a case-acceptance decision — a triage input:

- **Urgent** means a deadline in days, a safety issue, or irreversible harm imminent.
- **Time-sensitive** means a deadline in weeks, with harm ongoing but not immediately irreversible.
- **Standard** means no immediate deadline; it can queue normally.
- **May be out of scope** means the issue is outside the clinic's practice areas — flag for referral assessment.

### Step 6: Supervision flag check

Per `~/.claude/plugins/config/claude-for-legal/legal-clinic/CLAUDE.md` supervision style and flag triggers — if no config is loaded, use the generic supervision defaults (deadline mentioned, DV indicator, immigration status at issue). If formal queue or configurable flags are enabled, and a trigger is present, note the flag.

### Step 7: Deadline handoff — required deliverable

If the intake surfaces any timeline deadline (answer due, hearing, statute-of-limitations cutoff, cure period, filing window, notice window, ICE check-in, removal hearing, eviction court date, protective order renewal), **emit a copy-paste-ready `/legal-clinic:deadlines --add ...` block as part of the intake output**. This is a required deliverable, not a suggestion — the intake identifies deadlines, and the student shouldn't have to re-transcribe them into the deadline skill.

Format each deadline as a fenced code block the student can copy, with every field pre-populated from the intake:

```
/legal-clinic:deadlines --add
  case=[case slug or client-last-name-keyword]
  type=[response|hearing|statute-of-limitations|discovery|cure-period|filing-window|notice|other]
  description="[one-line description of what is due]"
  due=[VERIFY — student + supervisor compute from triggering event]
  source="[triggering event + statute/rule cite, e.g., 'UD complaint served 2026-05-04, CCP § 1167']"
  owner=[student name]
  warnings=[14,7,3,1]
```

Rules:
- One block per deadline surfaced. Do not combine. Each one will route through the deadlines skill's pre-add duplicate check.
- Leave the `due=` value as `[VERIFY — student + supervisor compute]` when the deadline is jurisdictional (response deadline, SOL, notice window under a specific rule). The deadlines skill will not compute for you; the student + supervisor do the math and update the entry.
- When a date is given in the triggering document (a hearing date on a summons, an ICE check-in date, a renewal deadline on a protective order), put that date in `due=`. When the date is computed (count N days from triggering event), leave the `[VERIFY]` marker.
- If no deadline is surfaced in the intake, omit this section — don't fabricate one.

## Output

Write the completed summary to `intake-summaries/<client-slug>.md` in the workspace (persisted deliverable for the student), then emit the same content in your reply with the next-steps decision tree.

```markdown
# Intake Summary: [Client name or ID]

---
[AI-ASSISTED DRAFT — requires student analysis and attorney review]

**Not legal advice.** This draft is an information-gathering artifact, not legal advice or attorney work product. All conclusions are hypotheses for supervised analysis.

**Privilege and confidentiality.** This summary is derived from client communications that may be privileged, confidential, or both. It inherits the source's privilege status. Distributing it beyond the privilege circle (including outside the clinic) can waive privilege. Keep it in the clinic's privileged file store, mark it appropriately, and make distribution decisions with your supervisor.
---

**Date:** [date] | **Intake by:** [student] | **Practice area:** [primary + any cross-area]

## Bottom line

[Take the case / Decline because X / Need more info on Y — next step is Z]

## Client's situation (in their words)

[The narrative the client gave, before legal categorization. This is the human story.]

## Legal issues identified

*Every statutory, ordinance, regulatory, rule, or case citation in this section carries a provenance tag (see plugin CLAUDE.md `## Shared guardrails` for the tag vocabulary — if the plugin config is unavailable, use the tag vocabulary documented in this template). `[user provided]` if the supervisor uploaded the text, `[statute / regulator site]` if you fetched it this session from an official source, a research-connector tag (`[CourtListener]`, etc.) if it came from a tool result in this conversation, `[model knowledge — verify]` otherwise. The default is `[model knowledge — verify]`. A supervising attorney who cannot verify a cite against a connector needs to see the tag to know what to check first.*

### Primary ([practice area])
- [Issue 1]: [one line with any cite tagged, e.g., "RLTO §5-12-080 `[model knowledge — verify]`"]
- [Issue 2]: [one line]

### Cross-practice-area flags
- [Other area]: [what the client said that raised it]
  [UNCERTAIN: whether clinic handles this or refers — professor call]

## Key facts

- For each key fact, record its source (client statement or document provided) and its documentation status (have it or need it).

## Conflict check

**Opposing party:** [name(s)]
**Related parties:** [any]
**Flag:** [clear / needs conflict check against clinic database]

## Triage

**Classification:** [Urgent / Time-sensitive / Standard / May be out of scope]
**Driving deadline:** [if any — date and what it is]

## Deadlines to log

[One `/legal-clinic:deadlines --add ...` block per surfaced deadline — Step 7.
If none, omit this section.]

## Jurisdictional notes

*Every statute, ordinance, rule, or case citation in this section carries a provenance tag — same vocabulary as `## Legal issues identified` (or the vocabulary documented in this template if the plugin config is unavailable). Default `[model knowledge — verify]`. When no research connector is reachable for this session, record it in the **Sources:** line of the reviewer note — do not emit a standalone banner.*

[State-specific or local-rule-specific issues relevant to this case type, per
CLAUDE.md jurisdiction, with each cite tagged]

## Supervision flags

[If supervision style includes flags: which fired and why. If formal queue:
"QUEUED for [Professor]."]

---

[Generic intake note, if applicable — see supervisor guide section]

## Verification prompts for the student

Before analysis, verify:
- [ ] [Specific fact the intake relies on — confirm with client or documents]
- [ ] [Deadline date — confirm from the actual notice/court document, not client's memory]
- [ ] [Any legal conclusion above is a starting hypothesis — research before relying on it]

## What this summary does NOT do

This summary does not decide whether the clinic takes this case. That's your
analysis and [Professor]'s judgment. It structures what the client told you
so you can spend your time on the analysis instead of the write-up.
```

## Practice-area intake template references

Store practice-area-specific question sets at `references/intake-templates/[area].md`. These files are populated at cold-start from the professor's intake forms; until then, the Step 2 defaults above apply.

## What this skill does NOT do

- **Decide case acceptance.** Student analyzes, professor decides.
- **Resolve conflicts.** Flags them for the professor.
- **Give advice during intake.** Intake is gathering; advice comes after analysis and professor review.
- **Produce a final document.** The summary is a starting point — the student reads it, corrects anything mischaracterized, and builds the analysis from it.

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs` — if the plugin config is unavailable, use the five default branches: draft the X, escalate, get more facts, watch and wait, something else. Customize the options to what this skill just produced; the defaults are a starting point, not a lock-in. The tree is the output; the lawyer picks.


