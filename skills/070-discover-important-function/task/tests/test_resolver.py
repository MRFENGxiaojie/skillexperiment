"""Resolver tests — cover implicit typing for bool/null/int/float and
timestamps.

Not covered here (fuzz-worthy gaps, see APIs.txt):
- weird number forms (very large exponents, hex/octal mixed, "+" signs)
- timestamp offset edge cases (e.g. "+9999", missing minutes, frac padding)
- tag conversion fallbacks (unknown !! tags, tagged values that fail)
"""

import math

from datetime import datetime, timezone

from yaml_utils.parser import parse, ScalarNode
from yaml_utils.resolver import resolve_tags, parse_timestamp, extract_timestamps


def test_implicit_bool_and_null():
    docs = parse("a: true\nb: false\nc: null\nd: ~\n")
    resolved = [resolve_tags(d) for d in docs]
    assert resolved == [{"a": True, "b": False, "c": None, "d": None}]


def test_implicit_ints():
    docs = parse("a: 42\nb: -7\nc: 0x1F\nd: 0o17\n")
    resolved = [resolve_tags(d) for d in docs]
    assert resolved == [{"a": 42, "b": -7, "c": 31, "d": 15}]


def test_implicit_floats():
    docs = parse("a: 3.14\nb: -0.5\nc: 1e3\nd: .inf\n")
    resolved = [resolve_tags(d) for d in docs]
    assert resolved[0]["a"] == 3.14
    assert resolved[0]["b"] == -0.5
    assert resolved[0]["c"] == 1000.0
    assert math.isinf(resolved[0]["d"])


def test_implicit_timestamp():
    docs = parse("a: 2026-01-02\nts: 2026-01-02T15:04:05Z\n")
    resolved = [resolve_tags(d) for d in docs][0]
    assert resolved["a"] == datetime(2026, 1, 2)
    assert resolved["ts"] == datetime(2026, 1, 2, 15, 4, 5, tzinfo=timezone.utc)


def test_parse_timestamp_with_offset():
    dt = parse_timestamp("2026-06-01 10:30:00+08:00")
    assert dt.tzinfo is not None
    assert dt.utcoffset().total_seconds() == 8 * 3600


def test_parse_timestamp_invalid():
    with pytest.raises(ValueError):
        parse_timestamp("not-a-date")


def test_quoted_scalars_stay_strings():
    docs = parse('a: "42"\nb: "true"\n')
    resolved = [resolve_tags(d) for d in docs]
    assert resolved == [{"a": "42", "b": "true"}]


def test_explicit_tags():
    node = ScalarNode("42", tag="!!int")
    assert resolve_tags(node) == 42


def test_extract_timestamps_collects_all():
    tree = {"x": datetime(2026, 1, 1), "y": {"z": [datetime(2026, 2, 1), "nope"]}}
    found = extract_timestamps(tree, [])
    assert len(found) == 2
