"""yaml-utils: parsing/serialization for the YamlUtils YAML variant."""

from .parser import parse, load, load_file
from .dumper import dump, dumps
from .resolver import resolve_tags, parse_timestamp
from .validator import validate_schema, SchemaError
from .compat import load_compat

__version__ = "0.4.2"

__all__ = [
    "parse",
    "load",
    "load_file",
    "dump",
    "dumps",
    "resolve_tags",
    "parse_timestamp",
    "validate_schema",
    "SchemaError",
    "load_compat",
]
