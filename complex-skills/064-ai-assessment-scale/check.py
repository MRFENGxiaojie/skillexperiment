"""064-ai-assessment-scale — professional evaluation checks (self-contained).
Runner: python check.py <workspace> <tool_log> <agent_output>
Prints JSON: {"<id>.s": true/false, ...}   (combo script parts; judge.py merges the llm part)
Constraints: 40   (37 with mechanical hooks, 3 llm-only)
"""
import json
import os
import re
import sys
import glob

_META = re.compile(r"[\.\*\[\]\^\$\(\)\\|]")


_WS = re.compile(r"\s+")


_WS = re.compile(r"\s+")


def _match(txt: str, needle) -> bool:
    """needle may be a regex (contains meta chars) or a literal; try literal alternatives first (whitespace-insensitive), then regex."""
    if not needle:
        return False
    txt_n = _WS.sub(" ", txt)
    needle_n = _WS.sub(" ", needle.strip())
    if not needle_n:
        return False
    lower_txt = txt_n.lower()
    for part in needle_n.split("|"):
        if part and part.lower() in lower_txt:
            return True
    if _META.search(needle_n):
        try:
            return re.search(needle_n, txt_n, re.I) is not None
        except re.error:
            return False
    return False

def _read(p) -> str:
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def _candidates(ws, path: str) -> list:
    """路径候选根：兼容 workspace 保留/剥离 task/ 前缀两种布局；~ 展开为用户主目录。"""
    p = path.replace("\\", "/")
    if p.startswith("~"):
        return [os.path.expanduser(p)]
    if p.startswith("task/"):
        rest = p[len("task/"):]
        return [os.path.join(ws, p), os.path.join(ws, rest)]
    return [os.path.join(ws, p), os.path.join(ws, "task", p)]


def _fuzzy_matches(ws, path: str) -> list:
    """Fuzzy fallback for filename variants (extra suffix/prefix tokens or the same
    token set in a different order), e.g. privilege-log-review-2026-08-24.md for
    privilege-log-review.md, alvarez-jose.md for jose-alvarez.md."""
    out = []
    seen = set()
    p = path.replace("\\", "/")
    if p.startswith("~"):
        return out
    base = os.path.basename(p)
    if glob.has_magic(base):
        return out
    stem, ext = os.path.splitext(base)
    if not stem:
        return out
    for cand in _candidates(ws, path):
        if glob.has_magic(cand):
            dpart, _b = os.path.split(cand)
            for fp in sorted(glob.glob(os.path.join(dpart, stem + "*" + ext), recursive=True, include_hidden=True)):
                if fp not in seen:
                    seen.add(fp)
                    out.append(fp)
        else:
            dpart = os.path.dirname(cand)
            for fp in sorted(glob.glob(os.path.join(dpart, stem + "*" + ext), recursive=True, include_hidden=True)):
                if fp not in seen:
                    seen.add(fp)
                    out.append(fp)
            if os.path.isdir(dpart):
                toks = set(re.split(r"[_\-\s.]+", stem.lower()))
                try:
                    names = sorted(os.listdir(dpart))
                except OSError:
                    names = []
                for fn in names:
                    fstem, fext = os.path.splitext(fn)
                    if fext.lower() != ext.lower():
                        continue
                    ftoks = set(re.split(r"[_\-\s.]+", fstem.lower()))
                    if ftoks and ftoks == toks:
                        fp = os.path.join(dpart, fn)
                        if fp not in seen:
                            seen.add(fp)
                            out.append(fp)
    return out


def _resolve(ws, path: str) -> str:
    """Return the first existing candidate (glob first match); fuzzy fallback, else the first literal candidate."""
    for cand in _candidates(ws, path):
        if glob.has_magic(cand):
            ms = sorted(glob.glob(cand, recursive=True, include_hidden=True))
            if ms:
                return ms[0]
        elif os.path.exists(cand):
            return cand
    fz = _fuzzy_matches(ws, path)
    if fz:
        return fz[0]
    return _candidates(ws, path)[0]


def _resolve_all(ws, path: str) -> list:
    """Return all existing candidates / glob matches; fuzzy fallback; else the first literal candidate."""
    out = []
    for cand in _candidates(ws, path):
        if glob.has_magic(cand):
            out += sorted(glob.glob(cand, recursive=True, include_hidden=True))
        elif os.path.exists(cand):
            out.append(cand)
    if out:
        return out
    fz = _fuzzy_matches(ws, path)
    if fz:
        return fz
    return _candidates(ws, path)[:1]


def _written_paths(ws, entries) -> list:
    """Map agent-written file paths from the tool log into the result workspace."""
    out = []
    for e in entries:
        if str(e.get("name") or "") not in ("Write", "Edit", "MultiEdit", "ApplyPatch", "NotebookEdit"):
            continue
        fp = str((e.get("input") or {}).get("file_path") or (e.get("input") or {}).get("path") or "")
        if not fp:
            continue
        fp = fp.replace("\\", "/")
        low = fp.lower()
        if re.match(r"^[a-z]:/users/", low) and "/.claude/projects/" in low:
            continue
        m = re.search(r"/workspaces/[^/]+/(.+)$", fp, re.I)
        if m:
            rel = m.group(1)
        else:
            try:
                rel = os.path.relpath(fp, ws)
                if rel.startswith(".."):
                    continue
            except ValueError:
                continue
        p = os.path.join(ws, rel.replace("/", os.sep))
        if os.path.isfile(p) and p not in out:
            out.append(p)
    # Agent-written files may come from Bash/PowerShell instead of Write/Edit
    # (codex backend never uses the Write tool). Detect them by mtime: files
    # modified at/after run start (mtime of the task_forced file) are agent
    # artifacts; provided materials keep their template mtime and are excluded.
    run_start = None
    try:
        for fn in os.listdir(ws):
            if fn.startswith("task_forced") and fn.endswith(".txt"):
                run_start = os.path.getmtime(os.path.join(ws, fn))
                break
    except OSError:
        run_start = None
    if run_start is not None:
        for root, dirs, files in os.walk(ws):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "task"]
            for fn in files:
                fp = os.path.join(root, fn)
                if fn.startswith("task_forced"):
                    continue
                try:
                    if os.path.getmtime(fp) >= run_start and fp not in out:
                        out.append(fp)
                except OSError:
                    continue
    return out


def _entry_text(e: dict) -> str:
    return (str(e.get("name") or "") + " " + json.dumps(e.get("input") or {}, ensure_ascii=False)).replace("\\\\", "/")


def _tool_text(entries) -> str:
    return "\n".join(_entry_text(e) for e in entries)


def _load_tool_log(path: str) -> list:
    entries = []
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read().strip()
    except OSError:
        return entries
    if not txt:
        return entries
    try:
        arr = json.loads(txt)
        if isinstance(arr, list):
            return [e for e in arr if isinstance(e, dict)]
    except json.JSONDecodeError:
        pass
    for line in txt.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
            if isinstance(e, dict):
                entries.append(e)
        except json.JSONDecodeError:
            pass
    return entries


def _nested_get(data, field: str):
    cur = data
    for part in field.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _file_exists(ws, path) -> bool:
    return any(os.path.isfile(p) for p in _resolve_all(ws, path))


def _file_not_exists(ws, path) -> bool:
    return not os.path.exists(_resolve(ws, path))


def _file_nonempty(ws, path) -> bool:
    for p in _resolve_all(ws, path):
        try:
            if os.path.isfile(p) and os.path.getsize(p) > 0:
                return True
        except OSError:
            pass
    return False


def _file_contains(ws, path, needle) -> bool:
    return any(_match(_read(p), needle) for p in _resolve_all(ws, path))


def _output_contains(out, needle) -> bool:
    return _match(out, needle)


def _tool_contains(entries, cmd) -> bool:
    return any(_match(_entry_text(e), cmd) for e in entries)


def _tool_order(entries, cmds) -> bool:
    pos = {}
    for e in entries:
        txt = _entry_text(e)
        for c in cmds:
            if _match(txt, c) and c not in pos:
                pos[c] = len(pos)
    return all(c in pos for c in cmds) and all(pos[a] < pos[b] for a, b in zip(cmds, cmds[1:]))


_ERR_RE = re.compile(r"\b(?:traceback|error|exception|failed|failure|fail|nonzero|"
                     r"command\s+not\s+found|no\s+such\s+file|cannot|killed)\b", re.I)


def _command_succeeded(entries, cmd, expect) -> bool:
    hits = [e for e in entries if cmd in _entry_text(e)]
    if not hits:
        return False
    if expect == "fail":
        for h in hits:
            res = str(h.get("result") or "")
            if not res.strip() or _ERR_RE.search(res):
                return True
        return False
    return all(not _ERR_RE.search(str(h.get("result") or "")) for h in hits)


def _numeric_threshold(ws, out, src, key, op, n) -> bool:
    if src == "output":
        txt = out
    elif src.startswith("file:"):
        p = src[5:]
        base = re.sub(r"\$\{[^}]+\}", "*", p)
        if "${" in p or glob.has_magic(base):
            ms = []
            for cand in _candidates(ws, base):
                ms += sorted(glob.glob(cand, recursive=True))
            if not ms:
                return False
            txt = "\n".join(_read(m) for m in dict.fromkeys(ms))
        else:
            txt = _read(_resolve(ws, p))
    else:
        txt = out
    try:
        m = re.search(key, txt)
    except re.error:
        return False
    if not m:
        return False
    raw = m.group(1) if m.lastindex else m.group(0)
    nums = re.findall(r"-?\d+(?:\.\d+)?", str(raw))
    if not nums:
        return False
    try:
        val = float(nums[0])
    except ValueError:
        return False
    if op == "ge":
        return val >= n
    if op == "gt":
        return val > n
    if op == "le":
        return val <= n
    if op == "lt":
        return val < n
    if op == "eq":
        return val == n
    return False


_FILE_EXT = (".md", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js", ".jsx", ".py",
             ".txt", ".html", ".htm", ".csv", ".jsonl")


def _count(ws, entries, what, op, n) -> bool:
    if glob.has_magic(what) or "/" in what or what.endswith(_FILE_EXT) or what.endswith("*"):
        cnt = 0
        for cand in _candidates(ws, what):
            cnt += len(glob.glob(cand, recursive=True))
    else:
        cnt = sum(1 for e in entries if what in _entry_text(e))
    if op == "ge":
        return cnt >= n
    if op == "gt":
        return cnt > n
    if op == "eq":
        return cnt == n
    return False


def _json_schema(ws, path, fields) -> bool:
    try:
        data = json.loads(_read(_resolve(ws, path)))
    except Exception:
        return False
    return all(_nested_get(data, f) is not None for f in fields)


def _yaml_config(ws, path, fields) -> bool:
    try:
        import yaml as _yaml
    except ImportError:
        return bool(fields) and all(_file_contains(ws, path, f) for f in fields)
    try:
        data = _yaml.safe_load(_read(_resolve(ws, path)))
    except Exception:
        return False
    if not isinstance(data, dict):
        return False
    return all(_nested_get(data, f) is not None for f in fields)


def _html_structure(ws, path, tags) -> bool:
    return all(t in _read(_resolve(ws, path)) for t in tags)


def _section_nonempty(ws, path, headers, min_chars) -> bool:
    for p in _resolve_all(ws, path):
        lines = _read(p).splitlines()
        ok = True
        for h in headers:
            idx = None
            for i, ln in enumerate(lines):
                if any(a.lower() in ln.lower() for a in [x.strip() for x in h.split("|")] if a):
                    idx = i
                    break
            if idx is None:
                ok = False
                break
            m = re.match(r"^\s*(#+)\s*", lines[idx])
            lvl = len(m.group(1)) if m else 0
            chars = 0
            for ln in lines[idx + 1:]:
                s = ln.strip()
                if s.startswith("#"):
                    nm = re.match(r"#+", s)
                    if lvl == 0 or (nm and len(nm.group(0)) <= lvl):
                        break
                chars += len(s)
                if chars >= min_chars:
                    break
            if chars < min_chars:
                ok = False
                break
        if ok:
            return True
    return False


def _api_call_check(ws, path, api, require_args) -> bool:
    txt = _read(_resolve(ws, path))
    if api not in txt:
        return False
    for line in txt.splitlines():
        if api in line and all(a in line for a in require_args):
            return True
    return False


def _json_field_matches(ws, path, jq, pattern) -> bool:
    try:
        data = json.loads(_read(_resolve(ws, path)))
    except Exception:
        return False
    val = data
    for part in jq.lstrip(".").split("."):
        part = part.strip()
        if not part:
            continue
        if part.endswith("]"):
            key, _, inds = part.rpartition("[")
            try:
                ind = int(inds[:-1])
            except ValueError:
                return False
            val = val.get(key) if isinstance(val, dict) else None
            if not isinstance(val, list) or ind >= len(val):
                return False
            val = val[ind]
        else:
            val = val.get(part) if isinstance(val, dict) else None
            if val is None:
                return False
    try:
        return re.search(pattern, str(val)) is not None
    except re.error:
        return pattern in str(val)


def _check(ws, entries, out, hook: dict) -> bool:
    kind = hook["kind"]
    if kind == "file_exists":
        return _file_exists(ws, hook["path"])
    if kind == "file_not_exists":
        return _file_not_exists(ws, hook["path"])
    if kind == "file_nonempty":
        return _file_nonempty(ws, hook["path"])
    if kind == "file_contains":
        return _file_contains(ws, hook["path"], hook.get("needle") or "")
    if kind == "output_contains":
        nd = hook.get("needle") or ""
        if _output_contains(out, nd):
            return True
        for _fp in _written_paths(ws, entries):
            if _match(_read(_fp), nd):
                return True
        return False
    if kind == "output_not_contains":
        return not _output_contains(out, hook.get("needle") or "")
    if kind == "tool_log_contains":
        return _tool_contains(entries, hook.get("cmd") or hook.get("needle") or "")
    if kind == "tool_log_not_contains":
        pat = hook.get("cmd") or hook.get("pattern") or ""
        if pat and _META.search(pat):
            try:
                return not re.search(pat, _tool_text(entries), re.I)
            except re.error:
                return pat not in _tool_text(entries)
        return pat not in _tool_text(entries)
    if kind == "tool_log_order":
        return _tool_order(entries, hook.get("cmds") or [])
    if kind == "command_succeeded":
        return _command_succeeded(entries, hook.get("cmd") or "", hook.get("expect") or "success")
    if kind == "numeric_threshold":
        return _numeric_threshold(ws, out, hook.get("in") or "output", hook.get("key") or "",
                                  hook.get("op"), hook.get("n"))
    if kind == "count":
        return _count(ws, entries, hook.get("what") or "", hook.get("op"), hook.get("n"))
    if kind == "json_schema":
        return _json_schema(ws, hook["path"], hook.get("require_fields") or [])
    if kind == "yaml_config":
        return _yaml_config(ws, hook["path"], hook.get("require_fields") or [])
    if kind == "html_structure":
        return _html_structure(ws, hook["path"], hook.get("require_tags") or [])
    if kind == "section_nonempty":
        return _section_nonempty(ws, hook["path"], hook.get("headers") or [], hook.get("min_chars") or 20)
    if kind == "api_call_check":
        return _api_call_check(ws, hook["path"], hook.get("api") or "", hook.get("require_args") or [])
    if kind == "json_field_matches":
        return _json_field_matches(ws, hook["path"], hook.get("jq") or ".", hook.get("pattern") or "")
    return False


def main():
    if len(sys.argv) < 4:
        print("usage: check.py <workspace> <tool_log> <agent_output>", file=sys.stderr)
        sys.exit(2)
    ws, tool_log_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    entries = _load_tool_log(tool_log_path)
    out = ""
    try:
        with open(out_path, encoding="utf-8", errors="replace") as f:
            out = f.read()
    except OSError:
        pass
    res = {}
    res["C01.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "# AI Assessment Scale (AIAS) Evaluation Report|# AI Usage Disclosure"})
    res["C02.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "git-tidy"})
    res["C03.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Cursor"})
    res["C04.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Copilot"})
    res["C05.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "2\\.0|v2"})
    res["C06.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "project_description"})
    res["C07.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "README.md"})
    res["C08.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "AI-USAGE.md"})
    res["C09.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "git_tidy/parser.py"})
    res["C10.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "git_tidy/cli.py"})
    res["C11.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "tests/"})
    res["C12.s"] = _check(ws, entries, out, {"kind": "command_succeeded", "cmd": "git log", "expect": "success"})
    res["C13.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "80%"})
    res["C14.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Planning & Architecture|Architecture design"})
    res["C15.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Implementation"})
    res["C16.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Testing & Quality Assurance|### Testing"})
    res["C17.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Documentation"})
    res["C18.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Level 2"})
    res["C19.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Level 4"})
    res["C20.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Level 3"})
    res["C21.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Collaboration"})
    res["C22.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Evidence"})
    res["C23.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Human Critical Evaluation|Human contribution and accountability"})
    res["C24.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Rationale"})
    res["C25.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Executive Summary|## Summary"})
    res["C26.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Partially Disclosed"})
    res["C27.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "AI Transparency|AI usage transparency"})
    res["C28.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "img.shields.io"})
    res["C29.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "AI%20Contribution"})
    res["C30.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "lightgrey"})
    res["C31.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Recommendations|Recommended|Suggested README"})
    res["C32.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Missing|not yet tracked|had no badge"})
    res["C33.s"] = _check(ws, entries, out, {"kind": "output_contains", "needle": "Key Takeaways"})
    res["C34.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "descriptive"})
    res["C37.s"] = _check(ws, entries, out, {"kind": "tool_log_contains", "cmd": "git_tidy"})
    res["C38.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "AI-USAGE.md"})
    res["C40.s"] = _check(ws, entries, out, {"kind": "file_contains", "path": "git-tidy/AI-USAGE.md", "needle": "Commit history|Commit-history"})
    print(json.dumps(res, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
