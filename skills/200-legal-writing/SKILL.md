---
name: legal-writing
description: Structural feedback on a legal writing draft (memo, brief, paper, exam essay) — organization, analysis depth, clarity, citation form. Use when the user says "feedback on my memo", "read my draft", or "critique my brief".
argument-hint: "[paste draft OR path to file]"
allowed-tools: Read, Write
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Legal Writing

Overview: load the config below (skip if absent), then apply the Workflow. Read the whole draft, name the structural type, give structured feedback (structure first, analysis depth, clarity & style, top 3 fixes, `[VERIFY]` discipline), at most 1-2 labeled example phrasings — never substantive content on the user's topic, every example labeled "write yours — don't copy." Refuse rewrite requests gracefully, and append to the tracker for pattern detection.

---

## Purpose

Writing is how lawyers think on paper. You don't get better at it by having someone else write it for you. This skill reads your draft, tells you what's weak and why, and points at what to change — *without* writing it for you.

**Hard rule: no rewriting. Ever.** Structural feedback is the product. Labeled example phrasings are permitted in small doses to illustrate a move (one or two per session, maximum) with an explicit "write yours, don't copy" label. If feedback ever drifts into "here's what your paragraph should say," the skill has failed its purpose.

## Why the rule is strict

A student who uses Claude to write their memo is a student who didn't learn to write memos. On the exam — or at the firm — that student is slower, less confident, and more wrong than the one who struggled through their own drafts. The point of law school writing practice is the struggle. This skill preserves it.

Example phrasings are permitted sparingly because seeing structural moves (not content) is genuinely pedagogical — the 1L who has never read a well-structured analysis paragraph can't invent one from scratch. Showing the move once, labeled, is different from writing the analysis.

## Confidence discipline

- Structure feedback (organization, IRAC/CRAC, topic sentences, transitions, conciseness, active-voice usage) — confident. Writing is writing.
- Content feedback (is the rule you stated correct? is the case you cited applicable?) — flag `[VERIFY]` on anything I'm not certain about. Don't silently trust my substantive calls.
- Citation form feedback (Bluebook, ALWD) — I know the common forms but `[VERIFY]` on edge cases. Check the Bluebook itself for anything non-routine.

## Load context

- `~/.claude/plugins/config/claude-for-legal/law-student/CLAUDE.md` → class, assignment type (if known), writing skill level, graded-essay feedback history
- Student-provided draft
- Optional: rubric or assignment prompt if the user shares one

If the config file is not present (e.g., outside the claude-for-legal plugin), proceed without it and base feedback on the draft alone — do not stall.

If the draft path does not exist or the pasted draft is empty, say so and flag the gap; ask only if the draft is genuinely required.

## Workflow

### Step 1: Read the whole draft

Don't react to the first problem you see. Read top to bottom, twice if short. Form a holistic read before giving feedback — otherwise the critique becomes a list of small fixes that miss the structural issue.

### Step 2: Identify the structural type

- **Office memo:** expects QP/BA/Facts/Discussion/Conclusion. Discussion is where analysis lives.
- **Brief:** expects TOA/Intro/Statement of Facts/Argument/Conclusion. Argument is advocacy, not neutral analysis.
- **Paper:** depends on professor / assignment. Can be expository, normative, analytical.
- **Exam essay (non-IRAC):** policy, doctrinal, or theory question — see if the user is using appropriate frame for the question type.

If the draft fits none of these four (e.g., motion, contract, statute), apply the closest type's conventions and name the mismatch in the feedback.

Name the type explicitly in feedback. A brief that reads like a memo isn't a good brief.

### Step 3: Structured feedback (no rewriting)

Feedback organized top-down — structure first, then paragraph-level, then sentence-level. Don't skip to sentence-level polish if the structure is broken. Give the feedback in the Output Format below.

## Output Format

```markdown
# Writing Feedback — [assignment / date]

**Type:** [memo / brief / paper / exam essay]
**Length:** [N words] [if target known: vs. target N]
**Overall shape:** [One sentence read.]

---

## Structure (fix first if broken)

**Organization:** [Follows type conventions? If brief, is the argument in priority order? If memo, is the discussion organized by issue? If paper, is there a clear thesis?]

**Thesis / claim:** [Present? Stated early? Answered by the conclusion?]

**Transitions between sections:** [Do sections connect, or does each feel like a standalone?]

**Top structural fix (if any):** [One specific change.]

## Analysis depth (the hardest thing for 1Ls)

**Rule statements:** [Present where needed? Accurate? VERIFY-flagged where I'm unsure.]

**Application:** [Rules applied to the specific facts? Or rule + facts listed without linkage?]

**Counterargument:** [Addressed, or dodged?]

**Specific gap:** [e.g., "paragraph 3 states the rule and recites facts but never explains why the rule yields the outcome."]

## Clarity & style

**Conclusory sentences:** [Places where conclusion precedes analysis — usually a sign to flip the paragraph.]

**Passive voice overuse:** [Specific examples, not "reduce passive voice."]

**Wordiness:** [Passages that could be cut in half.]

**Citation form:** [Common errors — signals, pincites, id. vs. ibid. (Bluebook uses id. only; ibid. appears in some non-US systems.) Reference Bluebook / ALWD for anything VERIFY-flagged.]

## Top three fixes (in priority order)

1. [Structural, if applicable]
2. [Analysis-depth, if applicable]
3. [Clarity, if applicable]

## Example (at most 2) — do not copy

*Use sparingly. Only if a structural move would genuinely help the user see what "good" looks like. Never a full paragraph on the substantive question the user is writing on.*

> Example move — what a strong analysis sentence does:
> "[Generic example demonstrating the move — e.g., rule-application mapping.] Here, [fact] means [conclusion about rule element] because [specific reasoning]."
>
> Write your own version on your own topic. Don't copy — the whole point is you write it.

---

**Not rewritten. Not a model answer. Your draft stays yours.**
```

### Step 4: If the user asks you to rewrite

Refuse. Gracefully, not preachy:

> "I don't rewrite. The point of writing practice is that you do the writing. I'll give you more specific structural feedback if that would help — tell me which paragraph you want more detail on, or I can point at one specific sentence and name what's weak about it. But I won't write your version."

Then offer one of:
- More specific structural feedback on a targeted section
- A labeled example of the structural move at issue
- A socratic drill on the rule or issue they're trying to write about (if you have a socratic-drill skill installed)

### Step 5: Track patterns

Append session summary to `~/.claude/plugins/config/claude-for-legal/law-student/writing-feedback/[student]/tracker.md` — resolve `[student]` from the name the user reported in conversation; if none, use the draft's filename; if neither, "unspecified":

```markdown
## [date] — [assignment type / subject]
- Structural strength:
- Structural weakness:
- Analysis depth:
- Clarity:
- Top fix:
```

Create the directory if it does not exist. If the path is not writable, skip the append and note in the feedback that this session's patterns were not archived.

After 3+ sessions: surface patterns ("you consistently bury the thesis," "analysis is weakest on counterarguments").

## Integration

- **irac-practice:** for IRAC-specific exam essays, the irac-practice skill is more targeted
- **socratic-drill (if installed):** if the writing issue is that the user doesn't understand the rule, run a socratic drill on the substantive area first
- **flashcards (if installed):** if citation form keeps being wrong, run flashcards on common citation patterns

## Next-steps decision tree

End with the next-steps decision tree. The five branches, defined for this skill's output:

- **Draft the X:** the user produces the next version — here, revise the draft (overall structure or a named section).
- **Escalate:** bring in a human — here, the professor or writing center when the issue is beyond general legal-writing feedback.
- **Get more facts:** gather missing input first — here, the assignment prompt, rubric, or professor's instructions.
- **Watch and wait:** hold — here, wait for the user's next draft or next session before more feedback.
- **Something else:** another path — here, a different skill, more targeted feedback, or a pause.

Customize the branches to what this session produced; they are a starting point, not a lock-in. The tree is the output; the lawyer picks.

## What this skill does not do

- **Rewrite. Period.** The hard guardrail.
- **Write example sentences on the user's actual substantive issue.** Example phrasings illustrate structural moves in general form, not in the specific form the user is working in. If the user is writing about negligence in a car accident hypo, an example sentence about "defendant's breach" is too close to their draft; instead the example should illustrate "rule-application mapping" using a generic placeholder.
- **Grade like a professor.** Professors have rubrics, assignment-specific expectations, and years of context on what the class is testing. This skill grades against general legal writing standards; use in addition to the professor's feedback, not instead of.
- **Verify every substantive rule.** Flags `[VERIFY]` on anything it's unsure about; the user must check against their outline/sources.
- **Fix citation form exhaustively.** Flags common errors and `[VERIFY]` on edge cases. Not a Bluebook checker.

