"""Validator tests — cover basic type checks, required fields and
additional-property rejection.

Not covered here (fuzz-worthy gaps, see APIs.txt):
- schema recursion (schema referencing itself via 'items')
- pathological rule dicts (missing 'type', non-dict rules)
- unicode key collisions
"""

import pytest

from yaml_utils.validator import validate_schema, SchemaError


SCHEMA = {
    "name": {"type": "str", "required": True},
    "age": {"type": "int"},
    "tags": {"type": "list", "items": {"type": "str"}},
    "meta": {"type": "map", "values": {"type": "str"}},
}


def test_valid_document():
    data = {"name": "alice", "age": 30, "tags": ["a", "b"], "meta": {"k": "v"}}
    assert validate_schema(data, SCHEMA) is True


def test_missing_required_field():
    with pytest.raises(SchemaError):
        validate_schema({"age": 30}, SCHEMA)


def test_wrong_type():
    with pytest.raises(SchemaError):
        validate_schema({"name": "alice", "age": "not-int"}, SCHEMA)


def test_list_item_type():
    with pytest.raises(SchemaError):
        validate_schema({"name": "alice", "tags": [1, 2]}, SCHEMA)


def test_optional_field_absent_ok():
    assert validate_schema({"name": "bob"}, SCHEMA) is True


def test_additional_properties_rejected():
    schema = {"name": {"type": "str", "required": True}, "additional_properties": False}
    assert validate_schema({"name": "x"}, schema) is True
    with pytest.raises(SchemaError):
        validate_schema({"name": "x", "extra": 1}, schema)
