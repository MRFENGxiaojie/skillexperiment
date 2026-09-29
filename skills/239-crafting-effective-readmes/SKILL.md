---
name: crafting-effective-readmes
description: README writing methodology with audience-matched templates for OSS, personal, internal, and config projects. Use when the user is writing, updating, or reviewing a README file, or asking which sections a README should have. Not all READMEs are the same — this skill matches templates and guidance to the audience and project type.
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Crafting Effective READMEs

## Overview

READMEs answer questions your audience will have. Different audiences need different information — an OSS project contributor needs different context than your future self opening a config folder.

**Always ask:** Who will read this, and what do they need to know?

## Process

### Step 1: Identify the Task

**Ask:** "What README task are you working on?"

- **Create**: new project, no README yet.
- **Add**: need to document something new.
- **Update**: capabilities changed, content is outdated.
- **Review**: check if README is still accurate.

### Step 2: Task-Specific Questions

**Creating initial README:**
1. What type of project? (see Project Types below)
2. What problem does it solve in one sentence?
3. What is the quickest path to "it works"?
4. Anything notable to highlight?

**Adding a section:**
1. What needs to be documented?
2. Where should it go in the existing structure?
3. Who else needs this information?

**Updating existing content:**
1. What changed?
2. Read the current README, identify outdated sections
3. Propose specific edits

**Reviewing/updating:**
1. Read the current README
2. Check against actual project state (package.json, key files, etc.)
3. Flag outdated sections
4. Update "Last reviewed" date if present

### Step 3: Always Ask

After drafting, review for anything the project context would highlight or include.

## Project Types

- **Open Source**: for contributors and users worldwide; key sections are Installation, Usage, Contributing, License; template `templates/oss.md`.
- **Personal**: for your future self and portfolio viewers; key sections are What it does, Tech stack, Learnings; template `templates/personal.md`.
- **Internal**: for teammates and new hires; key sections are Setup, Architecture, Runbooks; template `templates/internal.md`.
- **Config**: for your (confused) future self; key sections are What's here, Why, How to extend, Gotchas; template `templates/xdg-config.md`.

**Infer from the project** if unclear. Don't assume OSS defaults for everything.

## Essential Sections

Every README needs at minimum:

1. **Name** - Self-explanatory title
2. **Description** - What + why in 1-2 sentences
3. **Usage** - How to use it (examples help)

Usage is required for OSS, personal, and internal projects. For config directories a short usage note (or none) suffices — see `section-checklist.md`.

## Output Format

The deliverable is a `README.md` file at the project root, written in the project's primary language. Structure follows the template matching the project type (see Project Types); fill in every `[placeholder]` in the template. Keep the essential sections intact (see Essential Sections). For update/review tasks, edit the existing README in place rather than rewriting from scratch. After drafting, review for anything the project context would highlight or include (Step 3).

## Scope & Limitations

This skill writes, extends, updates, and reviews README files for code projects of four types (OSS, personal, internal, config directories). It does not translate READMEs, build documentation sites or API docs, generate screenshots or badges, or cover non-code repositories. Reviews are point-in-time: re-run after project changes. Templates are starting points — adapt section order to the actual project when the checklist allows.

## References

- `section-checklist.md` - Which sections to include by project type
- `style-guide.md` - Common README mistakes and prose guidance
- `using-references.md` - Guide to deeper reference materials (art-of-readme, make-a-readme, standard-readme-spec, and the two example READMEs in `references/`)

