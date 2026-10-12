"""runner_core.py -- shared mechanics for the retrigger runner."""
import json
import os
import queue
import random
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

PROJECT = Path(os.environ.get("BENCH_PROJECT") or Path(__file__).parent)
COMPLEX_SKILLS = PROJECT / "complex-skills"
RESULTS = PROJECT / "results" / "runs"
WORKSPACES = PROJECT / "workspaces"

def find_skills():
    skills = []
    for d in sorted(COMPLEX_SKILLS.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
            continue
        task_file = d / "task" / "task.txt"
        if task_file.exists():
            skills.append(d)
    return skills

def prepare_workspace(skill_dir):
    task_dir = skill_dir / "task"
    ts = str(int(time.time() * 1000))[-8:]
    ws = WORKSPACES / f"{skill_dir.name}-{ts}"
    ws.mkdir(parents=True, exist_ok=True)

    for f in task_dir.iterdir():
        if f.name == "task.txt":
            continue
        if f.is_dir():
            shutil.copytree(f, ws / f.name)
        else:
            shutil.copy2(f, ws / f.name)

    return ws

CLAUDE_CMD = os.environ.get("CLAUDE_CMD") or shutil.which("claude")
CODEX_CMD = os.environ.get("CODEX_CMD") or shutil.which("codex")

EXEC_BACKEND = "claude"

def _ensure_git_bash():
    if os.environ.get("CLAUDE_CODE_GIT_BASH_PATH"):
        return
    w = shutil.which("bash")
    if w:
        os.environ["CLAUDE_CODE_GIT_BASH_PATH"] = w

def _codex_default_model():
    try:
        cfg = Path(os.path.expanduser("~")) / ".codex" / "config.toml"
        if cfg.exists():
            for line in cfg.read_text(encoding="utf-8").splitlines():
                m = re.match(r'^\s*model\s*=\s*"([^"]+)"', line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return "codex-cli"

def codex_to_claude(lines, model):
    if model is None:
        model = _codex_default_model()
    out = []
    if model:
        out.append(json.dumps({"type": "stream_event",
                               "event": {"type": "message_start", "message": {"model": model}}}))
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "item.completed":
            continue
        item = ev.get("item") or {}
        itype = item.get("type")
        if itype == "agent_message":
            txt = item.get("text") or ""
            if not txt and isinstance(item.get("content"), str):
                txt = item["content"]
            if txt:
                out.append(json.dumps({"type": "stream_event",
                                       "event": {"type": "content_block_delta",
                                                 "delta": {"type": "text_delta", "text": txt}}}))
        elif itype == "command_execution":
            tid = item.get("id") or "tool_0"
            cmd = item.get("command") or ""
            out.append(json.dumps({"type": "assistant",
                                   "message": {"content": [{"type": "tool_use", "id": tid,
                                                            "name": "Bash", "input": {"command": cmd}}]}}))
            out.append(json.dumps({"type": "user",
                                   "message": {"content": [{"type": "tool_result",
                                                            "tool_use_id": tid,
                                                            "content": item.get("aggregated_output") or ""}]}}))
        elif itype == "function_call":
            tid = item.get("call_id") or "tool_0"
            args = item.get("arguments") or "{}"
            try:
                input_ = json.loads(args) if isinstance(args, str) else (args or {})
            except json.JSONDecodeError:
                input_ = {"raw": args}
            out.append(json.dumps({"type": "assistant",
                                   "message": {"content": [{"type": "tool_use", "id": tid,
                                                            "name": item.get("name") or "tool",
                                                            "input": input_}]}}))
        elif itype == "function_call_output":
            out.append(json.dumps({"type": "user",
                                   "message": {"content": [{"type": "tool_result",
                                                            "tool_use_id": item.get("call_id") or "tool_0",
                                                            "content": item.get("output") or ""}]}}))
    return out

def _codex_interrupt_reason(lines):
    for line in lines:
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "turn.completed":
            return None
    return "cut_off"

def run_codex(task_txt_path, workspace, model, max_tool_calls=0, agent_timeout=3000):
    if not CODEX_CMD:
        raise RuntimeError("codex CLI not found: set CODEX_CMD or put it on PATH")
    cmd = [
        CODEX_CMD, "exec", "--json",
        "-s", "danger-full-access",
        "--skip-git-repo-check",
        "-C", str(workspace),
        "--ephemeral",
    ]
    if model:
        cmd.extend(["--model", model])

    time.sleep(random.uniform(0.3, 1.5))
    with open(task_txt_path, "rb") as stdin_f:
        proc = subprocess.Popen(
            cmd,
            stdin=stdin_f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(workspace),
        )

    out_q = queue.Queue()

    def _reader():
        if proc.stdout is not None:
            for line in proc.stdout:
                out_q.put(line)
        out_q.put(None)

    threading.Thread(target=_reader, daemon=True).start()

    err_lines = []

    def _err_reader():
        if proc.stderr is not None:
            for line in proc.stderr:
                err_lines.append(line)

    err_thread = threading.Thread(target=_err_reader, daemon=True)
    err_thread.start()

    lines = []
    tool_count = 0
    budget_hit = False
    self_killed = False
    deadline = time.time() + agent_timeout

    while True:
        if time.time() >= deadline:
            self_killed = True
            proc.terminate()
            break
        remaining = deadline - time.time()
        try:
            line = out_q.get(timeout=remaining)
        except queue.Empty:
            self_killed = True
            proc.terminate()
            break
        if line is None:
            break
        lines.append(line.rstrip("\n"))
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (obj.get("type") == "item.completed"
                and obj.get("item", {}).get("type") in ("command_execution", "function_call")):
            tool_count += 1
            if max_tool_calls and tool_count >= max_tool_calls:
                budget_hit = True
                self_killed = True
                proc.terminate()
                while True:
                    try:
                        extra = out_q.get(timeout=2)
                    except queue.Empty:
                        break
                    if extra is None:
                        break
                    lines.append(extra.rstrip("\n"))
                break

    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
    err_thread.join(timeout=5)
    stderr = "".join(err_lines)
    if proc.stdout is None:
        return [], f"subprocess stdout is None (stderr: {stderr[:500]})", proc.returncode, False, None
    intr = _codex_interrupt_reason(lines)
    if intr == "cut_off" and self_killed:
        intr = None
    if intr:
        try:
            (Path(workspace) / "_raw_codex_interrupted.jsonl").write_text(
                "\n".join(lines), encoding="utf-8")
        except OSError:
            pass
    return codex_to_claude(lines, model), stderr, proc.returncode, budget_hit, intr

def _flatten_tool_result(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, str):
                parts.append(c)
            elif isinstance(c, dict):
                if "text" in c:
                    parts.append(c["text"])
                elif "content" in c:
                    parts.append(_flatten_tool_result(c["content"]))
        return "\n".join(parts)
    return str(content)

def parse_stream(lines):
    text_parts = []
    tool_entries = []
    tool_results = {}
    current_tool = None
    input_json_buffer = []
    tool_by_id = {}
    tool_id_order = []
    result_text = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        typ = obj.get("type")

        if typ == "assistant":
            content = obj.get("message", {}).get("content")
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        tid = c.get("id")
                        if tid and tid not in tool_by_id:
                            tool_by_id[tid] = {
                                "id": tid,
                                "name": c.get("name"),
                                "input": c.get("input") or {},
                            }
                            tool_id_order.append(tid)

        if typ == "stream_event":
            event = obj.get("event", {})
            event_type = event.get("type")

            if event_type == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    text_parts.append(delta.get("text", ""))
                elif delta.get("type") == "input_json_delta":
                    input_json_buffer.append(delta.get("partial_json", ""))

            elif event_type == "content_block_start":
                block = event.get("content_block", {})
                if block.get("type") == "tool_use":
                    if current_tool is not None:
                        input_str = "".join(input_json_buffer)
                        if input_str.strip():
                            try:
                                current_tool["input"] = json.loads(input_str)
                            except json.JSONDecodeError:
                                current_tool["input"] = {"raw": input_str}
                        tool_entries.append(current_tool)

                    current_tool = {
                        "id": block.get("id"),
                        "name": block.get("name"),
                        "input": {},
                    }
                    input_json_buffer = []

            elif event_type == "content_block_stop":
                if current_tool is not None:
                    input_str = "".join(input_json_buffer)
                    if input_str.strip():
                        try:
                            current_tool["input"] = json.loads(input_str)
                        except json.JSONDecodeError:
                            current_tool["input"] = {"raw": input_str}
                    tool_entries.append(current_tool)
                    current_tool = None
                    input_json_buffer = []

        elif typ == "user":
            content = obj.get("message", {}).get("content", [])
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_result":
                        tid = c.get("tool_use_id")
                        if tid:
                            tool_results[tid] = _flatten_tool_result(c.get("content", ""))

        elif typ == "result":
            rt = obj.get("result")
            if isinstance(rt, str) and rt.strip():
                result_text = rt

    if current_tool is not None:
        input_str = "".join(input_json_buffer)
        if input_str.strip():
            try:
                current_tool["input"] = json.loads(input_str)
            except json.JSONDecodeError:
                current_tool["input"] = {"raw": input_str}
        tool_entries.append(current_tool)

    seen = set()
    merged = []
    for e in tool_entries:
        tid = e.get("id")
        merged.append(tool_by_id.get(tid, e) if tid else e)
        if tid:
            seen.add(tid)
    for tid in tool_id_order:
        if tid not in seen:
            merged.append(tool_by_id[tid])

    for e in merged:
        e["result"] = tool_results.get(e.get("id"), "")

    output = "".join(text_parts)
    if result_text and result_text not in output:
        if len(result_text) >= len(output):
            output = result_text
        else:
            output = output + "\n" + result_text
    return output, merged

def run_judge(skill_dir, task_dir, workspace, tool_log_path, output_path, mode="skill", ignore_cf=False, judge_model=None, judge_api_key=None, judge_api_base=None, no_combo_llm=False, raw_log_path=None, judge_cell=None):
    judge_script = os.environ.get("JUDGE_SCRIPT") or "judge.py"
    judge_path = Path(__file__).parent / judge_script
    if mode == "task":
        cmd = ["python", str(judge_path), "--task",
               str(skill_dir), str(task_dir), str(workspace), str(tool_log_path), str(output_path)]
    else:
        cmd = ["python", str(judge_path), "--skill",
               str(skill_dir), str(workspace), str(tool_log_path), str(output_path)]
    if ignore_cf:
        cmd.append("--ignore-cf")
    if no_combo_llm:
        cmd.append("--no-combo-llm")
    if judge_model:
        cmd.extend(["--model", judge_model])
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["JUDGE_CELL"] = judge_cell or f"{RESULTS.name}/{skill_dir.name}"
    if judge_api_key:
        env["JUDGE_API_KEY"] = judge_api_key
    if judge_api_base:
        env["JUDGE_API_BASE"] = judge_api_base
    if raw_log_path:
        env["JUDGE_RAW_LOG"] = str(raw_log_path)
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=5400, env=env)
    if result.returncode != 0:
        print(f"    judge.py failed: {result.stderr[:200]}")
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"    judge.py did not print JSON: {result.stdout[:200]}")
        return None

def detect_model(out_lines):
    for line in out_lines:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "stream_event":
            e = ev.get("event", {})
            if e.get("type") == "message_start":
                m = e.get("message", {})
                if m.get("model"):
                    return m["model"]
    return None

def archive_workspace(skill_dir, workspace):
    ws_root = Path(WORKSPACES)
    candidates = [ws_root / skill_dir.name] + sorted(
        ws_root.glob(f"{skill_dir.name}-*"), key=lambda p: p.stat().st_mtime, reverse=True)
    source = next((p for p in candidates if p.is_dir()), None)
    if source is None:
        print(f"    [archive] {skill_dir.name}: no workspace output to archive")
        return
    result_dir = RESULTS / skill_dir.name
    archive_dir = result_dir / "workspace"
    if archive_dir.exists():
        shutil.rmtree(archive_dir, ignore_errors=True)
    target = archive_dir
    if archive_dir.exists():
        target = result_dir / "workspace-1"
        n = 2
        while target.exists():
            target = result_dir / f"workspace-{n}"
            n += 1
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(
        "__pycache__", "*.pyc", ".git", "node_modules", ".venv", "venv", "dist", "build"))

_ensure_git_bash()
