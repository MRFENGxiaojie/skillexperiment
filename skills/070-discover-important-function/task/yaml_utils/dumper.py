"""Serializer for the YamlUtils variant.

The dumper is not usually fed untrusted input, but it IS fed *untrusted
strings* from parsed documents during config regeneration, so quoting and
escaping behavior is still fuzz-relevant (see APIs.txt).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

INDENT = 2

PLAIN_UNSAFE = set(":{}[],&*#?|-<>=!%@`\"'\\\n\t")


def dumps(data: Any) -> str:
    """Serialize a python object to a single YamlUtils document."""
    lines: List[str] = []
    _emit(data, 0, lines)
    return "\n".join(lines) + ("\n" if lines else "")


def dump(data: Any) -> str:
    return dumps(data)


def _emit(data: Any, level: int, lines: List[str]) -> None:
    if isinstance(data, dict):
        if not data:
            lines.append(_pad(level) + "{}")
            return
        for k, v in data.items():
            key = _quote_if_needed(str(k))
            if isinstance(v, (dict, list)) and v is not None and (v if not isinstance(v, (str, bytes)) else True):
                if isinstance(v, dict) and not v:
                    lines.append(_pad(level) + f"{key}: {{}}")
                elif isinstance(v, list) and not v:
                    lines.append(_pad(level) + f"{key}: []")
                else:
                    lines.append(_pad(level) + f"{key}:")
                    _emit(v, level + 1, lines)
            else:
                lines.append(_pad(level) + f"{key}: {_emit_inline(v)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item:
                lines.append(_pad(level) + "-")
                _emit(item, level + 1, lines)
            elif isinstance(item, list):
                lines.append(_pad(level) + "-")
                _emit(item, level + 1, lines)
            else:
                lines.append(_pad(level) + f"- {_emit_inline(item)}")
    else:
        lines.append(_pad(level) + _emit_inline(data))


def _emit_inline(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):
        inner = ", ".join(f"{_quote_if_needed(str(k))}: {_emit_inline(v)}" for k, v in value.items())
        return "{" + inner + "}"
    if isinstance(value, list):
        return "[" + ", ".join(_emit_inline(v) for v in value) + "]"
    return _quote_if_needed(str(value))


def _quote_if_needed(text: str) -> str:
    """Quote a string if it contains characters that would change meaning
    if emitted as a plain scalar. Double quotes are escaped; newlines are
    emitted as \n. NB: this check is intentionally cheap — it does not
    inspect for alias-looking or timestamp-looking tokens."""
    needs_quote = any(ch in PLAIN_UNSAFE for ch in text)
    if not needs_quote:
        return text
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def _pad(level: int) -> str:
    return " " * (level * INDENT)
