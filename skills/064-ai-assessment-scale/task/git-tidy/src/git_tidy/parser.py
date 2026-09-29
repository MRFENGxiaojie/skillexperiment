"""提交信息解析与校验逻辑。

校验规则基于 Conventional Commits 1.0.0 规范。
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

CONVENTIONAL_RE = re.compile(
    r"^(?P<type>[a-z]+)(\((?P<scope>[a-z0-9-]+)\))?"
    r"(!)?: (?P<subject>.+)$"
)


@dataclass
class ParsedCommit:
    type: str
    scope: Optional[str]
    breaking: bool
    subject: str
    body: str


@dataclass
class Violation:
    code: str
    message: str
    fix: Optional[str] = None


def parse(message: str) -> ParsedCommit:
    """解析单条提交信息，返回结构化结果。"""
    lines = message.strip().splitlines()
    header = lines[0] if lines else ""
    body = "\n".join(lines[1:]).strip()
    m = CONVENTIONAL_RE.match(header)
    if not m:
        raise ValueError(f"无法解析的提交信息头部: {header!r}")
    return ParsedCommit(
        type=m.group("type"),
        scope=m.group("scope"),
        breaking=bool(m.group("!") or "BREAKING CHANGE" in body),
        subject=m.group("subject"),
        body=body,
    )


def validate(message: str, allowed_types: List[str], max_line_length: int = 72) -> List[Violation]:
    """校验提交信息，返回违规列表（空列表表示通过）。"""
    violations: List[Violation] = []
    try:
        parsed = parse(message)
    except ValueError as exc:
        violations.append(Violation(code="E001", message=str(exc)))
        return violations

    if parsed.type not in allowed_types:
        violations.append(
            Violation(
                code="E002",
                message=f"类型 {parsed.type!r} 不在允许列表 {allowed_types} 中",
                fix=parsed.type if parsed.type else None,
            )
        )
    if parsed.scope and not parsed.scope.isalnum():
        violations.append(Violation(code="E003", message=f"scope 含非法字符: {parsed.scope!r}"))
    for line in message.splitlines():
        if len(line) > max_line_length:
            violations.append(
                Violation(
                    code="E004",
                    message=f"行长度 {len(line)} 超过 {max_line_length}",
                )
            )
    return violations
