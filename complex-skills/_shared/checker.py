"""
Checker function library for SCORING.yaml evaluation.
Each function returns bool (True=pass, False=fail).

The runner resolves ${VARIABLES} before calling these functions.
Functions receive resolved paths and patterns as arguments.
"""

import json
import os
import re
import glob as globmod
from pathlib import Path as _Path  # internal use only


# ═══════════════════════════════════════════════════════════
# File Checks
# ═══════════════════════════════════════════════════════════

def file_exists(path: str) -> bool:
    """Verify file or directory exists. Supports glob patterns."""
    matches = globmod.glob(path, recursive=True)
    return len(matches) > 0 and any(os.path.exists(m) for m in matches)


def file_not_exists(path: str) -> bool:
    """Verify file or directory does NOT exist."""
    return not file_exists(path)


def file_contains(path: str, pattern: str) -> bool:
    """Verify file contains at least one line matching regex pattern.
    For glob paths, checks the first matching file."""
    matches = globmod.glob(path, recursive=True)
    if not matches:
        return False
    target = matches[0]
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return bool(re.search(pattern, content, re.MULTILINE))
    except (OSError, IsADirectoryError):
        return False


def file_valid_json(path: str) -> bool:
    """Verify file is parseable as valid JSON."""
    matches = globmod.glob(path, recursive=True)
    if not matches:
        return False
    try:
        with open(matches[0], "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, OSError):
        return False


def file_has_extension(path: str, extensions: list) -> bool:
    """Verify file has one of the expected extensions (case-insensitive)."""
    matches = globmod.glob(path, recursive=True)
    if not matches:
        return False
    ext = os.path.splitext(matches[0])[1].lower()
    expected = [e.lower() if e.startswith(".") else f".{e.lower()}" for e in extensions]
    return ext in expected


# ═══════════════════════════════════════════════════════════
# JSON Checks
# ═══════════════════════════════════════════════════════════

def _load_json(path: str) -> dict | list | None:
    """Internal: load JSON from path (supports glob)."""
    matches = globmod.glob(path, recursive=True)
    if not matches:
        return None
    try:
        with open(matches[0], "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _jq_get(data, expr: str):
    """Minimal jq-like field access. Supports .a.b, .a[0], .a.b[0].c"""
    parts = re.findall(r'\.([^.[]+)|\[(\d+)\]', expr)
    result = data
    for name, index in parts:
        if name:
            if isinstance(result, dict):
                result = result.get(name)
            else:
                return None
        if index:
            try:
                result = result[int(index)]
            except (IndexError, TypeError, KeyError):
                return None
        if result is None:
            return None
    return result


def json_field_exists(path: str, jq: str, min_present: int = 1) -> bool:
    """Verify at least min_present of comma-separated jq paths are non-null/non-empty."""
    data = _load_json(path)
    if data is None:
        return False
    exprs = [e.strip() for e in jq.split(",")]
    count = 0
    for expr in exprs:
        val = _jq_get(data, expr)
        if val is not None and val != "" and val != [] and val != {}:
            count += 1
    return count >= min_present


def json_field_equals(path: str, jq: str, expected: str) -> bool:
    """Verify JSON field value equals expected string."""
    data = _load_json(path)
    if data is None:
        return False
    val = _jq_get(data, jq)
    return str(val) == expected if val is not None else False


def json_field_matches(path: str, jq: str, pattern: str) -> bool:
    """Verify JSON field value matches regex pattern."""
    data = _load_json(path)
    if data is None:
        return False
    val = _jq_get(data, jq)
    if val is None:
        return False
    return bool(re.search(pattern, str(val)))


def json_array_nonempty(path: str, jq: str) -> bool:
    """Verify JSON array at jq path exists and has length > 0."""
    data = _load_json(path)
    if data is None:
        return False
    val = _jq_get(data, jq)
    return isinstance(val, list) and len(val) > 0


def json_array_length(path: str, jq: str, min: int, max: int = None) -> bool:
    """Verify JSON array length is >= min and (if max set) <= max."""
    data = _load_json(path)
    if data is None:
        return False
    val = _jq_get(data, jq)
    if not isinstance(val, list):
        return False
    if len(val) < min:
        return False
    if max is not None and len(val) > max:
        return False
    return True


def json_array_all_have_keys(path: str, jq: str, keys: list) -> bool:
    """Verify every element in JSON array has all specified keys with non-null values."""
    data = _load_json(path)
    if data is None:
        return False
    arr = _jq_get(data, jq)
    if not isinstance(arr, list):
        return False
    if len(arr) == 0:
        return False
    for item in arr:
        if not isinstance(item, dict):
            return False
        for key in keys:
            if key not in item or item[key] is None:
                return False
    return True


# ═══════════════════════════════════════════════════════════
# Timestamp Checks
# ═══════════════════════════════════════════════════════════

def _resolve_glob(path: str) -> str | None:
    """Resolve glob to first matching path."""
    matches = globmod.glob(path, recursive=True)
    return matches[0] if matches else None


def timestamp_before(path_a: str, path_b: str) -> bool:
    """Verify file at path_a was last modified before file at path_b."""
    a = _resolve_glob(path_a)
    b = _resolve_glob(path_b)
    if not a or not b:
        return False
    try:
        return os.path.getmtime(a) < os.path.getmtime(b)
    except OSError:
        return False


def timestamp_after(path_a: str, path_b: str) -> bool:
    """Verify file at path_a was last modified after file at path_b."""
    a = _resolve_glob(path_a)
    b = _resolve_glob(path_b)
    if not a or not b:
        return False
    try:
        return os.path.getmtime(a) > os.path.getmtime(b)
    except OSError:
        return False


# ═══════════════════════════════════════════════════════════
# Tool Log Checks
# ═══════════════════════════════════════════════════════════

# Tool log path, set by runner
_tool_log_path: str | None = None


def set_tool_log_path(path: str) -> None:
    """Called by runner to set the tool log file location."""
    global _tool_log_path
    _tool_log_path = path


def _read_tool_log() -> list[dict]:
    """Read and parse the tool log file (JSONL format)."""
    if not _tool_log_path or not os.path.exists(_tool_log_path):
        return []
    entries = []
    try:
        with open(_tool_log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except OSError:
        return []
    return entries


def _log_search(entries: list[dict], pattern: str) -> list[dict]:
    """Return entries where any string value matches pattern."""
    results = []
    for entry in entries:
        flat = json.dumps(entry, ensure_ascii=False)
        if re.search(pattern, flat):
            results.append(entry)
    return results


def tool_log_contains(pattern: str) -> bool:
    """Verify tool log contains at least one call matching regex pattern."""
    entries = _read_tool_log()
    return len(_log_search(entries, pattern)) > 0


def tool_log_not_contains(pattern: str) -> bool:
    """Verify tool log contains NO call matching regex pattern."""
    entries = _read_tool_log()
    return len(_log_search(entries, pattern)) == 0


def _entry_tool(entry: dict) -> str:
    """Tool name of a log entry — supports legacy 'tool' and stream-json 'name'."""
    return entry.get("tool") or entry.get("name", "")


def _entry_args(entry: dict) -> dict:
    """Tool args of a log entry — supports legacy 'args' and stream-json 'input'."""
    return entry.get("args") if "args" in entry else entry.get("input", {})


def tool_log_read_before_write(reads: list, require_all: bool = True) -> bool:
    """Verify Read calls for specified files occurred before any Write/Edit call.
    If require_all=True, ALL listed file patterns must have been read first.
    Ordering uses log entry sequence (entries are written chronologically);
    the stream-json format has no timestamp field, so positions are compared."""
    entries = _read_tool_log()
    if not entries:
        return False

    # Position of the first Write/Edit call (chronological order = list order)
    first_write_idx = None
    for idx, entry in enumerate(entries):
        if _entry_tool(entry) in ("Write", "Edit"):
            first_write_idx = idx
            break

    # Check each required read
    matched = 0
    for read_pattern in reads:
        found = False
        for idx, entry in enumerate(entries):
            if _entry_tool(entry) != "Read":
                continue
            args_str = json.dumps(_entry_args(entry), ensure_ascii=False)
            if not re.search(read_pattern, args_str):
                continue
            if first_write_idx is None or idx < first_write_idx:
                found = True
                break
        if found:
            matched += 1

    if require_all:
        return matched == len(reads)
    return matched > 0


def tool_log_order(first: str, second: str) -> bool:
    """Verify a call matching 'first' occurs before a call matching 'second'."""
    entries = _read_tool_log()
    first_ts = None
    for entry in entries:
        flat = json.dumps(entry, ensure_ascii=False)
        if first_ts is None and re.search(first, flat):
            first_ts = entry.get("timestamp", 0)
        elif first_ts is not None and re.search(second, flat):
            return True
    return False


# ═══════════════════════════════════════════════════════════
# Output Checks
# ═══════════════════════════════════════════════════════════

_agent_output: str | None = None


def set_agent_output(text: str) -> None:
    """Called by runner to set the agent's full text output."""
    global _agent_output
    _agent_output = text


def _tool_results_text() -> str:
    """Concatenate all tool-call result strings (ground-truth outputs)."""
    entries = _read_tool_log()
    parts = []
    for e in entries:
        r = e.get("result")
        if r is None:
            r = e.get("output")
        if isinstance(r, str):
            parts.append(r)
        elif r:
            parts.append(json.dumps(r, ensure_ascii=False))
    return "\n".join(parts)


def output_contains(pattern: str) -> bool:
    """Verify agent text output OR tool results contain a match for regex pattern."""
    haystack = (_agent_output or "") + "\n" + _tool_results_text()
    return bool(re.search(pattern, haystack, re.MULTILINE))


def output_not_contains(pattern: str) -> bool:
    """Verify neither agent text output nor tool results contain the pattern."""
    haystack = (_agent_output or "") + "\n" + _tool_results_text()
    return not bool(re.search(pattern, haystack, re.MULTILINE))
