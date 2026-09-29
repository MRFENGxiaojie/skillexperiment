---
name: plugin-settings
description: "This skill should be used when the user asks about \"plugin settings\", \"store plugin configuration\", \"user-configurable plugin\", \".local.md files\", \"plugin state files\", \"read YAML frontmatter\", \"per-project plugin settings\", or wants to make plugin behavior configurable. Documents the .claude/plugin-name.local.md pattern for storing plugin-specific configuration with YAML frontmatter and markdown content."
---

## Interaction policy

Work autonomously by default: do not proactively ask the user questions, request confirmation, or ask for choices. Only interact when the task explicitly requires it, or when essential information genuinely cannot be obtained from the provided materials/tools; otherwise decide and proceed from available evidence.

# Plugin Settings Pattern for Claude Code Plugins


## Overview

Plugins can store user-configurable settings and state in `.claude/plugin-name.local.md` files within the project directory. This pattern uses YAML frontmatter for structured configuration and markdown content for prompts or additional context.

**Key features:**
- File location: `.claude/plugin-name.local.md` at the project root
- Structure: YAML frontmatter + markdown body
- Purpose: Per-project plugin configuration and state
- Usage: Read in hooks, commands, and agents
- Lifecycle: User-managed (not in git, should be in `.gitignore`)


## File Structure

### Basic Template

```markdown
---
enabled: true
setting1: value1
setting2: value2
numeric_setting: 42
list_setting: ["item1", "item2"]
---

# Additional Context

The markdown body can contain:
- Task descriptions
- Additional instructions
- Prompts for feedback to Claude
- Documentation or notes
```

### Example: Plugin State File

**.claude/my-plugin.local.md:**
```markdown
---
enabled: true
strict_mode: false
max_retries: 3
notification_level: info
coordinator_session: team-leader
---

# Plugin Configuration

This plugin is configured for standard validation mode.
Contact @team-lead with questions.
```


## Reading Configuration Files

### From Hooks (Bash Scripts)

**Pattern: Check existence and parse frontmatter**

```bash
#!/bin/bash
set -euo pipefail

# Define state file path
STATE_FILE=".claude/my-plugin.local.md"

# Quick exit if file does not exist
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0  # Plugin not configured, ignore
fi

# Parse YAML frontmatter (between --- markers)
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")

# Extract individual fields
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//' | sed 's/^"\(.*\)"$/\1/')
STRICT_MODE=$(echo "$FRONTMATTER" | grep '^strict_mode:' | sed 's/strict_mode: *//' | sed 's/^"\(.*\)"$/\1/')

# Check if enabled
if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Use configuration in hook logic
if [[ "$STRICT_MODE" == "true" ]]; then
  # Apply strict validation
  # ...
fi
```

See `examples/read-settings-hook.sh` for complete working example.

### From Commands

Commands can read configuration files to customize behavior:

```markdown
---
description: Process data with plugin
allowed-tools: ["Read", "Bash"]
---

# Processing Command

Steps:
1. Check if settings exist in `.claude/my-plugin.local.md`
2. Read configuration using Read tool
3. Parse YAML frontmatter to extract settings
4. Apply settings to processing logic
5. Execute with configured behavior
```

### From Agents

Agents can reference settings in their instructions:

```markdown
---
name: plugin-settings
description: Agent that adapts to project settings
---

Check for plugin settings in `.claude/my-plugin.local.md`.
If present, parse YAML frontmatter and adapt behavior accordingly:
- enabled: Whether the plugin is active
- mode: Processing mode (strict, standard, lenient)
- Additional configuration fields
```


## Parsing Techniques

### Extract Frontmatter

```bash
# Extract everything between --- markers
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$FILE")
```

### Read Individual Fields

**String fields:**
```bash
VALUE=$(echo "$FRONTMATTER" | grep '^field_name:' | sed 's/field_name: *//' | sed 's/^"\(.*\)"$/\1/')
```

**Boolean fields:**
```bash
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')
# Compare: if [[ "$ENABLED" == "true" ]]; then
```

**Numeric fields:**
```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')
# Use: if [[ $MAX -gt 100 ]]; then
```

### Read Markdown Body

Extract content after the second `---`:

```bash
# Get everything after the closing ---
BODY=$(awk '/^---$/{i++; next} i>=2' "$FILE")
```


## Common Patterns

### Pattern 1: Temporarily Active Hooks

Use configuration file to control hook activation:

```bash
#!/bin/bash
STATE_FILE=".claude/security-scan.local.md"

# Quick exit if not configured
if [[ ! -f "$STATE_FILE" ]]; then
  exit 0
fi

# Read enabled flag
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ENABLED=$(echo "$FRONTMATTER" | grep '^enabled:' | sed 's/enabled: *//')

if [[ "$ENABLED" != "true" ]]; then
  exit 0  # Disabled
fi

# Execute hook logic
# ...
```

**Use case:** Enable/disable hooks without editing hooks.json (requires restart).

### Pattern 2: Agent State Management

Store agent-specific state and configuration:

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-agent
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
---

# Task Assignment

Implement JWT authentication for the API.

**Success Criteria:**
- Authentication endpoints created
- Tests passing
- PR created and CI green
```

Read from hooks to coordinate agents:

```bash
AGENT_NAME=$(echo "$FRONTMATTER" | grep '^agent_name:' | sed 's/agent_name: *//')
COORDINATOR=$(echo "$FRONTMATTER" | grep '^coordinator_session:' | sed 's/coordinator_session: *//')

# Send notification to coordinator
tmux send-keys -t "$COORDINATOR" "Agent $AGENT_NAME completed task" Enter
```

### Pattern 3: Configuration-Driven Behavior

**.claude/my-plugin.local.md:**
```markdown
---
validation_level: strict
max_file_size: 1000000
allowed_extensions: [".js", ".ts", ".tsx"]
enable_logging: true
---

# Validation Configuration

Strict mode enabled for this project.
All writes validated against security policies.
```

Use in hooks or commands:

```bash
LEVEL=$(echo "$FRONTMATTER" | grep '^validation_level:' | sed 's/validation_level: *//')

case "$LEVEL" in
  strict)
    # Apply strict validation
    ;;
  standard)
    # Apply standard validation
    ;;
  lenient)
    # Apply permissive validation
    ;;
esac
```


## Creating Configuration Files

### From Commands

Commands can create configuration files:

```markdown
# Setup Command

Steps:
1. Determine the configuration from the project context or the documented defaults
2. Create `.claude/my-plugin.local.md` with YAML frontmatter
3. Set the resolved values in the file
4. Confirm that the settings file was saved
5. Remind the user to restart Claude Code for hooks to recognize changes
```

### Template Generation

Provide template in plugin documentation:

```markdown

## Configuration

Create `.claude/my-plugin.local.md` in your project:

\`\`\`markdown
---
enabled: true
mode: standard
max_retries: 3
---

# Plugin Configuration

Your settings are active.
\`\`\`

After creating or editing, restart Claude Code for changes to take effect.
```


## Best Practices

### File Naming

DO:
- Use `.claude/plugin-name.local.md` format
- Match plugin name exactly
- Use `.local.md` suffix for user-local files

DON'T:
- Use a different directory (not `.claude/`)
- Use inconsistent naming
- Use `.md` without `.local` (may be committed)

### Gitignore

Always add to `.gitignore`:

```gitignore
.claude/*.local.md
.claude/*.local.json
```

Document this in the plugin README.

### Default Patterns

Provide sensible defaults when configuration file does not exist:

```bash
if [[ ! -f "$STATE_FILE" ]]; then
  # Use defaults
  ENABLED=true
  MODE=standard
else
  # Read from file
  # ...
fi
```

### Validation

Validate configuration values:

```bash
MAX=$(echo "$FRONTMATTER" | grep '^max_value:' | sed 's/max_value: *//')

# Validate numeric range
if ! [[ "$MAX" =~ ^[0-9]+$ ]] || [[ $MAX -lt 1 ]] || [[ $MAX -gt 100 ]]; then
  echo "⚠️  Invalid max_value in settings (must be 1-100)" >&2
  MAX=10  # Use default
fi
```

### Restart Requirement

**Important:** Configuration changes require Claude Code restart.

Document in your README:

```markdown

## Changing Settings

After editing `.claude/my-plugin.local.md`:
1. Save the file
2. Exit Claude Code
3. Restart: `claude` or `cc`
4. New settings will be loaded
```

Hooks cannot be hot-swapped within a session.


## Security Considerations

### Sanitize User Input

When writing configuration files from user input:

```bash
# Escape quotes in user input
SAFE_VALUE=$(echo "$USER_INPUT" | sed 's/"/\\"/g')

# Write to file
cat > "$STATE_FILE" <<EOF
---
user_setting: "$SAFE_VALUE"
---
EOF
```

### Validate File Paths

If settings contain file paths:

```bash
FILE_PATH=$(echo "$FRONTMATTER" | grep '^data_file:' | sed 's/data_file: *//')

# Check for directory traversal
if [[ "$FILE_PATH" == *".."* ]]; then
  echo "⚠️  Invalid path in settings (directory traversal)" >&2
  exit 2
fi
```

### Permissions

Configuration files should be:
- Readable only by the user (`chmod 600`)
- Not committed to git
- Not shared between users


## Real-World Examples

### multi-agent-swarm Plugin

**.claude/multi-agent-swarm.local.md:**
```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: Use JWT tokens, not sessions
---

# Task: Implement Authentication

Build JWT-based authentication for the REST API.
Coordinate with auth-agent on shared types.
```

**Hook usage (agent-stop-notification.sh):**
- Checks if file exists (lines 15-18: quick exit if not)
- Parses frontmatter to get coordinator_session, agent_name, enabled
- Sends notifications to coordinator if enabled
- Allows quick activation/deactivation via `enabled: true/false`

### ralph-wiggum Plugin

**.claude/ralph-loop.local.md:**
```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
---

Fix all lint errors in the project.
Ensure tests pass after each fix.
```

**Hook usage (stop-hook.sh):**
- Checks if file exists (lines 15-18: quick exit if not active)
- Reads iteration count and max_iterations
- Extracts completion_promise for loop termination
- Reads body as prompt for feedback
- Updates iteration count each loop


## Reference Files

- **Additional Resources**: see [references/additional-resources.md](references/additional-resources.md)
- **Implementation Workflow**: see [references/implementation-workflow.md](references/implementation-workflow.md)
- **Quick Reference**: see [references/quick-reference.md](references/quick-reference.md)

## Scope and Limitations

Use this skill when the task involves per-project plugin configuration stored in `.claude/plugin-name.local.md` files (YAML frontmatter + markdown body), read from hooks, commands, or agents.

Do NOT use this skill when:
- The configuration must be shared across users or machines — `.local.md` files are per-project and user-local by design.
- The settings contain secrets or credentials — use the OS secret store or environment variables instead; `.local.md` files are plain text (chmod 600 is a mild protection, not encryption).
- The task concerns Claude Code's own configuration (settings.json, hooks.json) — that is managed by the harness, not by the plugin pattern.
- The plugin needs a settings UI or multi-user management — this skill documents a plain-text convention, not a configuration service.

Limitations:
- The sed/grep parsing snippets handle flat, single-line scalar values. For nested or complex YAML, use yq (see references/parsing-techniques.md).
- Hook definitions cannot be hot-swapped within a session; settings file changes are picked up on the next hook trigger (see Best Practices).

## Output Format

This skill delivers:

1. **The settings file** — `.claude/<plugin-name>.local.md` with YAML frontmatter (typed values: string/boolean/numeric/list) plus a markdown body for prompts or context (see File Structure).
2. **Parsing code** — the snippets for hooks, commands, and agents that read the settings at runtime (see Reading Configuration Files and Parsing Techniques).
3. **Plugin documentation** — the configuration template, `.gitignore` entry, and restart note for the plugin README (see Best Practices).
