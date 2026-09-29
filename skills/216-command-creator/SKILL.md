---
name: command-creator
description: This skill should be used when creating a Claude Code slash command. Use when users ask to "create a command", "make a slash command", "add a command", or want to document a workflow as a reusable command. Essential for creating optimized, agent-executable slash commands following best practices.
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Command Creator

This skill guides the creation of Claude Code slash commands - reusable workflows that can be invoked with `/command-name` in Claude Code conversations.

## About Slash Commands

Slash commands are markdown files stored in `.claude/commands/` (project level) or `~/.claude/commands/` (global/user level) that are expanded into prompts when invoked. They are ideal for:

- Repetitive workflows (code review, PR submission, CI fix)
- Multi-step processes that need consistency
- Delegation patterns for agents
- Project-specific automation

## When to Use This Skill

Invoke this skill when users:

- Ask to "create a command" or "make a slash command"
- Want to automate a repetitive workflow
- Need to document a consistent process for reuse
- Say "I keep doing X all the time, can we create a command for it?"
- Want to create project-specific or global commands

## Included Resources

This skill includes reference documentation for detailed guidance:

- **references/patterns.md** - Command patterns (workflow automation, iterative fix, agent delegation, simple execution)
- **references/examples.md** - Real command examples with complete code (submit-stack, ensure-ci, create-implementation-plan)
- **references/best-practices.md** - Quality checklist, common pitfalls, writing guidelines, template structure

Load these references as needed when creating commands to understand patterns, see examples, or ensure quality.

## Command Structure Overview

Every slash command is a markdown file with:

```markdown
---
description: Brief description shown in /help (required)
argument-hint: <placeholder> (optional, if the command takes arguments)
---

# Command Title

[Detailed instructions for the agent to execute autonomously]
```

## Command Creation Workflow

### Step 1: Determine Location

**Automatically detect the appropriate location:**

1. Check git repository status: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Default location:
   - If in git repository → Project level: `.claude/commands/`
   - If not in git repository → Global: `~/.claude/commands/`
3. Allow user override:
   - If user explicitly mentions "global" or "user level" → Use `~/.claude/commands/`
   - If user explicitly mentions "project" or "project level" → Use `.claude/commands/`

Report the chosen location to the user before proceeding.

### Step 2: Show Command Patterns

Help the user understand different command types. Load **references/patterns.md** to see available patterns:

- **Workflow Automation** - Analyze → Act → Report (e.g., submit-stack)
- **Iterative Fix** - Execute → Analyze → Fix → Repeat (e.g., ensure-ci)
- **Agent Delegation** - Context → Delegate → Iterate (e.g., create-implementation-plan)
- **Simple Execution** - Run command with arguments (e.g., codex-review)

Match the request to the closest existing pattern. This helps frame the conversation.

### Step 3: Gather Command Information

Gather key information from the request; ask only for what is genuinely missing:

#### A. Command Name and Purpose

Ask:

- "What should the command be called?" (for filename)
- "What does this command do?" (for description field)

Guidelines:

- Command names MUST be kebab-case (hyphens, NOT underscores)
  - ✅ CORRECT: `submit-stack`, `ensure-ci`, `create-from-plan`
  - ❌ WRONG: `submit_stack`, `ensure_ci`, `create_from_plan`
- Filenames match command names: `my-command.md` → invoked as `/my-command`
- Description should be concise, action-oriented (appears in `/help` output)

#### B. Arguments

Ask:

- "Does this command take any arguments?"
- "Are arguments required or optional?"
- "What should the arguments represent?"

If the command takes arguments:

- Add `argument-hint: <placeholder>` to the frontmatter
- Use `<angle-brackets>` for required arguments
- Use `[square-brackets]` for optional arguments

#### C. Workflow Steps

Ask:

- "What specific steps should this command follow?"
- "In what order should they happen?"
- "What tools or commands should be used?"

Gather details about:

- Initial analysis or checks to perform
- Main actions to take
- How to handle results
- Success criteria
- Error handling approach

#### D. Tool Constraints and Guidance

Ask:

- "Should this command use any specific agents or tools?"
- "Are there tools or operations that should be avoided?"
- "Should it read any specific files for context?"

### Step 4: Generate Optimized Command

Create the command file with agent-optimized instructions. Load **references/best-practices.md** for:

- Template structure
- Best practices for agent execution
- Writing style guidelines
- Quality checklist

Key principles:

- Use imperative form (instructions starting with a verb)
- Be explicit and specific
- Include expected results
- Provide concrete examples
- Define clear error handling

### Step 5: Create the Command File

1. Determine the full file path:
   - Project: `.claude/commands/[command-name].md`
   - Global: `~/.claude/commands/[command-name].md`

2. Ensure the directory exists:

   ```bash
   mkdir -p [directory-path]
   ```

3. Write the command file using the Write tool

4. Report to the user:
   - Report the file location
   - Summarize what the command does
   - Explain how to use: `/command-name [arguments]`

### Step 6: Test and Iterate (Optional)

If the user wants to test:

1. Suggest testing: `You can test this command by running: /command-name [arguments]`
2. Be ready to iterate based on feedback
3. Update the file with improvements as needed

## Quick Tips

**For detailed guidance, load the included references:**

- Load **references/patterns.md** when designing the command workflow
- Load **references/examples.md** to see how existing commands are structured
- Load **references/best-practices.md** before finalizing to ensure quality

**Common patterns to remember:**

- Use Bash tool for `pytest`, `pyright`, `ruff`, `prettier`, `make`, `gt` commands
- Use Task tool to invoke subagents for specialized tasks
- Check for specific files first (e.g., `.PLAN.md`) before proceeding
- Mark all as complete immediately, not in batches
- Include explicit error handling instructions
- Define clear success criteria

## Summary

When creating a command:

1. **Detect location** (project vs global)
2. **Show patterns** to frame the conversation
3. **Gather information** (name, purpose, arguments, steps, tools)
4. **Generate optimized command** with agent-executable instructions
5. **Create file** in the appropriate location
6. **Confirm and iterate** as needed

Focus on creating commands that agents can execute autonomously, with clear steps, explicit tool usage, and proper error handling.

## Scope and Limitations

This skill creates Claude Code slash commands — reusable workflow definitions that agents can invoke. It covers command structure, argument handling, tool usage instructions, and best practices for agent-executable commands.

It does not cover: custom hooks (use the hook-development skill), MCP server implementation, plugin manifest authoring, or skill creation (use the skill-creator skill). Commands are designed for agent execution within Claude Code — they are not standalone scripts or external tools.
