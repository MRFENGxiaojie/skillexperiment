---
name: capture-triage
description: "Processes Drafts Pro captures from the Inbox folder. Classifies by intent, shows preview for approval, routes to Ready as tasks. Use when triaging captures, processing mobile notes, or as part of daily review. Triggers on \"triage captures\", \"process captures\", \"check my captures\"."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Capture Triage

## What This Does

Turns mobile captures into actionable tasks in your Ready queue. Everything captured has
intent - this skill makes it explicit so task-clarity-scanner can decide what's important.

## Who It's For

Ed - capturing quick thoughts in Drafts Pro throughout the day.

## The Philosophy

> Everything captured has intent. Route to Ready, let task-clarity-scanner decide what
> moves to Someday/Maybe.

No passive filing. Every capture becomes a decision point.

---

## Paths

```
Inbox:      /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
Processed:  /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/Processed/
Daily note: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
(Route into the existing daily note already in the vault — e.g. 2026-08-10.md. Only create a new YYYY-MM-DD.md if no daily note exists.)
Projects:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
Contacts:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/CONTACT - *.md
```

---

## Important: Naming Clarification

- Inbox **folder** is `/Zettelkasten/Inbox/` — where Drafts Pro sends mobile notes.
- Captures **section** is `## Captures` in the daily note — links to docs created today.
- Ready **destination** is `## Ready` section in the daily note — where triaged tasks go.

**Remember:** This skill reads from the Inbox FOLDER and routes to the Ready SECTION.
Tasks go to Ready section only - Captures section is for document links.

---

## Workflow

### Step 1: Check Inbox Folder (Root Only)

**Important:** Only check files directly in Inbox/, NOT subdirectories.

```bash
ls "Zettelkasten/Inbox/"*.md 2>/dev/null   # or Glob pattern Zettelkasten/Inbox/*.md
```

If no files found: Report "No captures waiting" and stop.
If files found: Continue to Step 2.

### Step 2: Load Context

Pull active project names from mission-context skill AND:

```
Glob: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
```

Build a list of project names for matching.

### Step 3: Read and Classify Each Capture (Background OK)

**This step can run in background.** Read and classify all captures before surfacing to user.

For each `.md` file in Inbox:
1. Read full content
2. **Extract source URL from frontmatter** (see Step 3b)
3. Detect if already-processed (see Step 3a)
4. Classify by intent (see Step 4)

Present the preview only after ALL files are read and classified, then route directly (no user decision step).

### Step 3a: Detect Already-Processed Content

If capture content looks like a summary (has structure, headers, quotes sources):
- Flag as `[PROCESSED]`
- Will suggest routing as REFERENCE
- Won't offer research-swarm (already researched)

**Signals of processed content:**
- Has markdown headers (##, ###)
- Contains bullet lists with structured info
- Quotes or attributes other sources
- Looks like notes from a video/article

### Step 3b: Extract Source URLs

**For x-bookmark files** (filename starts with `x-`):
- Read `tweet_url` from YAML frontmatter
- This URL MUST be included when routing to Ready

**For other captures with URLs:**
- Check for `url:`, `source_url:`, or `link:` in frontmatter
- Check for markdown links `[text](url)` in body
- Preserve any URLs found for routing step

### Step 4: Classify Each Capture

**Priority Rule:** Inline hints override auto-detection. Check for these FIRST:
- `IDEA:` or `Idea:` → IDEA
- `Research:` → RESEARCH (triggers swarm option)
- `for [Project Name]` → PROJECT_UPDATE
- `Task:` or `TODO:` → TASK

**Auto-Detection (if no inline hint):**

- A capture that starts with a verb (call, email, buy, check, send, schedule) is classified as TASK.
- A capture that contains a `Research:` hint or an explicit question needing investigation is classified as RESEARCH.
- A capture with "What if..." or speculative language is classified as IDEA.
- A capture that mentions an active project name is classified as PROJECT_UPDATE.
- A capture with a person's name plus action context is classified as CONTACT.
- A capture of links, articles, saved content, or observations is classified as REFERENCE.

### Step 5: Show Classification Preview (Single-Pass)

Show the preview table, then proceed directly with routing in the same pass. Do not ask the user to decide.

---

#### Step 5a: Present the Table

Show what you found. Let user absorb the information first:

```
## Capture Triage Preview

Found [N] captures. Here's how I've classified them:

- note1.md, preview "Call dentist...", is classified as TASK and suggested routing is Ready: Call dentist (MM-DD).
- note2.md, preview "What if we...", is classified as IDEA and suggested routing is Ready: Consider: [idea] (MM-DD).
- summary.md, preview [PROCESSED] "Article about...", is classified as REFERENCE and suggested routing is Ready: Review: [title] (MM-DD).
- question.md, preview "Research: how do...", is classified as RESEARCH and suggested routing is Spawn research-swarm?.
```

**Show the table in your output, then proceed.** Do not pause for user confirmation; route everything as shown in the table (equivalent to "Approve all").

---

#### Step 5b: Proceed (no confirmation needed)

After showing the table, state the default decision **"Approve all"** explicitly in your output, then do NOT ask the user; proceed directly with routing as shown:

```
Approved routing (Approve all):
1. **Approve all** - Route everything as shown  ← default
```

**Key points:**
- Show [PROCESSED] flag for already-summarized content
- RESEARCH items are handled autonomously (see Step 7): add a [RESEARCH] placeholder to Ready; spawn a research-swarm only if a background-agent tool is available
- Apply all shown routes without waiting for user modification or skip

### Step 6: Route by Classification

Route each capture directly (as shown in the table):

- TASK routes to Ready with format `- [ ] [action] (MM-DD)`.
- IDEA routes to Ready with format `- [ ] Consider: [idea] (MM-DD)`.
- REFERENCE routes to Ready with format `- [ ] Review: [linked title](URL) - brief context (MM-DD)`.
- RESEARCH spawns an agent directly (see Step 7).
- PROJECT_UPDATE routes to the project file as a timestamped append to `## Context Gathered`.
- CONTACT creates a note and routes to Ready with format `- [ ] Follow up with [Name] (MM-DD)`.

**IMPORTANT: Review tasks MUST include links.**

For REFERENCE items, always include the source link so Ed can find it:
- X bookmarks: `[Title](https://x.com/author/status/ID)`
- Articles: `[Article Title](URL)`
- Obsidian docs: `[[Document Name]]`
- YouTube: `[Video Title](URL)`

If a capture has no URL but references external content, note this: `(source needed)`

---

**Edit Instructions:**

For each item routed to Ready:
1. Open the daily note at:
   `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md`
   Use the existing daily note in the vault (here `2026-08-10.md`); only create a new dated file if none exists.
2. Find the `## Ready` section
3. Use Edit tool to append the task in the format shown above
4. **Do NOT add to `## Captures`** - that section is for document links only

Example Edit operation:
```
old_string: "## Ready\n- [ ] existing task"
new_string: "## Ready\n- [ ] existing task\n- [ ] [new task from capture] (01-06)"
```

**If creating PROJECT or CONTACT files:** Those files get created separately, and a
LINK to them goes in Ready as a task (e.g., `- [ ] [[PROJECT - Name]] - brief desc`).

### Step 7: Handle Research (Autonomous)

Handle every RESEARCH capture autonomously — do not ask the user whether to spawn research.

If a background subagent tool (Task/Agent) is available, spawn a research-swarm for it:


```
Task(
  description="Research: [Topic]",
  prompt="Research question: [Full capture content]

  Use research-swarm pattern to investigate. Save findings to Zettelkasten.
  When complete, add review task to Ready: '- [ ] Review: [[Research - Topic]] (MM-DD)'",
  subagent_type="research-swarm",
  run_in_background=true
)
```

Always add a placeholder line to the daily note Ready section (spawned or not):
```
- [RESEARCH] [Topic] - research pending (MM-DD)
```
If no background subagent tool is available, this placeholder is the record — route the RESEARCH item as a Ready placeholder and continue.

### Step 8: Handle Contacts

When a capture mentions a person with action context:

1. Check if `CONTACT - [Name].md` exists
2. If exists: Append to `## Interactions` section
3. If new: Create contact note using template
4. Always add follow-up task to Ready

**Contact Note Template:**

```markdown
---
type: contact
created: YYYY-MM-DD
source: capture-triage
---

# [Person Name]

## Context
[Original capture content]

## Interactions
- YYYY-MM-DD: Initial capture - [summary]

## Follow-up
[Any implied next steps]
```

### Step 9: Move to Processed

After routing each capture:

```bash
mv "[Inbox file]" "[Processed folder]"
```

Move files to Inbox/Processed/ as safety net (preserves originals).

### Step 10: Generate Triage Summary

```markdown
## Capture Triage - YYYY-MM-DD HH:MM

**Processed:** N items | **Research spawned:** M (if any)

### Routed to Ready
- [N] tasks
- [N] ideas (Consider:)
- [N] references (Review:)

### Research Running
- [Topic] - spawned at HH:MM

### Actions Taken
- Moved N files to Inbox/Processed/
- Created CONTACT - [Name].md (if any)
- Updated PROJECT - [Name].md (if any)
```

---

## Examples

### Example 1: Dry Run Preview

**Inbox folder contains 4 files:**

```
1. "Call dentist Monday about cleaning"
2. "What if we did a 5-day hook challenge?"
3. [PROCESSED] "Summary of Karpathy video - 6 paradigm shifts..."
4. "Research: how do successful coaches use AI?"
```

**Skill shows:**

```
## Capture Triage Preview

- "Call dentist..." is classified as TASK with suggested action → Ready: "Call dentist Monday (01-05)".
- "What if we..." is classified as IDEA with suggested action → Ready: "Consider: 5-day hook challenge (01-05)".
- [PROCESSED] "Summary of Karpathy..." is classified as REFERENCE with suggested action → Ready: "Review: [Karpathy video](URL) - 6 paradigm shifts (01-05)".
- "Research: how do coaches..." is classified as RESEARCH with suggested action → [RESEARCH] placeholder (research-swarm if tool available).

Approved routing (Approve all): route everything as shown.
```

### Example 2: After Routing

**Result:**
- Ready gets 3 new tasks + 1 research placeholder
- Research-swarm spawns in background (if tool available)
- All 4 files moved to Processed/
- Summary generated

---

## Guidelines

- **Single-pass preview** - Show the table, state the "Approve all" default, then route directly (no user decision step)
- **Ready, not Captures** - All triaged items become tasks in `## Ready` section
- **Dry run is standard** - Always show preview before routing
- **Respect inline hints** - They override auto-detection
- **Research handled autonomously** - Add a [RESEARCH] placeholder to Ready; spawn a research-swarm only if a background-agent tool is available
- **[PROCESSED] content** - Flag summaries, suggest REFERENCE routing
- **Everything to Ready** - Let task-clarity-scanner handle prioritization
- **Preserve originals** - Move to Processed/ folder as safety net
- **Review tasks need links** - Always include source URL or wikilink so Ed can find the content

---

## Limitations

- **Markdown files only.** Only `.md` files in the Inbox root are processed. Subdirectories, non-markdown files, and hidden files are silently ignored.
- **Autonomous routing.** All routing decisions are previewed in the table and applied directly, without waiting for user confirmation (automated/headless runs). In interactive sessions the user can adjust later.
- **Existing projects only.** The skill appends to existing `PROJECT - *.md` files. It never creates new project files from scratch.
- **Moves, never deletes.** Original capture files are moved to `Processed/`, never deleted. No data is permanently removed.
- **Inbox root only.** Only files directly in `Inbox/` are processed. Files in subdirectories (including `Inbox/Processed/`) are excluded.
- **Downstream handoff.** This skill routes to Ready; it does not prioritize or schedule tasks. That is handled by task-clarity-scanner.

## Version History

- Version 1.0 (2025-01-05): Initial build as inbox-triage.
- Version 2.0 (2025-01-05): Renamed to capture-triage, added dry run, AskUserQuestion flow, and all routes to Ready.
- Version 2.1 (2026-01-06): Renamed folder Captures→Inbox, split Step 5 into a two-step preview, explicit Ready section routing, and background OK for classification.
- Version 2.2 (2026-01-12): Added requirement that Review tasks MUST include source links (URL or wikilink), and added Step 3b to extract URLs from frontmatter (especially x-bookmark tweet_url).
- Version 2.3 (2026-08-17): Made routing fully autonomous for headless runs — single-pass preview with an explicit 'Approve all' default, research handled without asking, and routing into the existing daily note.

---

## Notes & Learnings

- Day 1 test processed 32 captures with backlog - dry run prevented overwhelm
- [PROCESSED] detection helps avoid re-researching already-summarized content
- Research-swarm opt-in prevents runaway agent spawning
- Review tasks without links are useless - Ed can't find the content to review (added v2.2)

