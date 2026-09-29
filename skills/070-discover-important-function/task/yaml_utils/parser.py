"""Recursive-descent parser for the YamlUtils YAML variant.

Input comes from external, untrusted sources (partner feeds, upload
endpoints, config mirrors), so every function in this module sits on the
fuzz-relevant attack surface. See APIs.txt for the prioritization.

Document structure:

    stream      := ( document ('---' | '...')? )*
    document    := mapping | sequence | scalar
    mapping     := ( key ':' value )+        (block)
                 | '{' pair (',' pair)* '}'  (flow)
    sequence    := ('-' value)*              (block)
                 | '[' value (',' value)* ']' (flow)
    key         := scalar | '?' scalar
    value       := scalar | mapping | sequence | alias | merge
    anchor      := '&' name
    alias       := '*' name
    merge       := '<<' ':' alias-or-mapping
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union


class YAMLError(Exception):
    """Base error for all parsing failures. Subclasses carry line/col."""


class ScannerError(YAMLError):
    def __init__(self, line: int, col: int, msg: str):
        self.line = line
        self.col = col
        super().__init__(f"line {line}, col {col}: {msg}")


class ParserError(YAMLError):
    def __init__(self, line: int, col: int, msg: str):
        self.line = line
        self.col = col
        super().__init__(f"line {line}, col {col}: {msg}")


class RecursionLimitError(YAMLError):
    """Raised when nesting or alias recursion exceeds the safety limit."""


MAX_DEPTH = 500
MAX_ALIAS_CHAIN = 500
MERGE_KEY = "<<"


@dataclass
class Mark:
    line: int
    col: int


@dataclass
class ScalarNode:
    value: str
    style: str = "plain"          # plain | single | double | literal | folded
    tag: Optional[str] = None
    mark: Optional[Mark] = None


@dataclass
class SequenceNode:
    items: List["Node"] = field(default_factory=list)
    flow: bool = False
    tag: Optional[str] = None
    mark: Optional[Mark] = None


@dataclass
class MappingNode:
    pairs: List[tuple["Node", "Node"]] = field(default_factory=list)
    flow: bool = False
    tag: Optional[str] = None
    mark: Optional[Mark] = None


@dataclass
class AliasNode:
    name: str
    mark: Optional[Mark] = None


Node = Union[ScalarNode, SequenceNode, MappingNode, AliasNode]


def parse(text: Union[str, bytes]) -> List[dict]:
    """Parse a (possibly multi-document) stream into python objects."""
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except UnicodeDecodeError as e:
            raise YAMLError(f"stream is not valid UTF-8: {e}") from e
    loader = _Loader(text)
    docs = []
    while loader.peek_document():
        node = loader.parse_document()
        docs.append(node_to_python(node, loader))
    return docs


def load(text: Union[str, bytes]) -> dict:
    """Parse a single-document stream; error if there is not exactly one."""
    docs = parse(text)
    if len(docs) != 1:
        raise YAMLError(f"expected exactly one document, found {len(docs)}")
    return docs[0]


def load_file(path: str) -> dict:
    with open(path, "rb") as fh:
        return load(fh.read())


class _Loader:
    """Tokenizes the stream on demand and drives the recursive descent."""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")
        self.line_idx = 0
        self.anchors: dict[str, Node] = {}
        self.alias_stack: List[str] = []

    # ── low-level helpers ──────────────────────────────────────────────

    def peek_document(self) -> bool:
        self._skip_blank_and_comments()
        line = self._current()
        if line is None:
            return False
        stripped = line.strip()
        while stripped in ("---", "...", ""):
            self.line_idx += 1
            self._skip_blank_and_comments()
            line = self._current()
            if line is None:
                return False
            stripped = line.strip()
        return True

    def _current(self) -> Optional[str]:
        if self.line_idx >= len(self.lines):
            return None
        return self.lines[self.line_idx]

    def _skip_blank_and_comments(self) -> None:
        while True:
            line = self._current()
            if line is None:
                return
            stripped = line.strip()
            if stripped == "" or stripped.startswith("#"):
                self.line_idx += 1
                continue
            break

    def _error(self, cls, msg) -> None:
        raise cls(self.line_idx + 1, 0, msg)

    @staticmethod
    def _indent_of(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    # ── document / node dispatch ──────────────────────────────────────

    def parse_document(self) -> Node:
        self._skip_blank_and_comments()
        line = self._current()
        if line is not None and line.strip() == "---":
            self.line_idx += 1
        node = self.parse_node(indent=0)
        self._skip_blank_and_comments()
        line = self._current()
        if line is not None and line.strip() == "...":
            self.line_idx += 1
        return node

    def parse_node(self, indent: int) -> Node:
        self._skip_blank_and_comments()
        line = self._current()
        if line is None:
            self._error(ParserError, "expected a node, found end of stream")
        stripped = line.lstrip(" ")
        actual_indent = len(line) - len(stripped)
        if actual_indent < indent:
            self._error(ParserError, "bad indentation")
        if stripped.startswith("-") and (len(stripped) == 1 or stripped[1] == " "):
            return self.parse_block_sequence(actual_indent)
        if ":" in stripped:
            return self.parse_block_mapping(actual_indent)
        if stripped.startswith("["):
            self.line_idx += 1
            return self._flow_seq_from_text(stripped)
        if stripped.startswith("{"):
            self.line_idx += 1
            return self._flow_map_from_text(stripped)
        return self.parse_scalar_node()

    # ── block mapping ─────────────────────────────────────────────────

    def parse_block_mapping(self, indent: int) -> MappingNode:
        node = MappingNode()
        while True:
            self._skip_blank_and_comments()
            line = self._current()
            if line is None:
                break
            stripped = line.lstrip(" ")
            actual = len(line) - len(stripped)
            if actual < indent:
                break
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("-") and (len(stripped) == 1 or stripped[1] == " "):
                break  # sibling sequence at same indent
            if stripped == "---" or stripped == "...":
                break
            key = self._parse_mapping_key(stripped)
            rest = self._rest_after_key(stripped)
            self.line_idx += 1
            if rest is None or rest == "":
                nxt = self._next_nonblank()
                if nxt is None:
                    value: Node = ScalarNode("")
                elif self._indent_of(nxt) > actual:
                    value = self.parse_node(actual)
                else:
                    value = ScalarNode("")
            elif rest.startswith("&") and len(rest.split()) == 1:
                # anchor declared on a following nested node
                anchor_name = rest[1:]
                nxt = self._next_nonblank()
                if nxt is not None and self._indent_of(nxt) > actual:
                    nested = self.parse_node(actual)
                else:
                    nested = ScalarNode("")
                self.anchors[anchor_name] = nested
                value = nested
            else:
                value = self._parse_inline_text(rest, actual)
            node.pairs.append((key, value))
        return node

    def _parse_mapping_key(self, stripped: str) -> Node:
        # Handle anchors/aliases/tags on the key, then find the ':'
        seg = stripped
        if seg.startswith("*"):
            return AliasNode(seg[1:].split()[0])
        if seg.startswith("!!"):
            tag = seg.split()[0]
            seg = seg[len(tag) :].lstrip()
        idx = seg.find(":")
        if idx == -1:
            self._error(ParserError, "no ':' in mapping key")
        raw_key = seg[:idx]
        if raw_key.startswith('"') or raw_key.startswith("'"):
            key = self._unquote(raw_key)
        else:
            key = raw_key.strip()
        return ScalarNode(key)

    def _rest_after_key(self, stripped: str) -> Optional[str]:
        idx = stripped.find(":")
        return stripped[idx + 1 :].strip() if idx != -1 else None

    # ── block sequence ────────────────────────────────────────────────

    def parse_block_sequence(self, indent: int) -> SequenceNode:
        node = SequenceNode()
        while True:
            self._skip_blank_and_comments()
            line = self._current()
            if line is None:
                break
            stripped = line.lstrip(" ")
            actual = len(line) - len(stripped)
            if actual < indent:
                break
            if not stripped.startswith("-") or (len(stripped) > 1 and stripped[1] != " "):
                break
            rest = stripped[1:].lstrip()
            self.line_idx += 1
            if rest:
                if ":" in rest:
                    node.items.append(self._parse_compact_mapping(rest, actual))
                else:
                    node.items.append(self._parse_inline_text(rest, actual))
            else:
                nxt = self._next_nonblank()
                if nxt is None:
                    node.items.append(ScalarNode(""))
                elif self._indent_of(nxt) > actual:
                    node.items.append(self.parse_node(actual))
                else:
                    node.items.append(ScalarNode(""))
        return node

    def _parse_compact_mapping(self, first_line: str, indent: int) -> MappingNode:
        """A sequence item that starts a mapping on the same line:
        '- name: alpha' followed by more indented key: value lines."""
        node = MappingNode()
        key = self._parse_mapping_key(first_line)
        rest = self._rest_after_key(first_line)
        if rest is None or rest == "":
            value: Node = ScalarNode("")
        else:
            value = self._parse_inline_text(rest, indent)
        node.pairs.append((key, value))
        # continue with following block lines at deeper indent
        self._skip_blank_and_comments()
        nxt = self._current()
        if nxt is not None and self._indent_of(nxt) > indent:
            more = self.parse_block_mapping(indent)
            node.pairs.extend(more.pairs)
        return node

    # ── inline (same-line) values ─────────────────────────────────────

    def _parse_inline_text(self, rest: str, header_indent: int) -> Node:
        if rest.startswith("|"):
            return self._parse_block_scalar("literal", rest, header_indent)
        if rest.startswith(">"):
            return self._parse_block_scalar("folded", rest, header_indent)
        if rest.startswith("["):
            return self._flow_seq_from_text(rest)
        if rest.startswith("{"):
            return self._flow_map_from_text(rest)
        if rest.startswith("&"):
            return self._parse_anchored_inline(rest, header_indent)
        if rest.startswith("*"):
            return AliasNode(rest[1:].split()[0])
        return self._scalar_from_rest(rest)

    def _parse_anchored_inline(self, rest: str, header_indent: int) -> Node:
        name = rest[1:].split()[0]
        inner = rest[len(name) + 1 :].strip()
        if inner.startswith("["):
            n = self._flow_seq_from_text(inner)
        elif inner.startswith("{"):
            n = self._flow_map_from_text(inner)
        elif inner.startswith("|") or inner.startswith(">"):
            n = self._parse_block_scalar("literal" if inner.startswith("|") else "folded", inner, header_indent)
        elif inner:
            n = self._scalar_from_rest(inner)
        else:
            n = ScalarNode("")
        self.anchors[name] = n
        return n

    # ── flow style (single-line) ──────────────────────────────────────

    def _flow_seq_from_text(self, text: str) -> SequenceNode:
        node = SequenceNode(flow=True)
        depth = 0
        items: List[Node] = []
        buf = ""
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "[":
                depth += 1
                if depth > 1:
                    buf += ch
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    if buf.strip():
                        items.append(self._flow_item(buf.strip()))
                    break
                buf += ch
            elif ch == "," and depth == 1:
                items.append(self._flow_item(buf.strip()))
                buf = ""
            else:
                buf += ch
            i += 1
        if depth != 0:
            self._error(ParserError, "unbalanced '[' in flow sequence")
        node.items = items
        return node

    def _flow_map_from_text(self, text: str) -> MappingNode:
        node = MappingNode(flow=True)
        depth = 0
        pairs: List[tuple[Node, Node]] = []
        buf = ""
        i = 0
        in_pair = False
        key: Optional[Node] = None
        while i < len(text):
            ch = text[i]
            if ch == "{":
                depth += 1
                if depth > 1:
                    buf += ch
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    if buf.strip() and not in_pair:
                        pairs.append((self._flow_item(buf.strip()), ScalarNode("")))
                    elif in_pair:
                        pairs.append((key, self._flow_item(buf.strip())))
                    break
                buf += ch
            elif ch == ":" and depth == 1 and not in_pair:
                key = self._flow_item(buf.strip())
                buf = ""
                in_pair = True
            elif ch == "," and depth == 1:
                if in_pair:
                    pairs.append((key, self._flow_item(buf.strip())))
                elif buf.strip():
                    pairs.append((self._flow_item(buf.strip()), ScalarNode("")))
                buf = ""
                in_pair = False
            else:
                buf += ch
            i += 1
        if depth != 0:
            self._error(ParserError, "unbalanced '{' in flow mapping")
        node.pairs = pairs
        return node

    def _flow_item(self, s: str) -> Node:
        if s.startswith("{"):
            return self._flow_map_from_text(s)
        if s.startswith("["):
            return self._flow_seq_from_text(s)
        if s.startswith("&"):
            return self._parse_anchored_inline(s, 0)
        if s.startswith("*"):
            return AliasNode(s[1:].strip())
        return ScalarNode(self._unquote(s))

    # ── scalars ───────────────────────────────────────────────────────

    def parse_scalar_node(self) -> ScalarNode:
        line = self._current()
        stripped = line.lstrip(" ")
        self.line_idx += 1
        return self._scalar_from_rest(stripped)

    def _scalar_from_rest(self, rest: str) -> ScalarNode:
        if rest.startswith("|"):
            return self._parse_block_scalar("literal", rest, 0)
        if rest.startswith(">"):
            return self._parse_block_scalar("folded", rest, 0)
        if rest.startswith('"'):
            return ScalarNode(self._unquote_double(rest), style="double")
        if rest.startswith("'"):
            return ScalarNode(self._unquote_single(rest), style="single")
        if rest.startswith("!!"):
            parts = rest.split()
            tag = parts[0]
            value = " ".join(parts[1:])
            if value.startswith('"'):
                value = self._unquote_double(value)
            return ScalarNode(value, tag=tag)
        # strip trailing comment
        value = rest
        hash_pos = value.find(" #")
        if hash_pos != -1:
            value = value[:hash_pos].rstrip()
        return ScalarNode(value.strip())

    def _parse_block_scalar(self, kind: str, header: str, header_indent: int) -> ScalarNode:
        """Block scalars ('|' literal, '>' folded). `header` is the text
        after the key (e.g. '|2-'), `header_indent` the indent of the
        header line. self.line_idx already points at the first content
        line when called from inline positions; when called from a
        line-start position the header line must be consumed by caller."""
        chomping = "clip"
        indent_hint: Optional[int] = None
        for ch in header[1:]:
            if ch in "+-":
                chomping = "keep" if ch == "+" else "strip"
            elif ch.isdigit():
                indent_hint = int(ch)
        lines: List[str] = []
        if indent_hint is not None:
            content_indent = header_indent + indent_hint
        else:
            # auto-detect: first non-blank content line's indent
            content_indent = header_indent + 1
            j = self.line_idx
            while j < len(self.lines):
                probe = self.lines[j].lstrip(" ")
                if probe:
                    content_indent = len(self.lines[j]) - len(probe)
                    break
                j += 1
        while True:
            nxt = self._current()
            if nxt is None:
                break
            nxt_stripped = nxt.lstrip(" ")
            if nxt_stripped == "":
                lines.append("")
                self.line_idx += 1
                continue
            nxt_indent = len(nxt) - len(nxt_stripped)
            if nxt_indent < content_indent:
                break
            lines.append(nxt[content_indent:])
            self.line_idx += 1
        if kind == "folded":
            body = " ".join(lines)
        else:
            body = "\n".join(lines)
        if chomping == "strip":
            body = body.rstrip("\n")
        elif chomping == "clip":
            body = body.rstrip("\n") + "\n"
        else:
            body = body + "\n\n"
        return ScalarNode(body, style=kind)

    # ── quoting / aliases / merge ─────────────────────────────────────

    def _unquote(self, s: str) -> str:
        if len(s) >= 2 and s[0] == '"':
            return self._unquote_double(s)
        if len(s) >= 2 and s[0] == "'":
            return self._unquote_single(s)
        return s

    def _unquote_double(self, s: str) -> str:
        if not s.startswith('"'):
            return s
        end = s.find('"', 1)
        if end == -1:
            self._error(ScannerError, "unterminated double-quoted scalar")
        body = s[1:end]
        out = []
        i = 0
        while i < len(body):
            ch = body[i]
            if ch == "\\" and i + 1 < len(body):
                nxt = body[i + 1]
                mapping = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "0": "\0"}
                if nxt in mapping:
                    out.append(mapping[nxt])
                else:
                    out.append(nxt)
                i += 2
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    def _unquote_single(self, s: str) -> str:
        if not s.startswith("'"):
            return s
        end = s.find("'", 1)
        if end == -1:
            self._error(ScannerError, "unterminated single-quoted scalar")
        return s[1:end].replace("''", "'")

    def _next_nonblank(self) -> Optional[str]:
        j = self.line_idx
        while j < len(self.lines):
            if self.lines[j].strip():
                return self.lines[j]
            j += 1
        return None


def _lookup_alias(loader: _Loader, name: str) -> Any:
    """Resolve an alias to the anchored python value.

    Cycle detection: if the same alias appears more than once on the
    resolution stack, the document is rejected.
    """
    if name in loader.alias_stack:
        raise RecursionLimitError(f"alias cycle detected at '&{name}'")
    node = loader.anchors.get(name)
    if node is None:
        raise ParserError(loader.line_idx + 1, 0, f"unknown anchor '&{name}'")
    loader.alias_stack.append(name)
    try:
        return node_to_python(node, loader)
    finally:
        loader.alias_stack.pop()


def _merge_mappings(target: dict, merge_value: Any, loader: _Loader) -> None:
    """Apply YAML merge-key semantics for a '<<' pair.

    Precedence: explicit keys of the mapping beat merged keys; among
    multiple merges, earlier merges win (first-wins).
    """
    if isinstance(merge_value, dict):
        sources = [merge_value]
    elif isinstance(merge_value, list):
        sources = merge_value
    else:
        raise ParserError(loader.line_idx + 1, 0, "merge value must be a mapping or sequence")
    for src in sources:
        if not isinstance(src, dict):
            raise ParserError(loader.line_idx + 1, 0, "merge source must be a mapping")
        for k, v in src.items():
            if k not in target:
                target[k] = v


def node_to_python(node: Node, loader: _Loader) -> Any:
    """Convert a node tree to plain python objects, resolving aliases and
    applying merge keys. The 'loader' argument is only used by aliases."""
    if isinstance(node, ScalarNode):
        return node.value
    if isinstance(node, AliasNode):
        return _lookup_alias(loader, node.name)
    if isinstance(node, SequenceNode):
        return [node_to_python(item, loader) for item in node.items]
    if isinstance(node, MappingNode):
        out: dict = {}
        for key_node, value_node in node.pairs:
            if isinstance(key_node, ScalarNode) and key_node.value == MERGE_KEY:
                merge_value = node_to_python(value_node, loader)
                _merge_mappings(out, merge_value, loader)
            else:
                key = node_to_python(key_node, loader)
                value = node_to_python(value_node, loader)
                out[key] = value
        return out
    raise ParserError(0, 0, f"cannot convert node {type(node).__name__}")
