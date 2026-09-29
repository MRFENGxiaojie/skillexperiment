"""Dumper tests — cover basic round-trips and quoting of special
characters.

Not covered here (fuzz-worthy gaps, see APIs.txt):
- strings that look like aliases ("*foo") or merge keys ("<<")
- control characters / surrogates in strings
- non-string dict keys
- extremely deep nesting (recursion in _emit)
"""

import pytest

from yaml_utils.dumper import dumps
from yaml_utils.parser import parse


def test_dump_flat_mapping():
    text = dumps({"a": 1, "b": "x"})
    assert parse(text) == [{"a": "1", "b": "x"}]


def test_dump_nested():
    data = {"server": {"host": "10.0.0.1", "ports": [80, 443]}}
    text = dumps(data)
    assert parse(text) == [data]


def test_dump_empty_collections():
    assert dumps({}) == "{}\n"
    assert dumps({"a": [], "b": {}}) == "a: []\nb: {}\n"


def test_dump_quotes_colon_in_value():
    text = dumps({"msg": "hello: world"})
    assert 'msg: "hello: world"' in text


def test_dump_quotes_braces_in_value():
    text = dumps({"a": "[b]"})
    assert text == 'a: "[b]"\n'


def test_dump_none_bool():
    text = dumps({"a": None, "b": True, "c": False})
    assert parse(text) == [{"a": "null", "b": "true", "c": "false"}]
