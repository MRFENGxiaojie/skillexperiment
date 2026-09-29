"""git-tidy 命令行入口。"""
from __future__ import annotations

import argparse
import subprocess
import sys

from .parser import validate


def _read_latest_message() -> str:
    """读取最近一次提交信息（用于 check 命令）。"""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%B"], capture_output=True, text=True, check=True
    )
    return out.stdout


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="git-tidy")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="校验最近一次提交信息")
    sub.add_parser("fix", help="尝试自动修复格式问题")
    sub.add_parser("install-hook", help="安装 pre-commit hook")

    args = parser.parse_args(argv)

    if args.command == "check":
        message = _read_latest_message()
        violations = validate(message, ["feat", "fix", "docs", "chore", "refactor", "test"])
        if violations:
            for v in violations:
                print(f"[{v.code}] {v.message}", file=sys.stderr)
            return 1
        print("OK: 提交信息符合规范")
        return 0

    if args.command == "fix":
        # 简化实现：仅提示手工修复建议
        message = _read_latest_message()
        violations = validate(message, ["feat", "fix", "docs", "chore", "refactor", "test"])
        for v in violations:
            if v.fix:
                print(f"建议将类型改为 {v.fix}")
        return 0 if not violations else 1

    if args.command == "install-hook":
        hook = (
            "#!/bin/sh\n"
            "exec git-tidy check\n"
        )
        with open(".git/hooks/pre-commit", "w", encoding="utf-8") as f:
            f.write(hook)
        print("pre-commit hook 已安装")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
