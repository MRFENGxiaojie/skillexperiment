"""Legacy compatibility layer.

`load_compat` pre-processes legacy YamlUtils-0.2 documents (which used a
different directive syntax) with regexes before handing them to the real
parser. It is still invoked by two old data-import cron jobs and is the
part of the codebase nobody has audited yet.

Fuzz relevance: the regex pre-processing runs before parsing, so input
reaches this module first. See APIs.txt.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from .parser import YAMLError, parse

DIRECTIVE_RE = re.compile(r"^%\w+ (.*)$", re.MULTILINE)
MAPPER_RE = re.compile(r"^mapper (\S+) -> (\S+)$", re.MULTILINE)
CONTINUATION_RE = re.compile(r"\\\n( *)", re.MULTILINE)


def load_compat(text: str) -> Dict[str, Any]:
    """Parse a legacy document with 0.2-style directives.

    Steps:
      1. strip '%'-prefixed directive lines
      2. convert legacy mapper directives into '!!' tags
      3. join backslash continuations
      4. delegate to the standard parser (single document expected)
    """
    text = CONTINUATION_RE.sub(" ", text)
    directives: List[str] = []
    def _grab(match: "re.Match[str]") -> str:
        directives.append(match.group(0))
        return ""
    text = DIRECTIVE_RE.sub(_grab, text)
    for directive in directives:
        dm = MAPPER_RE.match(directive)
        if dm:
            text = text.replace(dm.group(1), "!!" + dm.group(2), 1)
    docs = parse(text)
    if not docs:
        return {}
    return docs[0]
