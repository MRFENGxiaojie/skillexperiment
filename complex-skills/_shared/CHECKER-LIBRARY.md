# Checker Function Library

Standard Python functions for `judge: script` evaluation. Each function returns `bool` (True=pass, False=fail).
The evaluation runner resolves `${VARIABLES}` before calling functions.

## Runner-Injected Variables

| Variable | Description |
|----------|-------------|
| `${WORKSPACE}` | Agent working directory root |
| `${TOOL_LOG}` | Tool call transcript (JSONL, one call per line) |
| `${AGENT_OUTPUT}` | Agent's full text output |
| `${SKILL_DIR}` | The skill directory containing SKILL.md |

Skill-specific variables (e.g., `${STATE_JSON}`, `${TARGET_SKILL}`) are defined per SCORING.yaml
and resolved by the runner from the skill's own documentation.

---

## File Checks

### file_exists
```python
def file_exists(path: str) -> bool:
    """Verify file or directory exists at path."""
```
| parameter | type | description |
|-----------|------|-------------|
| path | str | Glob-supported path relative to ${WORKSPACE} |

### file_not_exists
```python
def file_not_exists(path: str) -> bool:
    """Verify file or directory does NOT exist at path."""
```

### file_contains
```python
def file_contains(path: str, pattern: str) -> bool:
    """Verify file contains a line matching regex pattern."""
```
| parameter | type | description |
|-----------|------|-------------|
| path | str | File path relative to ${WORKSPACE} |
| pattern | str | Regex pattern (Python re syntax) |

### file_valid_json
```python
def file_valid_json(path: str) -> bool:
    """Verify file is parseable as valid JSON."""
```

### file_has_extension
```python
def file_has_extension(path: str, extensions: list[str]) -> bool:
    """Verify file has one of the expected extensions."""
```

---

## JSON Checks

All JSON checks first validate the file is parseable JSON, then apply the jq expression.

### json_field_exists
```python
def json_field_exists(path: str, jq: str, min_present: int = 1) -> bool:
    """Verify at least min_present of the comma-separated jq paths are non-null and non-empty."""
```
| parameter | type | description |
|-----------|------|-------------|
| path | str | JSON file path |
| jq | str | Comma-separated jq expressions, e.g. ".a, .b.c, .d[0]" |
| min_present | int | Minimum number that must be non-null (default 1) |

### json_field_equals
```python
def json_field_equals(path: str, jq: str, expected: str) -> bool:
    """Verify JSON field value equals expected string."""
```

### json_field_matches
```python
def json_field_matches(path: str, jq: str, pattern: str) -> bool:
    """Verify JSON field value matches regex pattern."""
```

### json_array_nonempty
```python
def json_array_nonempty(path: str, jq: str) -> bool:
    """Verify JSON array at jq path exists and has length > 0."""
```

### json_array_length
```python
def json_array_length(path: str, jq: str, min: int, max: int = None) -> bool:
    """Verify JSON array length is >= min and (if max set) <= max."""
```

### json_array_all_have_keys
```python
def json_array_all_have_keys(path: str, jq: str, keys: list[str]) -> bool:
    """Verify every element in the JSON array has all specified keys with non-null values."""
```

---

## Timestamp Checks

### timestamp_before
```python
def timestamp_before(path_a: str, path_b: str) -> bool:
    """Verify file at path_a was last modified before file at path_b."""
```

### timestamp_after
```python
def timestamp_after(path_a: str, path_b: str) -> bool:
    """Verify file at path_a was last modified after file at path_b."""
```

---

## Tool Log Checks

Tool log is a JSONL file where each line records one tool call:
`{"tool": "Read|Write|Edit|Bash|Glob|Grep|...", "args": {...}, "timestamp": "..."}`

### tool_log_contains
```python
def tool_log_contains(pattern: str) -> bool:
    """Verify tool log contains at least one call matching regex pattern (matched against JSON line)."""
```

### tool_log_not_contains
```python
def tool_log_not_contains(pattern: str) -> bool:
    """Verify tool log contains NO call matching regex pattern."""
```

### tool_log_read_before_write
```python
def tool_log_read_before_write(reads: list[str], require_all: bool = True) -> bool:
    """Verify Read calls for specified files occurred before any Write/Edit call.
    If require_all=True, ALL listed files must have been read first."""
```
| parameter | type | description |
|-----------|------|-------------|
| reads | list[str] | File path patterns that must be Read |
| require_all | bool | If True, all patterns must match; if False, any one is sufficient |

### tool_log_order
```python
def tool_log_order(first: str, second: str) -> bool:
    """Verify a call matching 'first' pattern occurs BEFORE a call matching 'second' pattern."""
```

---

## Output Checks

### output_contains
```python
def output_contains(pattern: str) -> bool:
    """Verify agent's text output contains a line matching regex pattern."""
```

### output_not_contains
```python
def output_not_contains(pattern: str) -> bool:
    """Verify agent's text output does NOT contain pattern."""
```

---

## LLM Judge Checks

For `judge: llm` items, the `check` field is a structured prompt fragment:

```yaml
check:
  question: "<yes/no question the LLM judge must answer>"
  evidence: "<what part of the agent's output/log to examine>"
```

The LLM judge receives: `{skill_content} + {task_prompt} + {agent_output} + {tool_log} + {question} + {evidence}`
and must return `{verdict: "yes"|"no", reasoning: "..."}`.
