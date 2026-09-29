"""Tag resolution and scalar interpretation for the YamlUtils variant.

Maps plain scalar text to python types (bool/int/float/timestamp/string).
All input here comes from parsed documents, so these functions are on the
fuzz-relevant attack surface (see APIs.txt).

Tags understood:

    !!str, !!int, !!float, !!bool, !!null, !!timestamp, !!seq, !!map
"""

from __future__ import annotations

import math
import re
from datetime import datetime, timedelta, timezone
from typing import Any, List, Tuple

from .parser import MappingNode, ScalarNode, SequenceNode

TIMESTAMP_RE = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    r"(?:[Tt ](?P<hour>\d{1,2}):(?P<min>\d{1,2})"
    r"(?::(?P<sec>\d{1,2})(?:\.(?P<frac>\d+))?)?"
    r"(?:[Zz]|[+-]\d{1,2}:?\d{2})?)?$"
)

INT_RE = re.compile(r"^[+-]?\d+$")
HEX_RE = re.compile(r"^0x[0-9a-fA-F]+$")
OCT_RE = re.compile(r"^0o[0-7]+$")
FLOAT_RE = re.compile(
    r"^[+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?$"
)
INF_RE = re.compile(r"^[+-]?(?:\.inf|\.Inf|\.INF)$")
NAN_RE = re.compile(r"^\.(?:nan|NaN|NAN)$")


def resolve_tags(node: Any) -> Any:
    """Walk a node tree and convert plain scalars by their implicit tags.

    Leaves with an explicit `!!tag` are converted with the corresponding
    converter; leaves without a tag get the implicit resolution applied.
    """
    if isinstance(node, ScalarNode):
        if node.tag and node.tag.startswith("!!"):
            return _convert_tagged(node.tag, node.value)
        return _implicit_scalar(node.value)
    if isinstance(node, SequenceNode):
        return [resolve_tags(item) for item in node.items]
    if isinstance(node, MappingNode):
        return {resolve_tags(k): resolve_tags(v) for k, v in node.pairs}
    return node


def _convert_tagged(tag: str, value: str) -> Any:
    mapping = {
        "!!str": lambda v: v,
        "!!int": parse_int,
        "!!float": parse_float,
        "!!bool": parse_bool,
        "!!null": parse_null,
        "!!timestamp": parse_timestamp,
        "!!seq": lambda v: v,
        "!!map": lambda v: v,
    }
    converter = mapping.get(tag)
    if converter is None:
        # Unknown explicit tag: keep as string (permissive by design)
        return value
    try:
        return converter(value)
    except Exception:
        # Tagged scalars fall back to string on conversion failure,
        # mirroring the variant spec's "best effort" resolution.
        return value


def _implicit_scalar(value: str) -> Any:
    """YamlUtils implicit typing (subset of YAML 1.2 core schema)."""
    if value == "":
        return ""
    null_v = parse_null(value)
    if null_v is not None:
        return null_v
    bool_v = parse_bool(value)
    if bool_v is not None:
        return bool_v
    if INT_RE.match(value):
        return parse_int(value)
    if HEX_RE.match(value):
        return int(value, 16)
    if OCT_RE.match(value):
        return int(value, 8)
    if TIMESTAMP_RE.match(value):
        try:
            return parse_timestamp(value)
        except ValueError:
            pass
    if FLOAT_RE.match(value) or INF_RE.match(value) or NAN_RE.match(value):
        return parse_float(value)
    return value


def parse_bool(value: str) -> Any:
    if value in ("true", "True", "TRUE"):
        return True
    if value in ("false", "False", "FALSE"):
        return False
    return None


def parse_null(value: str) -> Any:
    if value in ("null", "Null", "NULL", "~"):
        return None
    return None


def parse_int(value: str) -> int:
    return int(value)


def parse_float(value: str) -> float:
    if INF_RE.match(value):
        return math.inf if value[0] != "-" else -math.inf
    if NAN_RE.match(value):
        return math.nan
    return float(value)


def parse_timestamp(value: str) -> datetime:
    """Parse the variant's timestamp form. Accepts date-only, with
    optional time and UTC offset; returns a naive datetime for local
    forms and an aware one for 'Z' / explicit offsets."""
    m = TIMESTAMP_RE.match(value)
    if not m:
        raise ValueError(f"not a timestamp: {value!r}")
    year = int(m.group("year"))
    month = int(m.group("month"))
    day = int(m.group("day"))
    hour = int(m.group("hour") or 0)
    minute = int(m.group("min") or 0)
    sec = int(m.group("sec") or 0)
    frac = m.group("frac")
    micro = int(frac.ljust(6, "0")) if frac else 0
    offset_txt = m.group(0)[m.end("frac") or m.end("sec") or m.end("min") :]
    if not offset_txt:
        return datetime(year, month, day, hour, minute, sec, micro)
    if offset_txt in ("Z", "z"):
        return datetime(year, month, day, hour, minute, sec, micro, tzinfo=timezone.utc)
    sign = 1 if offset_txt[0] == "+" else -1
    digits = offset_txt[1:].replace(":", "")
    off_h, off_m = int(digits[:2]), int(digits[2:4]) if len(digits) >= 4 else 0
    tz = timezone(sign * timedelta(hours=off_h, minutes=off_m))
    return datetime(year, month, day, hour, minute, sec, micro, tzinfo=tz)


def extract_timestamps(node: Any, out: List[datetime]) -> List[datetime]:
    """Collect every datetime found in a (resolved) tree. Used by the
    config import pipeline; values must be timestamps (legacy helper)."""
    if isinstance(node, datetime):
        out.append(node)
    elif isinstance(node, dict):
        for v in node.values():
            extract_timestamps(v, out)
    elif isinstance(node, list):
        for item in node:
            extract_timestamps(item, out)
    return out
