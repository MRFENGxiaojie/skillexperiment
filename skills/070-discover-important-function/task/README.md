# yaml-utils

Parsing and serialization for the **YamlUtils YAML variant**, a superset of
plain YAML 1.2 used as the configuration/interchange format across several
internal services.

## Important note

Documents parsed by this library may come from **untrusted external sources**
(public upload endpoints, config mirrors, partner feeds). Anything in the
`parse_*` / `load_*` / `resolve_*` paths must therefore be treated as
security-sensitive input. A security review requested fuzzing; the fuzz
target prioritization is tracked in `APIs.txt` at the repository root.

## Installation

```bash
pip install -e .[dev]
```

## Usage

```python
from yaml_utils import parse, load_file, dump

docs = parse("a: 1\nb: [2, 3]\n")        # list of documents
data = load_file("config.yu")            # single-document helper
text = dump({"a": [1, 2], "b": {"c": 3}})
```

## Variant features

- Anchors (`&name`) / aliases (`*name`), with merge keys (`<<:`)
- Tags (`!!str`, `!internal/provider`)
- Block scalars (`|`, `>` with chomping indicators) and flow style `{}` / `[]`
- Multi-document streams (`---` / `...`)
- Comments, quoted and plain scalars

## Testing

```bash
pytest
```

See `docs/` for variant spec details.
