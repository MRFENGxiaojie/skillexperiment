---
name: plugin-structure
description: "Provides guidance on Claude Code plugin directory structure, plugin.json manifest configuration, and component organization. Use when the user asks to create a plugin, structure a plugin, understand plugin structure, organize plugin components, configure plugin.json, use ${CLAUDE_PLUGIN_ROOT}, add commands/agents/skills/hooks, configure auto-discovery, or needs guidance on plugin directory layout, manifest configuration, component organization, file naming conventions, or Claude Code plugin architecture best practices."
allowed-tools: Read, Write, Bash, Glob
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Plugin Structure for Claude Code

## Overview

Claude Code plugins follow a standardized directory structure with automatic component discovery. Understanding this structure allows you to create well-organized and maintainable plugins that integrate seamlessly with Claude Code.

**Key concepts:**
- Conventional directory layout for automatic discovery
- Manifest-driven configuration in `.claude-plugin/plugin.json`
- Component-based organization (commands, agents, skills, hooks)
- Portable path references using `${CLAUDE_PLUGIN_ROOT}`
- Explicit loading vs. automatic component discovery

## Workflow / Process

When the user asks to create or structure a plugin, follow these steps:

1. **Confirm the plugin name and component scope.** Ask which components the plugin needs (commands, agents, skills, hooks, MCP servers) and pick a pattern:
   - **Minimal** — single command or two, no dependencies
   - **Full** — multiple component types with shared scripts and integrations
   - **Skills-focused** — only skills and their resources
   When in doubt, start minimal; add components only when the plugin actually uses them.

2. **Create the directory tree.** Follow the structure in the next section, creating only the directories the plugin will use (Critical Rules 2-3).

3. **Write `.claude-plugin/plugin.json`.** Start with the required `name` field, add recommended metadata, and set custom paths only when components live outside the default directories.

4. **Create the component files.** Commands and agents are `.md` files with YAML frontmatter; skills are directories containing `SKILL.md`; hooks use `hooks/hooks.json`; MCP servers use `.mcp.json`.

5. **Reference paths with `${CLAUDE_PLUGIN_ROOT}`.** Replace every hardcoded or working-directory path, and verify manifest paths start with `./` and stay relative.

6. **Self-check.** Walk through the Troubleshooting questions: components in the right place, correct extensions, valid frontmatter, manifest paths pointing at existing files.

Each step's output feeds the next: step 1 decides the tree, the tree decides the manifest, and so on. For a request that only asks how plugin structure works (no build task), skip to the relevant section and explain rather than execute the flow.

## Directory Structure

Every Claude Code plugin follows this organizational pattern:

### plugin-name/
- .claude-plugin/
  - plugin.json          # Required: Plugin manifest
- commands/                 # Slash commands (.md files)
- agents/                   # Subagent definitions (.md files)
- skills/                   # Agent skills (subdirectories)
  - skill-name/
    - SKILL.md         # Required for each skill
- hooks/
  - hooks.json           # Event handler configuration
- .mcp.json                # MCP server definitions
- scripts/                 # Helper scripts and utilities

**Critical rules:**

1. **Manifest location**: The `plugin.json` manifest MUST be in the `.claude-plugin/` directory
2. **Component locations**: All component directories (commands, agents, skills, hooks) MUST be at the plugin root level, NOT nested inside `.claude-plugin/`
3. **Optional components**: Only create directories for components the plugin actually uses
4. **Naming convention**: Use kebab-case for all directory and file names

## Plugin Manifest (plugin.json)

The manifest defines plugin metadata and configuration. Located in `.claude-plugin/plugin.json`:

### Required Fields

```json
{
  "name": "plugin-name"
}
```

**Name requirements:**
- Use kebab-case format (lowercase with hyphens)
- Must be unique among installed plugins
- No spaces or special characters
- Example: `code-review-assistant`, `test-runner`, `api-docs`

### Recommended Metadata

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief explanation of the plugin's purpose",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "homepage": "https://docs.example.com",
  "repository": "https://github.com/user/plugin-name",
  "license": "MIT",
  "keywords": ["testing", "automation", "ci-cd"]
}
```

**Version format**: Follow semantic versioning (MAJOR.MINOR.PATCH)
**Keywords**: Use for plugin discovery and categorization

### Component Path Configuration

Specify custom paths for components (complement default directories):

```json
{
  "name": "plugin-name",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

**Important**: Custom paths complement defaults—they do not replace them. Components in both default directories and custom paths will be loaded.

**Path rules:**
- Must be relative to the plugin root
- Must start with `./`
- Cannot use absolute paths
- Support arrays for multiple locations

## Component Organization

### Commands

**Location**: `commands/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `commands/` are loaded automatically

**Example structure**:
### commands/
- review.md        # /review command
- test.md          # /test command
- deploy.md        # /deploy command

**File format**:
```markdown
---
name: example-command
description: Command description
---

Command implementation instructions...
```

**Usage**: Commands integrate as native slash commands in Claude Code

### Agents

**Location**: `agents/` directory
**Format**: Markdown files with YAML frontmatter
**Auto-discovery**: All `.md` files in `agents/` are loaded automatically

**Example structure**:
### agents/
- code-reviewer.md
- test-generator.md
- refactorer.md

**File format**:
```markdown
---
description: Agent role and expertise
capabilities:
  - Specific task 1
  - Specific task 2
---

Detailed agent instructions and knowledge...
```

**Usage**: Users can invoke agents manually, or Claude Code selects them automatically based on task context

### Skills

**Location**: `skills/` directory with subdirectories per skill
**Format**: Each skill in its own directory with a `SKILL.md` file
**Auto-discovery**: All `SKILL.md` files in skill subdirectories are loaded automatically

**Example structure**:
### skills/
- api-testing/
  - SKILL.md
  - scripts/
    - test-runner.py
  - references/
    - api-spec.md
- database-migrations/
  - SKILL.md
  - examples/
    - migration-template.sql

**SKILL.md format**:
```markdown
---
name: example-skill-name
description: When to use this skill
---

Skill instructions and guidance...
```

**Support files**: Skills can include scripts, references, examples, or assets in subdirectories

**Usage**: Claude Code autonomously activates skills based on task context matching the description

### Hooks

**Location**: `hooks/hooks.json` or inline in `plugin.json`
**Format**: JSON configuration defining event handlers
**Registration**: Hooks register automatically when the plugin is enabled

**Example structure**:
### hooks/
- hooks.json           # Hooks configuration
- scripts/
  - validate.sh      # Hook script
  - check-style.sh   # Hook script

**Configuration format**:
```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
      "timeout": 30
    }]
  }]
}
```

**Available events**: PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification

**Usage**: Hooks execute automatically in response to Claude Code events

### MCP Servers

**Location**: `.mcp.json` at plugin root or inline in `plugin.json`
**Format**: JSON configuration for MCP server definitions
**Auto-start**: Servers start automatically when the plugin is enabled

**Example format**:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Usage**: MCP servers integrate seamlessly into Claude Code's tool system

## Portable Path References

### ${CLAUDE_PLUGIN_ROOT}

Use the `${CLAUDE_PLUGIN_ROOT}` environment variable for all intra-plugin path references:

```json
{
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

**Why it matters**: Plugins install in different locations depending on:
- User installation method (marketplace, local, npm)
- Operating system conventions
- User preferences

**Where to use**:
- Hook command paths
- MCP server command arguments
- Script execution references
- Resource file paths

**Never use**:
- Hardcoded absolute paths (`/Users/name/plugins/...`)
- Working directory relative paths (`./scripts/...` in commands)
- Home directory shortcuts (`~/plugins/...`)

### Path Resolution Rules

**In manifest JSON fields** (hooks, MCP servers):
```json
"command": "${CLAUDE_PLUGIN_ROOT}/scripts/tool.sh"
```

**In component files** (commands, agents, skills):
```markdown
Reference scripts at: ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py
```

**In executed scripts**:
```bash
#!/bin/bash
# ${CLAUDE_PLUGIN_ROOT} available as environment variable
source "${CLAUDE_PLUGIN_ROOT}/lib/common.sh"
```

**Expansion mechanism**: `${CLAUDE_PLUGIN_ROOT}` is expanded by the shell (bash, `sh -c` command strings, MCP server launch commands). In interpreted languages, read it from the environment instead — e.g. `process.env.CLAUDE_PLUGIN_ROOT` in Node.js or `os.environ["CLAUDE_PLUGIN_ROOT"]` in Python. A literal `${CLAUDE_PLUGIN_ROOT}` inside a `require()` or `open()` call is not expanded and will fail at runtime.

## File Naming Conventions

### Component Files

**Commands**: Use `.md` files in kebab-case
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`
- `api-docs.md` → `/api-docs`

**Agents**: Use `.md` files in kebab-case describing role
- `test-generator.md`
- `code-reviewer.md`
- `performance-analyzer.md`

**Skills**: Use kebab-case directory names
- `api-testing/`
- `database-migrations/`
- `error-handling/`

### Support Files

**Scripts**: Use descriptive kebab-case names with appropriate extensions
- `validate-input.sh`
- `generate-report.py`
- `process-data.js`

**Documentation**: Use kebab-case markdown files
- `api-reference.md`
- `migration-guide.md`
- `best-practices.md`

**Configuration**: Use standard names
- `hooks.json`
- `.mcp.json`
- `plugin.json`

## Auto-Discovery Mechanism

Claude Code discovers and loads components automatically:

1. **Plugin manifest**: Reads `.claude-plugin/plugin.json` when the plugin is enabled
2. **Commands**: Checks `commands/` directory for `.md` files
3. **Agents**: Checks `agents/` directory for `.md` files
4. **Skills**: Checks `skills/` for subdirectories containing `SKILL.md`
5. **Hooks**: Loads configuration from `hooks/hooks.json` or manifest
6. **MCP servers**: Loads configuration from `.mcp.json` or manifest

**Discovery timing**:
- Plugin installation: Components register with Claude Code
- Plugin enabled: Components become available for use
- No restart needed at install time: component changes take effect when Claude Code starts the next session

**Override behavior**: Custom paths in `plugin.json` complement (do not replace) default directories

## Output Format

For a plugin creation or structuring request, deliver:

1. **The directory tree** as a code block — every directory and file the plugin needs, following the conventions in this skill.
2. **The content of each file** — `plugin.json`, command/agent `.md` files with frontmatter, `SKILL.md` files, `hooks.json`, and `.mcp.json`, complete enough to be used directly.
3. **A loading explanation** — which components auto-discover, how the manifest points to the rest, and when changes take effect (installation registers components; changes apply from the next Claude Code session).

For an explanation request (how plugin structure works), the deliverable is a walkthrough of the relevant structure with a small example rather than a full plugin.

## Scope and Limitations

**Covers:** plugin directory layout, `plugin.json` manifest configuration, component organization (commands, agents, skills, hooks, MCP servers), path portability, naming, and auto-discovery behavior for Claude Code plugins.

**Out of scope:**
- Plugin packaging and publishing (marketplace listing, distribution) — this skill ends at a working plugin directory.
- Hook script implementation logic — this skill covers where hooks live and how they register, not how to write the scripts themselves.
- MCP server internals — server implementations are their own project; this skill only covers wiring `.mcp.json` and paths.
- Plugin dependency management and update mechanics.

**When not to use:** requests about publishing a plugin, writing a single hook script in isolation, or building an MCP server itself are better served elsewhere.

## Best Practices

### Organization

1. **Logical grouping**: Group related components together
   - Place testing-related commands, agents, and skills together
   - Create subdirectories in `scripts/` for different purposes

2. **Minimal manifest**: Keep `plugin.json` lean
   - Specify custom paths only when necessary
   - Rely on auto-discovery for standard layouts
   - Use inline configuration only for simple cases

3. **Documentation**: Include README files
   - Plugin root: Overall purpose and usage
   - Component directories: Specific guidance
   - Script directories: Usage and requirements

### Naming

1. **Consistency**: Use consistent naming across components
   - If command is `test-runner`, name related agent `test-runner-agent`
   - Match skill directory names with their purpose

2. **Clarity**: Use descriptive names that indicate purpose
   - Good: `api-integration-testing/`, `code-quality-checker.md`
   - Avoid: `utils/`, `misc.md`, `temp.sh`

3. **Length**: Balance brevity with clarity
   - Commands: 2-3 words (`review-pr`, `run-ci`)
   - Agents: Describe role clearly (`code-reviewer`, `test-generator`)
   - Skills: Topic-focused (`error-handling`, `api-design`)

### Portability

1. **Always use ${CLAUDE_PLUGIN_ROOT}**: Never hardcode paths
2. **Test on multiple systems**: Verify on macOS, Linux, Windows
3. **Document dependencies**: List required tools and versions
4. **Avoid system-specific features**: Use portable bash/Python constructs

### Maintenance

1. **Version consistently**: Update version in plugin.json for releases
2. **Deprecate gracefully**: Mark old components clearly before removal
3. **Document breaking changes**: Note changes affecting existing users
4. **Test thoroughly**: Verify all components work after changes

## Common Patterns

### Minimal Plugin

Single command with no dependencies:
### my-plugin/
- .claude-plugin/
  - plugin.json    # name field only
- commands/
  - hello.md       # Single command

### Full Plugin

Complete plugin with all component types:
### my-plugin/
- .claude-plugin/
  - plugin.json
- commands/          # User-facing commands
- agents/            # Specialized subagents
- skills/            # Auto-activating skills
- hooks/             # Event handlers
  - hooks.json
  - scripts/
- .mcp.json          # External integrations
- scripts/           # Shared utilities

### Skills-Focused Plugin

Plugin providing only skills:
### my-plugin/
- .claude-plugin/
  - plugin.json
- skills/
  - skill-one/
    - SKILL.md
  - skill-two/
    - SKILL.md

## Troubleshooting

**Component is not loading**:
- Check that the file is in the correct directory with the correct extension
- Verify YAML frontmatter syntax (commands, agents, skills)
- Ensure skill has `SKILL.md` (not `README.md` or other name)
- Confirm plugin is enabled in Claude Code settings

**Path resolution errors**:
- Replace all hardcoded paths with `${CLAUDE_PLUGIN_ROOT}`
- Verify that paths are relative and start with `./` in manifest
- Check that referenced files exist at specified paths
- Test with `echo $CLAUDE_PLUGIN_ROOT` in hook scripts

**Auto-discovery is not working**:
- Confirm that directories are at the plugin root (not in `.claude-plugin/`)
- Verify file naming follows conventions (kebab-case, correct extensions)
- Check that custom paths in manifest are correct
- Restart Claude Code to reload plugin configuration

**Conflicts between plugins**:
- Use unique, descriptive component names
- Namespace commands with plugin name if necessary
- Document potential conflicts in plugin README
- Consider command prefixes for related functionality

---

For detailed examples and advanced patterns, see files in the `references/` and `examples/` directories.

