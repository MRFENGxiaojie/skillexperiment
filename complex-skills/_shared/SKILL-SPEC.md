# SKILL.md Specification v1.0

The authoritative standard for SKILL.md files in the SkillIF evaluation corpus. All 322 skills MUST conform to this spec.

---

## 1. Frontmatter (YAML)

### 1.1 Required Fields

| Field | Rule | Example |
|-------|------|---------|
| `name` | Lowercase, alphanumeric + hyphens only, ≤64 characters. MUST match directory name. | `wcag-accessibility-audit` |
| `description` | Third-person description of WHAT the skill does + WHEN to use it. ≤1024 characters. See §2. | `Comprehensive web accessibility audit using WCAG 2.1/2.2 guidelines. Use when the user asks to audit a website for accessibility, check WCAG compliance, or prepare for accessibility certification.` |

### 1.2 Allowed Optional Fields (Claude Code harness)

| Field | Purpose | Example |
|-------|---------|---------|
| `allowed-tools` | Tools the skill may use, comma-separated | `Read, Write, Bash, Glob, Grep` |
| `argument-hint` | Hint for argument input | `[skill path \| SKILL.md path]` |
| `user-invocable` | Whether user can invoke directly | `true` |
| `model` | Model override hint | `claude-sonnet-5` |
| `paths` | File path patterns that trigger this skill | `**/*.docx` |
| `disable-model-invocation` | Prevent model from auto-invoking | `true` |

### 1.3 Forbidden Fields

ALL other frontmatter keys are forbidden. Specifically:
- No `metadata`, `license`, `version`, `agents`, `source`, `risk`, `date_added`, `category`, `compatibility`, `tags`, `author`, `domain`, `bundle`, `contributors`, `created`, `updated`, `dependencies`, `difficulty`, `frequency`, `time-saved`, `estimatedTime`, `displayName`, `color`, `featured`, `orchestrated-by`, `related-skills`, `related-commands`, `related-agents`, `subdomain`, `tech-stack`, `python-tools`, `tools`, `trigger`, `triggers`, `use-cases`, `verified`, `title`, `stats`, `skills`

Non-frontmatter metadata (license, author, version history) that is genuinely valuable belongs in a `## Metadata` section at the END of the body.

---

## 2. Description Specification

### 2.1 Structure

A description MUST answer these three questions:

1. **WHAT** — What does this skill do? Be specific, not vague.
2. **WHEN** — In what situations should the agent use this skill? List concrete trigger scenarios.
3. **KEYWORDS** — Domain terms, file extensions, action verbs that help match user intent.

### 2.2 Template

```
<what this skill does, third-person>. Use when the user <trigger scenarios>.
```

### 2.3 Voice

- MUST be **third-person**: describes the skill, not addresses the user
- MUST NOT use:
  - Imperative: `"Use this skill to..."`, `"Use this skill whenever..."`
  - First-person: `"I can help you..."`, `"I will..."`, `"We provide..."`
  - Second-person: `"You can use this to..."`

### 2.4 Trigger Signals (at least one must appear)

- `"Use when the user..."`
- `"Use when the user asks to..."`
- `"Use when the user needs to..."`
- `"Triggers on..."`
- `"Use for..."`

### 2.5 What to Avoid in Description

- Cross-skill routing (`"NOT for X, use Y instead"`) — belongs in body Scope section
- Generic/vague descriptions (`"A useful skill"`, `"Helps with tasks"`)
- Descriptions under 40 characters (too short to be meaningful)

### 2.6 Examples

**Good:**
```yaml
description: "Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers. Use when the user asks to create a test plan, generate manual test cases, build a regression suite, validate a page against a Figma design, or write a bug report."
```

**Bad (imperative):**
```yaml
description: "Use this skill whenever the user wants to create a document."
```

**Bad (vague):**
```yaml
description: "A useful skill for various tasks."
```

**Bad (first-person):**
```yaml
description: "I can help you with PDF processing and extraction."
```

---

## 3. Body Structure

### 3.1 Required Sections

Every SKILL.md body MUST include these three sections (in any order, under any heading name):

| Section | Must Answer | Example Headings |
|---------|-------------|------------------|
| **Workflow / Process** | What does the skill actually do, step by step? | `## Workflow`, `## Execution Flow`, `## Process` |
| **Output Format** | What does the user get? What does the result look like? | `## Output`, `## Output Format`, `## Deliverables` |
| **Scope / Limitations** | What does this skill NOT do? When should it NOT be used? | `## Scope`, `## Limitations`, `## What This Skill Does NOT Do` |

### 3.2 Size Limits

| Pattern | Target Lines | When to Use |
|---------|-------------|-------------|
| **Mindset** | ~50 | Creative tasks requiring taste and judgment |
| **Navigation** | ~30 | Multiple distinct sub-scenarios, routes to sub-files |
| **Philosophy** | ~150 | Art/creation requiring originality and craftsmanship |
| **Process** | ~200 | Complex multi-stage projects with checkpoints |
| **Tool** | ~300 | Precise format-specific operations with decision trees |

**Hard limit**: SKILL.md body MUST NOT exceed 600 lines. Content beyond 600 lines belongs in `references/` files.

### 3.3 File References

- Use relative paths within the skill directory: `references/foo.md`, `scripts/bar.py`
- MUST NOT use cross-skill references: `../other-skill/SKILL.md` or `../other-skill/references/foo.md`
- When referencing another skill, use its name in prose: `"see also: <skill-name>"`

### 3.4 Content Guidelines

- **Knowledge delta over redundancy**: Don't explain basic concepts the model already knows
- **Anti-patterns over generic advice**: Specific NEVER rules with reasons > vague warnings
- **Decision trees over prose**: When there are branches, use a table or decision tree
- **Concrete over abstract**: Real examples, actual commands, specific values

---

## 4. Directory Naming

- MUST match `name` field in frontmatter
- Format: `NNN-kebab-case-name/` where NNN is the 3-digit sequence number
- Example: `281-wcag-accessibility-audit/`
- NO spaces, NO uppercase letters in the directory name

---

## 5. Compliance Checklist

```
[ ] name: lowercase + hyphens, ≤64 chars, matches directory
[ ] description: third-person, includes WHAT + WHEN + KEYWORDS, ≤1024 chars
[ ] description: no imperative/first-person/second-person openings
[ ] description: no cross-skill routing embedded
[ ] description: at least one trigger signal phrase
[ ] frontmatter: no keys outside the allowed list
[ ] body: ≤600 lines
[ ] body: has workflow/process section
[ ] body: has output format section
[ ] body: has scope/limitations section
[ ] body: no cross-skill file references (../other-skill/)
[ ] directory: NNN-kebab-case, no spaces or uppercase
```
