"""Schema validation for parsed YamlUtils documents.

Schemas are declarative dicts:

    {"name": {"type": "str", "required": True},
     "ports": {"type": "list", "items": {"type": "int"}},
     "meta":  {"type": "map", "values": {"type": "str"}}}

Types: str, int, float, bool, null, list, map, any.
"""

from __future__ import annotations

from typing import Any, Dict, List


class SchemaError(Exception):
    """Raised with a path string on the first validation failure."""


class SchemaValidator:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def validate(self, data: Any) -> bool:
        return self._validate_value(data, self.schema, path="$")

    def _validate_value(self, data: Any, rule: Any, path: str) -> bool:
        if not isinstance(rule, dict):
            raise SchemaError(f"{path}: malformed schema rule {rule!r}")
        t = rule.get("type", "any")
        if t == "map":
            if not isinstance(data, dict):
                raise SchemaError(f"{path}: expected map, got {type(data).__name__}")
            self._validate_map(data, rule, path)
        elif t == "list":
            if not isinstance(data, list):
                raise SchemaError(f"{path}: expected list, got {type(data).__name__}")
            item_rule = rule.get("items", {"type": "any"})
            for i, item in enumerate(data):
                self._validate_value(item, item_rule, f"{path}[{i}]")
        else:
            if not self._type_ok(data, t):
                raise SchemaError(f"{path}: expected {t}, got {repr(data)[:40]}")
        return True

    def _validate_map(self, data: Dict, rule: Any, path: str) -> None:
        fields = rule.get("fields")
        if fields is not None:
            for fname, frule in fields.items():
                if fname not in data:
                    if frule.get("required", False):
                        raise SchemaError(f"{path}.{fname}: missing required field")
                    continue
                self._validate_value(data[fname], frule, f"{path}.{fname}")
        allowed = rule.get("additional_properties")
        if allowed is False:
            known = set(fields) if fields else set()
            for key in data:
                if key not in known:
                    raise SchemaError(f"{path}: unexpected key {key!r}")
        values = rule.get("values")
        if values is not None:
            for k, v in data.items():
                self._validate_value(v, values, f"{path}.{k}")

    def _type_ok(self, data: Any, t: str) -> bool:
        if t == "any":
            return True
        if t == "str":
            return isinstance(data, str)
        if t == "int":
            return isinstance(data, int) and not isinstance(data, bool)
        if t == "float":
            return isinstance(data, (int, float)) and not isinstance(data, bool)
        if t == "bool":
            return isinstance(data, bool)
        if t == "null":
            return data is None
        return True


def validate_schema(data: Any, schema: Dict[str, Any]) -> bool:
    """Validate `data` against `schema`; raises SchemaError on failure."""
    return SchemaValidator(schema).validate(data)
