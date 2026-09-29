"""Parser tests — cover the common path: mappings, sequences, anchors,
aliases, comments, flow style and multi-document streams.

Not covered here (fuzz-worthy gaps, see APIs.txt):
- merge keys (`<<`) in any combination with aliases
- alias cycles / deep alias chains
- block scalar indentation edge cases (`|2`, `>+`, tab vs space)
- very deep nesting
"""

import pytest

from yaml_utils.parser import parse, load, RecursionLimitError, YAMLError


def test_parse_simple_mapping():
    docs = parse("a: 1\nb: two\n")
    assert docs == [{"a": "1", "b": "two"}]


def test_parse_nested_mapping_and_sequence():
    docs = parse("servers:\n  - name: alpha\n    port: 8080\n  - name: beta\n")
    assert docs == [{"servers": [{"name": "alpha", "port": "8080"}, {"name": "beta"}]}]


def test_parse_flow_style():
    docs = parse("a: {x: 1, y: 2}\nb: [1, 2, 3]\n")
    assert docs == [{"a": {"x": "1", "y": "2"}, "b": ["1", "2", "3"]}]


def test_parse_anchors_and_aliases():
    text = "base: &b {k: v}\ncopy: *b\n"
    assert parse(text) == [{"base": {"k": "v"}, "copy": {"k": "v"}}]


def test_parse_comments_ignored():
    docs = parse("# top comment\na: 1 # trailing\n# another\nb: 2\n")
    assert docs == [{"a": "1", "b": "2"}]


def test_parse_multiple_documents():
    docs = parse("a: 1\n---\nb: 2\n...\n---\nc: 3\n")
    assert docs == [{"a": "1"}, {"b": "2"}, {"c": "3"}]


def test_parse_block_scalar_literal():
    docs = parse("msg: |\n  hello\n  world\n")
    assert docs == [{"msg": "hello\nworld\n"}]


def test_parse_quoted_scalars():
    docs = parse('a: "hello: world"\nb: \'it\'\'s fine\'\n')
    assert docs == [{"a": "hello: world", "b": "it's fine"}]


def test_load_single_document():
    assert load("a: 1\n") == {"a": "1"}


def test_load_rejects_multiple_documents():
    with pytest.raises(YAMLError):
        load("a: 1\n---\nb: 2\n")


def test_parse_unknown_alias_raises():
    with pytest.raises(YAMLError):
        parse("a: *nope\n")


def test_parse_unbalanced_bracket_raises():
    with pytest.raises(YAMLError):
        parse("a: [1, 2\n")


def test_parse_empty_stream():
    assert parse("") == []
    assert parse("# only a comment\n") == []
