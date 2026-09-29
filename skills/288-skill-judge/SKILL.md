---
name: skill-judge
description: Evaluate Agent Skill designs against official specifications and best practices. Use when the user asks to review, audit, evaluate, or score a skill, SKILL.md file, or skill package, or asks how to improve skill quality. Provides multi-dimensional scoring (D1-D8, 120-point scale) and actionable improvement suggestions. Covers skill quality assessment, trigger descriptions, knowledge delta, and design pattern compliance.
allowed-tools: Read, Write, Bash, Glob
argument-hint: [path to SKILL.md or skill directory]
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17 official examples.

---


## Core Philosophy

A Skill is NOT a tutorial — it is a **knowledge externalization mechanism**. A skill's value is its **knowledge delta**: the gap between what it provides and what the model already knows.

> **Quality Skill = Exclusive Expert Knowledge − What Claude Already Knows**

**Tool vs Skill**: tools define what the model CAN do (bash, read_file); skills inject what it KNOWS how to do (PDF processing, MCP building). Same model, different skills loaded, becomes different experts.

**Three types of knowledge** — categorize every section of the skill under review:

- **Expert**: Claude genuinely does not know this — must keep, this is the Skill's value.
- **Activation**: Claude knows but may not think of — keep if brief, serves as a reminder.
- **Redundant**: Claude definitely knows this — must delete, wastes tokens.

Context window is a shared public resource — every redundant paragraph is token waste. Good skill design maximizes Expert content, uses Activation sparingly, and eliminates Redundant mercilessly.

---

## Workflow / Process

An evaluation follows five steps:

1. **First Pass — Knowledge Delta Scan**: Read the SKILL.md completely and tag each section **[E] Expert** / **[A] Activation** / **[R] Redundant**. Compute the approximate E:A:R ratio (good: >70% Expert, <20% Activation, <10% Redundant; poor: <40% Expert, high Redundant). This scan feeds D1.
2. **Structure Analysis**: Check frontmatter validity, count total lines, list reference files and sizes, identify which design pattern the skill follows, and check load triggers if references exist. Feeds D4, D5, D7.
3. **Score Each Dimension**: Score D1-D8 (rubrics below). For each dimension, cite specific evidence with line numbers, give a one-line justification, and note specific improvements when the score is below the maximum.
4. **Calculate Total and Grade**: Sum the eight scores (maximum 120), convert to a percentage, and apply the grade scale in the Output Format section.
5. **Generate Report**: Produce the report following the Output Format section, using the reference templates for each part.

The full protocol with worked examples is in `references/evaluation-protocol.md` — **MANDATORY: read it before the first evaluation**.

---

## Output Format

Deliver the evaluation as a markdown report with these sections:

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/120 (X%)
- **Grade**: [A/B/C/D/F]
- **Pattern**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Verdict**: [One-sentence assessment]

## Dimension Scores
[Table with all 8 dimensions, their scores, and notes]

## Critical Issues
[Issues that must be fixed and significantly impact effectiveness]

## Top 3 Improvements
[Prioritized, specific improvement suggestions]

## Detailed Recommendations
[Specific, actionable suggestions with line references]
```

Use the templates in `references/summary.md`, `references/dimension-scores.md`, `references/critical-issues.md`, `references/top-3-improvements.md`, and `references/detailed-recommendations.md` for the report structure.

**Grade Scale** (percentage of 120):

- **A** (90%+, 108+ points): Excellent — production-ready expert Skill.
- **B** (80-89%, 96-107 points): Good — minor improvements needed.
- **C** (70-79%, 84-95 points): Adequate — clear improvement path.
- **D** (60-69%, 72-83 points): Below average — significant issues.
- **F** (<60%, <72 points): Poor — needs fundamental redesign.

Every score below the maximum must be accompanied by evidence (line numbers) and a specific improvement.

---

## Scope and Limitations

**Evaluates:** SKILL.md files and skill packages — single-file skills and multi-file skills with references/, examples/, or scripts/ directories.

**Does not evaluate:** MCP server configurations, tool definitions, or general documentation. The rubric targets agent skills; applying it to other artifacts produces misleading scores.

**Simple skills:** for a skill with no references and under 100 lines, score D5 (Progressive Disclosure) on conciseness and self-containment rather than on load triggers.

**Single-file vs multi-file:** multi-file skills are judged on loading triggers and resource organization; single-file skills are judged on whether their length and structure justify a single file.

**Output is an assessment:** this skill evaluates and recommends; it does not rewrite the skill under review.

---

## Evaluation Dimensions (120 points total)

### D1: Knowledge Delta (20 points) — THE CENTRAL DIMENSION

The most important dimension. Does the Skill add genuinely expert knowledge?

- **0-5**: Explains basics Claude knows (what X is, how to write code, standard library tutorials).
- **6-10**: Mixed — some expert knowledge diluted by obvious content.
- **11-15**: Mostly expert knowledge with minimal redundancy.
- **16-20**: Pure knowledge delta — every paragraph justifies its tokens.

**Red flags** (instant score ≤5):
- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Explaining how to use common libraries
- Generic best practices ("write clean code", "handle errors")
- Definitions of standard industry terms

**Positive signals** (high knowledge delta indicators):
- Decision trees for non-obvious choices ("when X fails, try Y because Z")
- Trade-offs only an expert would know ("A is faster but B handles edge case C")
- Edge cases from real experience
- "NEVER do X because [non-obvious reason]"
- Domain-specific thinking frameworks

**Evaluation questions**:
1. For each section, ask: "Does Claude already know this?"
2. If explaining something, ask: "Is this explaining TO Claude or FOR Claude?"
3. Count paragraphs that are Expert vs Activation vs Redundant

---

### D2: Mindset + Procedures (15 points)

Does the Skill transfer expert **thinking patterns** along with **necessary domain-specific procedures**?

The difference between experts and novices is not "knowing how to operate" — it's "how to think about the problem". But thinking patterns alone are not enough when Claude lacks domain-specific procedural knowledge.

**Key distinction**:
- **Thinking patterns** (e.g., "Before designing, ask: What makes this memorable?"): High value — shapes decision-making.
- **Domain-specific procedures** (e.g., "OOXML workflow: unzip → edit XML → validate → rezip"): High value — Claude may not know this.
- **Generic procedures** (e.g., "Step 1: Open file, Step 2: Edit, Step 3: Save"): Low value — Claude already knows.

- **0-3**: Only generic procedures Claude already knows.
- **4-7**: Has domain procedures but lacks thinking frameworks.
- **8-11**: Good balance — thinking patterns + domain-specific workflows.
- **12-15**: Expert level — shapes thinking AND provides procedures Claude wouldn't know.

**What counts as valuable procedures**:
- Workflows Claude was not trained on (new tools, proprietary systems)
- Non-obvious correct ordering (e.g., "validate BEFORE packaging, not after")
- Critical steps easy to miss (e.g., "MUST recalculate formulas after editing")
- Domain-specific sequences (e.g., MCP server 4-phase development process)

**What counts as redundant procedures**:
- Generic file operations (open, read, write, save)
- Standard programming patterns (loops, conditionals, error handling)
- Common usage of well-documented libraries

**Expert thinking patterns look like**:
```markdown
Before [action], ask yourself:
- **Purpose**: What problem does this solve? Who uses it?
- **Constraints**: What are the hidden requirements?
- **Differentiation**: What makes this solution memorable?
```

**Valuable domain procedures look like**:
```markdown
### Redlining Workflow (Claude wouldn't know this sequence)
1. Convert to markdown: `pandoc --track-changes=all`
2. Map text to XML: grep for text in document.xml
3. Implement changes in batches of 3-10
4. Package and verify: confirm ALL changes were applied
```

**Redundant generic procedures look like**:
```markdown
Step 1: Open the file
Step 2: Find the section
Step 3: Make the change
Step 4: Save and test
```

**The test**:
1. Does it tell Claude WHAT to think? (thinking patterns)
2. Does it tell Claude HOW to do things it wouldn't know? (domain procedures)

A good Skill provides both when needed.

---

### D3: Anti-Pattern Quality (15 points)

Does the Skill have effective NEVER lists?

**Why this matters**: Half of expert knowledge is knowing what NOT to do. A senior designer sees purple gradient on white background and instinctively cringes — "too AI-generated". This intuition for "what to absolutely never do" comes from stepping on countless landmines.

Claude hasn't stepped on those landmines. It doesn't know that the Inter font is overused, doesn't know that purple gradients are the signature of AI-generated content. Good Skills must explicitly declare these "absolute nevers".

- **0-3**: No anti-patterns mentioned.
- **4-7**: Generic warnings ("avoid mistakes", "be careful", "consider edge cases").
- **8-11**: Specific NEVER list with some reasoning.
- **12-15**: Expert-quality anti-patterns with WHY — things only experience teaches.

**Expert anti-patterns** (specific + reason):
```markdown
NEVER use generic AI-generated aesthetics like:
- Overused font families (Inter, Roboto, Arial)
- Cliché color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Default border-radius on everything
```

**Weak anti-patterns** (vague, no reasoning):
```markdown
Avoid making mistakes.
Be careful with edge cases.
Don't write bad code.
```

**The test**: Would an expert read the anti-pattern list and say "yes, I learned that the hard way"? Or would they say "this is obvious to everyone"?

---

### D4: Specification Compliance — Especially Description (15 points)

Does the Skill follow official format requirements? **Special focus on description quality.**

- **0-5**: Missing frontmatter or invalid format.
- **6-10**: Has frontmatter but description is vague or incomplete.
- **11-13**: Valid frontmatter, description has WHAT but weak on WHEN.
- **14-15**: Perfect — comprehensive description with WHAT, WHEN, and trigger keywords.

**Frontmatter requirements**:
- `name`: lowercase, alphanumeric + hyphens only, ≤64 characters
- `description`: **THE MOST CRITICAL FIELD** — determines whether the skill is used

---

**Why description is THE MOST IMPORTANT FIELD**:

### SKILL ACTIVATION FLOW

```
User Request
    → Agent sees ALL descriptions (only descriptions, not bodies!)
    → Decides which of skills to activate
    → Loads the body of the selected skill(s)
```

If description doesn't match - Skill is NEVER loaded
If description is vague - Skill may not trigger when it should
If description lacks keywords - Skill is invisible to Agent

**The brutal truth**: A Skill with perfect content but poor description is **useless** — it will never be activated. The description is the **one and only chance** to tell the Agent "use me in these situations".

---

**Description must answer THREE questions**:

1. **WHAT**: What does this Skill do? (functionality)
2. **WHEN**: In which situations should it be used? (trigger scenarios)
3. **KEYWORDS**: What terms should trigger this Skill? (searchable terms)

**Excellent description** (all three elements):
```yaml
description: "Comprehensive document creation, editing, and analysis with support
for tracked changes, comments, formatting preservation, and text extraction.
When Claude needs to work with professional documents (.docx files) to:
(1) Create new documents, (2) Modify or edit content,
(3) Work with tracked changes, (4) Add comments, or any other document task"
```

Analysis:
- WHAT: creation, editing, analysis, tracked changes, comments
- WHEN: "When Claude needs to work with... to: (1)... (2)... (3)..."
- KEYWORDS: .docx files, tracked changes, professional documents

**Poor description** (missing elements):
```yaml
description: "Handle document-related functionality"
```

Problems:
- WHAT: vague ("document-related functionality" — specifically what?)
- WHEN: missing (when should Agent use this?)
- KEYWORDS: missing (no ".docx", no specific scenarios)

**Another poor example**:
```yaml
description: "A useful skill for various tasks"
```

This is useless — Agent doesn't know when to activate it.

---

**Description quality checklist**:
- [ ] Lists specific capabilities (not just "helps with X")
- [ ] Includes explicit trigger scenarios ("Use when...", "When user asks for...")
- [ ] Contains searchable keywords (file extensions, domain terms, action verbs)
- [ ] Specific enough for Agent to know EXACTLY when to use
- [ ] Includes scenarios where this skill MUST be used (not just "can be used")

---

### D5: Progressive Disclosure (15 points)

Does the Skill implement appropriate content layers?

Skill loading has three layers:
```
Layer 1: Metadata (always in memory)
         Only name + description
         ~100 tokens per skill

Layer 2: SKILL.md Body (loaded after trigger)
         Detailed guidelines, code examples, decision trees
         Ideal: < 500 lines

Layer 3: Resources (loaded on demand)
         scripts/, references/, assets/
         No limit
```

- **0-5**: Everything dumped in SKILL.md (>500 lines, no structure).
- **6-10**: Has references but unclear when to load them.
- **11-13**: Good bundling with MUST-READ triggers present.
- **14-15**: Perfect — decision trees + explicit triggers + "DO NOT Load" guidance.

**For Skills WITH a references directory**, check Load Trigger Quality:

- **Poor**: References listed at the end, no loading guidance.
- **Mediocre**: Some triggers but not integrated into workflow.
- **Good**: MUST-READ triggers at workflow steps.
- **Excellent**: Scenario detection + conditional triggers + "DO NOT Load".

**The loading problem**:
Load too little - Load too much
- References go unused                  - Wastes context space
- Agent doesn't know when to load       - Irrelevant info dilutes key content
- Knowledge is there but never accessed  - Unnecessary token overhead

**Good load trigger** (integrated into workflow):
```markdown
### Creating New Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`docx-js.md`](docx-js.md) (~500 lines) completely from start to finish.
**NEVER set range limits when reading this file.**

**DO NOT load** `ooxml.md` or `redlining.md` for this task.
```

**Poor load trigger** (just listed):
```markdown

## References
- docx-js.md - for creating documents
- ooxml.md - for editing
- redlining.md - for tracking changes
```

**For simple Skills** (no references, <100 lines): Score based on conciseness and self-containment.

---

### D6: Freedom Calibration (15 points)

Is the specificity level appropriate for the task fragility?

Different tasks need different levels of constraint. This is about matching freedom to fragility.

- **0-5**: Severely mismatched (rigid scripts for creative tasks, vague for fragile ops).
- **6-10**: Partially appropriate, some mismatches.
- **11-13**: Good calibration for most scenarios.
- **14-15**: Perfect freedom calibration everywhere.

**The freedom spectrum**:

- **Creative/Design**: Should have high freedom — multiple valid approaches, differentiation is value (example: frontend-design).
- **Code review**: Should have medium freedom — principles exist but judgment needed (example: code-review).
- **File format operations**: Should have low freedom — one wrong byte corrupts file, consistency critical (examples: docx, xlsx, pdf).

**High freedom** (text-based instructions):
```markdown
Commit to a BOLD aesthetic direction. Pick an extreme: brutally minimal,
maximalist chaos, retro-futuristic, organic natural...
```

**Medium freedom** (pseudocode or parameterized):
```markdown
Review priority:
1. Security vulnerabilities (must fix)
2. Logic errors (must fix)
3. Performance issues (must fix)
4. Maintainability (optional)
```

**Low freedom** (specific scripts, exact steps):
```markdown
**MANDATORY**: Use exact script in `scripts/create-doc.py`
Parameters: --title "X" --author "Y"
DO NOT modify the script.
```

**The test**: Ask "if Agent makes a mistake, what is the consequence?"
- High consequence → Low freedom
- Low consequence → High freedom

---

### D7: Pattern Recognition (10 points)

Does the Skill follow an established official pattern?

Through analysis of 17 official Skills, we identified 5 main design patterns:

- **Mindset** (~50 lines): Thinking > technique, strong NEVER list, high freedom (example: frontend-design) — use for creative tasks requiring taste.
- **Navigation** (~30 lines): Minimal SKILL.md, routes to sub-files (example: internal-comms) — use for multiple distinct scenarios.
- **Philosophy** (~150 lines): Two steps — Philosophy → Express, emphasizes craftsmanship (example: canvas-design) — use for art/creation requiring originality.
- **Process** (~200 lines): Phased workflow, checkpoints, medium freedom (example: mcp-builder) — use for complex multi-stage projects.
- **Tool** (~300 lines): Decision trees, code examples, low freedom (examples: docx, pdf, xlsx) — use for precise format-specific operations.

- **0-3**: No recognizable pattern, chaotic structure.
- **4-6**: Partially follows a pattern with significant deviations.
- **7-8**: Clear pattern with minor deviations.
- **9-10**: Masterful application of appropriate pattern.

**Pattern selection guide**:

- If your task needs taste and creativity, use the **Mindset** pattern (~50 lines).
- If your task needs originality and craftsmanship quality, use the **Philosophy** pattern (~150 lines).
- If your task has multiple distinct sub-scenarios, use the **Navigation** pattern (~30 lines).
- If your task is a complex multi-stage project, use the **Process** pattern (~200 lines).
- If your task involves precise format-specific operations, use the **Tool** pattern (~300 lines).

---

### D8: Practical Usability (15 points)

Can an Agent actually use this Skill effectively?

- **0-5**: Confusing, incomplete, contradictory, or untested guidance.
- **6-10**: Usable but with notable gaps.
- **11-13**: Clear guidance for common cases.
- **14-15**: Comprehensive coverage including edge cases and error handling.

**Check for**:
- **Decision trees**: For multi-path scenarios, is there clear guidance on which path to take?
- **Code examples**: Do they actually work? Or are they pseudocode that breaks?
- **Error handling**: What if the primary approach fails? Are there fallbacks?
- **Edge cases**: Are uncommon but realistic scenarios covered?
- **Actionability**: Can Agent act immediately, or does it need to figure things out?

**Good usability** (decision tree + fallback):
```markdown
- **Read text**: primary tool `pdftotext`, fallback `PyMuPDF` — use the fallback when you need layout info.
- **Extract tables**: primary tool `camelot-py`, fallback `tabula-py` — use the fallback when `camelot` fails.

**Common issues**:
- Scanned PDF: pdftotext returns blank → Use OCR first
- Encrypted PDF: Permission error → Use PyMuPDF with password
```

**Poor usability** (vague):
```markdown
Use appropriate tools for PDF processing.
Handle errors properly.
Consider edge cases.
```

---


## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted
- **NEVER** ignore token waste — every redundant paragraph should result in deduction
- **NEVER** let length impress you — a 43-line Skill can outperform a 500-line one
- **NEVER** skip mentally testing decision trees — do they actually lead to correct choices?
- **NEVER** forgive explaining basics with "but it provides useful context"
- **NEVER** overlook missing NEVER lists — if there is no NEVER list, that is a significant gap
- **NEVER** assume all procedures are valuable — distinguish domain-specific from generic
- **NEVER** underestimate the description field — poor description = skill is never used
- **NEVER** put "when to use" information only in the body — Agent only sees description before loading

---

## Common Failure Patterns

Watch for these recurring failure modes when evaluating a skill:

1. **The Tutorial** — explains basics Claude already knows (D1 red flag)
2. **The Dump** — everything in one 800+ line file (D5 red flag)
3. **The Orphan References** — reference files that never get loaded, no triggers anywhere in the workflow (D5 red flag)
4. **The Checkbox Procedure** — mechanical steps without thinking frameworks (D2 red flag)
5. **The Vague Warning** — "be careful" without specific guidance (D3 red flag)
6. **The Invisible Skill** — great content but a poor description, so it never activates (D4 red flag)
7. **The Wrong Location** — "when to use" information only in the body, invisible to the Agent before loading (D4 red flag)
8. **The Over-Engineered** — unnecessary auxiliary files that add tokens without knowledge (D5/D8 red flag)
9. **The Freedom Mismatch** — wrong freedom level for the task type (D6 red flag)

If any pattern is present, note it explicitly in the report and reflect it in the affected dimension's score.

---

## Reference Files

- [evaluation-protocol.md](references/evaluation-protocol.md): **MANDATORY** before the first evaluation — the full 5-step protocol with thresholds.
- [summary.md](references/summary.md): load at Step 5, when writing the Summary section of the report.
- [dimension-scores.md](references/dimension-scores.md): load at Step 5, when writing the Dimension Scores table.
- [critical-issues.md](references/critical-issues.md): load at Step 5, when writing the Critical Issues section.
- [top-3-improvements.md](references/top-3-improvements.md): load at Step 5, when writing the Top 3 Improvements section.
- [detailed-recommendations.md](references/detailed-recommendations.md): load at Step 5, when writing the Detailed Recommendations section.

**DO NOT load** the report templates until Step 5 (Generate Report) — they are output structure, not evaluation input.

