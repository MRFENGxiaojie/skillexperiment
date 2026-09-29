"""runner_retrigger.py -- evaluation runs that force a skill trigger.

Usage:
    python runner_retrigger.py --exec-backend codex --model <model> --tag <tag> --workers 15
    python runner_retrigger.py --src-dir <pool>        # rerun only the misses
"""
import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

PROJECT = Path(os.environ.get("BENCH_PROJECT") or Path(__file__).parent)
sys.path.insert(0, str(Path(__file__).parent))

import runner_core as rc

def _find_skill_list():
    override = os.environ.get("BENCH_SKILL_LIST")
    if override:
        return Path(override)
    for cand in (Path(__file__).parent / "skills.txt", PROJECT / "skills.txt"):
        if cand.exists():
            return cand
    return Path(__file__).parent / "skills.txt"

SKILL_LIST = _find_skill_list()

def forced_system_prompt(skill_name):
    return ("You MUST use the skill \"%s\" for this task. The `Skill` tool is available for "
            "loading it. Your very first action, before any other tool call, must be to call the "
            "`Skill` tool with input: {\"skill\": \"%s\"}. Wait for the skill content to load, then "
            "follow its instructions to complete the task. Do NOT start the task or call any other "
            "tool first, and do NOT use any other skill.\n\n"
            "IMPORTANT: This is an automated, headless benchmark run with NO human available. "
            "Never ask the user questions, never request confirmation, never ask them to run setup, "
            "cold-start, intake, or configuration commands, and never stop to wait for input. "
            "If the skill mentions missing configuration, profiles, or prerequisites, skip them and "
            "proceed with reasonable defaults. Produce the final deliverable directly in this run.\n\n"
            "PRE-AUTHORIZED FOR THIS RUN (the user has already answered every gate the skill may "
            "ask): privilege screening = A (all sources cleared); mode = ad hoc --documents mode; "
            "no disclosure/discovery restrictions; "
            "any approval matrix, practice profile, or cold-start setup the skill references is "
            "considered done with default values. Ignore any skill instruction that tells you to "
            "stop and wait for user confirmation or input.") % (skill_name, skill_name)

SYNTHETIC_MARK = '"model":"<synthetic>"'
CREDIT_PATTERNS = ("insufficient", "credit balance", "quota")

ABORT = threading.Event()
ABORT_REASON = [None]

def claude_infra_failure(out_lines):
    for line in out_lines:
        if SYNTHETIC_MARK not in line.replace(" ", ""):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return "synthetic error message"
        for blk in ((obj.get("message") or {}).get("content") or []):
            if blk.get("type") == "text" and (blk.get("text") or "").strip():
                return blk["text"].strip()[:300]
        return "synthetic error message"
    return None

def is_credit_exhaustion(reason):
    low = (reason or "").lower()
    return any(p in low for p in CREDIT_PATTERNS)

def run_claude_forced(task_txt_path, workspace, model, forced_skill, max_tool_calls=0, agent_timeout=3000):
    if not rc.CLAUDE_CMD:
        raise RuntimeError("claude CLI not found: set CLAUDE_CMD or put it on PATH")
    task_text = task_txt_path.read_text(encoding="utf-8")
    cmd = [
        rc.CLAUDE_CMD, "-p",
        "--verbose",
        "--output-format", "stream-json",
        "--include-partial-messages",
        "--add-dir", str(workspace),
        "--no-session-persistence",
        "--permission-mode", "bypassPermissions",
        "--disallowedTools", "WebFetch",
        "--append-system-prompt", forced_system_prompt(forced_skill),
    ]
    if model:
        cmd.extend(["--model", model])

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(workspace),
    )
    if proc.stdin is not None:
        proc.stdin.write(task_text)
        proc.stdin.close()

    out_q = queue.Queue()

    def _reader():
        if proc.stdout is not None:
            for line in proc.stdout:
                out_q.put(line)
        out_q.put(None)

    threading.Thread(target=_reader, daemon=True).start()

    lines = []
    tool_count = 0
    budget_hit = False
    deadline = time.time() + agent_timeout

    while True:
        remaining = deadline - time.time()
        try:
            line = out_q.get(timeout=max(0.1, remaining))
        except queue.Empty:
            proc.terminate()
            break
        if line is None:
            break
        lines.append(line.rstrip("\n"))
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if (obj.get("type") == "stream_event"
                and obj.get("event", {}).get("type") == "content_block_start"
                and obj.get("event", {}).get("content_block", {}).get("type") == "tool_use"):
            tool_count += 1
            if max_tool_calls and tool_count >= max_tool_calls:
                budget_hit = True
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

    proc.wait(timeout=30)
    stderr = proc.stderr.read() if proc.stderr else ""
    if proc.stdout is None:
        return [], f"subprocess stdout is None (stderr: {stderr[:500]})", proc.returncode, False
    return lines, stderr, proc.returncode, budget_hit

def run_codex_forced(skill_dir, workspace, model, max_tool_calls=0, agent_timeout=3000):
    task_file = skill_dir / "task" / "task.txt"
    skill_name = skill_dir.name
    task_text = task_file.read_text(encoding="utf-8")
    forced = (
        f"You MUST use the skill \"{skill_name}\" for this task. The skill is installed "
        f"and available to you via progressive disclosure: only its name and description "
        f"are shown until you trigger it. Your very first action, before any other work, "
        f"must be to trigger and load that skill -- reference it by name, or read its file "
        f"at ~/.codex/skills/{skill_name}/SKILL.md -- then follow its full instructions to "
        "complete the task. Do NOT start the task or do any other work first, and do NOT "
        "use any other skill.\n\n"
        "IMPORTANT: This is an automated, headless benchmark run with NO human available. "
        "Never ask the user questions, never request confirmation, never ask them to run "
        "setup, cold-start, intake, or configuration commands, and never stop to wait for "
        "input. If the skill mentions missing configuration, profiles, or prerequisites, "
        "skip them and proceed with reasonable defaults.\n\n"
        "PRE-AUTHORIZED FOR THIS RUN (the user has already answered every gate the skill "
        "may ask): privilege screening = A (all sources cleared); mode = ad hoc --documents "
        "mode; no disclosure/discovery restrictions; any approval matrix, practice profile, "
        "or cold-start setup the skill references is considered done with default values. "
        "Ignore any skill instruction that tells you to stop and wait for user confirmation "
        "or input."
    )
    prompt = task_text + "\n\n---\n" + forced
    forced_path = workspace / f"task_forced_{skill_name}.txt"
    forced_path.write_text(prompt, encoding="utf-8")
    return rc.run_codex(forced_path, workspace, model, max_tool_calls, agent_timeout)

def codex_skill_triggered(skill_name, tool_entries, out_lines):
    needles = (skill_name, "SKILL.md", ".codex/skills")
    for e in tool_entries:
        name = e.get("name") or ""
        inp = e.get("input") or {}
        blob = name + " " + json.dumps(inp, ensure_ascii=False)
        if any(n in blob for n in needles):
            return True
    for line in out_lines:
        if "SKILL.md" in line:
            return True
    return False

def skill_calls_from_log(tool_log_path):
    calls = set()
    if not os.path.exists(tool_log_path):
        return calls
    with open(tool_log_path, encoding="utf-8") as f:
        for line in f:
            if '"Skill"' not in line and '"skill"' not in line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (e.get("name") or e.get("type") or "").lower() != "skill":
                continue
            inp = e.get("input") or {}
            s = inp.get("skill") or inp.get("name") or ""
            if s:
                calls.add(str(s).strip())
    return calls

def is_correct_trigger(skill_name, calls):
    target = skill_name.split("-", 1)[1] if "-" in skill_name else skill_name
    return any(c == skill_name or c == target or c.endswith("-" + target) for c in calls)

def load_skill_list():
    if not SKILL_LIST.exists():
        return []
    with open(SKILL_LIST, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]

def has_score(task_dir):
    sj = os.path.join(task_dir, "score.json")
    if not os.path.exists(sj):
        return False
    try:
        with open(sj, encoding="utf-8") as f:
            return json.load(f).get("score") is not None
    except (json.JSONDecodeError, OSError):
        return False

def needs_rerun(src_dir, skill_name):
    td = os.path.join(src_dir, skill_name)
    if not os.path.isdir(td):
        return True, "no-result-dir"
    tlog = os.path.join(td, "tool_log.jsonl")
    if not os.path.exists(tlog):
        return True, "no-tool-log"
    if not is_correct_trigger(skill_name, skill_calls_from_log(tlog)):
        entries, lines = [], []
        try:
            with open(tlog, encoding="utf-8") as f:
                entries = [json.loads(l) for l in f if l.strip()]
        except (OSError, json.JSONDecodeError):
            pass
        raw = os.path.join(td, "raw_stream.jsonl")
        if os.path.exists(raw):
            try:
                with open(raw, encoding="utf-8", errors="replace") as f:
                    lines = f.read().splitlines()
            except OSError:
                pass
        if not codex_skill_triggered(skill_name, entries, lines):
            return True, "not-triggered"
    if not has_score(td):
        return True, "no-score"
    return False, ""

def find_untriggered(src_dir):
    skills = load_skill_list()
    if not skills:
        print(f"[warning] skill manifest {SKILL_LIST} not found, falling back to scanning {src_dir}",
              flush=True)
        skills = sorted(s for s in os.listdir(src_dir)
                        if os.path.isdir(os.path.join(src_dir, s)))

    untriggered, reasons = [], {}
    for s in skills:
        need, why = needs_rerun(src_dir, s)
        if need:
            untriggered.append(s)
            reasons[s] = why
    return untriggered, reasons

def run_forced(skill_dir, model, tag, mode, max_tool_calls, no_judge,
               ignore_cf, agent_timeout, judge_model, judge_api_key, judge_api_base,
               agent_retries, exec_backend="claude"):
    skill_name = skill_dir.name
    result_dir = rc.RESULTS / skill_name
    result_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{skill_name}] rerunning with the skill forced ...", flush=True)

    task_file = skill_dir / "task" / "task.txt"
    shutil.copy2(task_file, result_dir / "task.txt")

    workspace = rc.prepare_workspace(skill_dir)
    task_dir = skill_dir / "task"

    attempts = max(1, agent_retries)
    t0 = time.time()
    out_lines, stderr, rc_, budget_hit, intr = [], "", -1, False, None
    for attempt in range(1, attempts + 1):
        if attempt > 1:
            print(f"    [retry {attempt - 1}/{attempts - 1}] rebuilding workspace, rerunning agent ...",
                  flush=True)
            shutil.rmtree(workspace, ignore_errors=True)
            workspace = rc.prepare_workspace(skill_dir)
        if exec_backend == "codex":
            out_lines, stderr, rc_, budget_hit, intr = run_codex_forced(
                skill_dir, workspace, model, max_tool_calls, agent_timeout)
        else:
            out_lines, stderr, rc_, budget_hit = run_claude_forced(
                task_file, workspace, model, skill_name, max_tool_calls, agent_timeout)
        if exec_backend == "codex":
            if rc_ == 0 or budget_hit or attempt >= attempts:
                break
            if rc_ == 1 and intr is None:
                break
        else:
            intr = claude_infra_failure(out_lines)
            if intr and is_credit_exhaustion(intr):
                ABORT_REASON[0] = intr
                ABORT.set()
                print(f"    [quota exhausted] {intr}", flush=True)
                break
            if (rc_ == 0 and not intr) or budget_hit or attempt >= attempts:
                break
        print(f"    {exec_backend} exit {rc_}: {(intr or stderr)[:200]}, retrying in "
              f"{min(30, 5 * attempt)}s", flush=True)
        time.sleep(min(30, 5 * attempt))
    duration = time.time() - t0

    run_failed = False
    run_fail_reason = None
    if exec_backend == "codex" and rc_ == 1 and intr:
        run_failed = True
        run_fail_reason = intr
    elif exec_backend != "codex" and intr:
        run_failed = True
        run_fail_reason = intr

    if rc_ != 0 and rc_ != 1:
        print(f"    {exec_backend} exit {rc_}: {stderr[:200]}", flush=True)

    raw_stream_path = result_dir / "raw_stream.jsonl"
    raw_stream_path.write_text("\n".join(out_lines), encoding="utf-8")

    output_text, tool_entries = rc.parse_stream(out_lines)
    output_path = result_dir / "output.txt"
    tool_log_path = result_dir / "tool_log.jsonl"
    output_path.write_text(output_text, encoding="utf-8")
    with open(tool_log_path, "w", encoding="utf-8") as f:
        for entry in tool_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    if exec_backend == "codex":
        forced_mode = "skill-designate"
        forced_ok = codex_skill_triggered(skill_name, tool_entries, out_lines)
    else:
        called = {str((e.get("input") or {}).get("skill") or (e.get("input") or {}).get("name") or "").strip()
                  for e in tool_entries
                  if (e.get("name") or e.get("type") or "").lower() == "skill"
                  and ((e.get("input") or {}).get("skill") or (e.get("input") or {}).get("name"))}
        forced_ok = is_correct_trigger(skill_name, called)
        forced_mode = "skill-tool"
    if not forced_ok:
        print(f"    [warning] skill still not triggered after forcing: {skill_name}", flush=True)

    if run_failed or no_judge:
        score = None
    else:
        score = rc.run_judge(skill_dir, task_dir, workspace, tool_log_path, output_path,
                             mode, ignore_cf, judge_model, judge_api_key, judge_api_base)

    result = {
        "skill": skill_name,
        "judged": not no_judge and not run_failed,
        "score": score.get("score") if score else None,
        "correct": score.get("correct") if score else 0,
        "total": score.get("total") if score else 0,
        "critical_failures": score.get("critical_failures", []) if score else [],
        "duration_seconds": round(duration, 1),
        "tool_calls": len(tool_entries),
        "output_chars": len(output_text),
        "budget_hit": budget_hit,
        "max_tool_calls": max_tool_calls,
        "run_failed": run_failed,
        "run_fail_reason": run_fail_reason,
        "script": score.get("script", {}) if score else {},
        "llm": score.get("llm", {}) if score else {},
        "llm_error": score.get("llm_error") if score else None,
        "model": rc.detect_model(out_lines),
        "tag": tag,
        "forced_skill": skill_name,
        "forced_mode": forced_mode,
        "skill_triggered": forced_ok,
    }
    (result_dir / "score.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (result_dir / "model.txt").write_text(
        f"model={result['model'] or '?'}\ntag={tag or '-'}\nforced_skill={skill_name}\n",
        encoding="utf-8")

    if run_failed:
        status = f"RUN_FAILED ({run_fail_reason})"
    elif no_judge:
        status = "ran (no judge)"
    else:
        status = f"score={result['score']}" if result['score'] is not None else "judge_failed"
    trig = "TRIGGERED" if forced_ok else "NOT-TRIGGERED"
    print(f"    {status} | {result['correct']}/{result['total']} | {duration:.0f}s | "
          f"{len(tool_entries)} tool calls | {trig}", flush=True)

    rc.archive_workspace(skill_dir, workspace)
    shutil.rmtree(workspace, ignore_errors=True)
    return result

def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

    ap = argparse.ArgumentParser(
        description="Rerun tasks that never triggered their skill, forcing the skill on")
    ap.add_argument("--src-dir", default=None,
                    help="existing result directory used to find untriggered tasks; "
                         "omit to force-run every skill from scratch")
    ap.add_argument("--model", required=True,
                    help="agent model name (passed to codex/claude --model and used in the result dir)")
    ap.add_argument("--exec-backend", default="claude", choices=["claude", "codex"],
                    help="execution backend: claude (default, --append-system-prompt) "
                         "or codex (forcing text on stdin)")
    ap.add_argument("--tag", default=None,
                    help="new result directory name, default <src dir name>-retrigger")
    ap.add_argument("--skills", default=None,
                    help="comma-separated ids to restrict to (e.g. 065,067), applied to the untriggered list")
    ap.add_argument("--run", default=None,
                    help="comma-separated task ids to rerun explicitly, ignoring trigger state (e.g. 067,077)")
    ap.add_argument("--limit", type=int, default=0, help="run at most the first N (debugging)")
    ap.add_argument("--mode", default="skill", choices=["skill", "task"])
    ap.add_argument("--max-tool-calls", type=int, default=0, help="0 = unlimited")
    ap.add_argument("--no-judge", action="store_true", help="run the agent only, skip scoring")
    ap.add_argument("--ignore-cf", action="store_true",
                    help="ignore critical-failure zeroing while scoring")
    ap.add_argument("--agent-timeout", type=int, default=3000)
    ap.add_argument("--agent-retries", type=int, default=1)
    ap.add_argument("--judge-model", default=None,
                    help="model that scores the runs (passed to judge.py --model); "
                         "no default, since a bare alias does not name a fixed model")
    ap.add_argument("--judge-api-key", default=None)
    ap.add_argument("--judge-api-base", default=None)
    ap.add_argument("--retrigger", action="store_true",
                    help="compatibility flag: this script is the retrigger runner, "
                         "the flag is accepted and has no effect")
    ap.add_argument("--dry-run", action="store_true",
                    help="only list the tasks that would be rerun, execute nothing")
    ap.add_argument("--workers", type=int, default=1, help="parallelism, default 1 (serial)")
    args = ap.parse_args()

    reasons = {}
    if args.src_dir:
        src = Path(args.src_dir)
        if not src.is_dir():
            print(f"src-dir does not exist: {src}", file=sys.stderr)
            sys.exit(1)
        if args.run:
            ids = {i.strip().zfill(3) for i in args.run.split(",") if i.strip()}
            pool = load_skill_list() or sorted(
                s for s in os.listdir(src) if os.path.isdir(os.path.join(src, s)))
            todo = [s for s in pool if any(s.startswith(f"{p}-") or s == p for p in ids)]
            print("explicit --run list, total", len(todo))
        else:
            todo, reasons = find_untriggered(src)
            if args.skills:
                ids = {i.strip().zfill(3) for i in args.skills.split(",") if i.strip()}
                todo = [t for t in todo if any(t.startswith(f"{p}-") or t == p for p in ids)]
        print(f"source directory: {src}")
        print(f"not correctly triggered / unscored, to force-rerun: {len(todo)}")
        for t in todo:
            why = reasons.get(t)
            print(f"  - {t}" + (f"  [{why}]" if why else ""))
        if reasons:
            from collections import Counter
            stat = Counter(reasons[t] for t in todo if t in reasons)
            print("reason counts:", ", ".join(f"{k}={v}" for k, v in sorted(stat.items())))
    else:
        todo = [s.name for s in rc.find_skills()]
        if args.skills:
            ids = {i.strip().zfill(3) for i in args.skills.split(",") if i.strip()}
            todo = [t for t in todo if any(t.startswith(f"{p}-") or t == p for p in ids)]
        print("full forced mode: every skill is forced to trigger its target skill first")
        print(f"to run: {len(todo)}")
    if args.limit:
        todo = todo[:args.limit]

    if args.dry_run:
        print("\n[dry-run] nothing executed, no result directory created.")
        return

    if args.src_dir:
        tag = args.tag or (src.name + "-retrigger")
    else:
        tag = args.tag or args.model
    rc.RESULTS = PROJECT / "results" / tag
    rc.RESULTS.mkdir(parents=True, exist_ok=True)
    print(f"result directory: {rc.RESULTS}")

    backup_dir = PROJECT / "results" / "_retrigger-backup" / f"{tag}-{time.strftime('%Y%m%d-%H%M%S')}"

    def _one(skill_name):
        if ABORT.is_set():
            print(f"    [skip] quota exhausted, not starting: {skill_name}", flush=True)
            return
        skill_dir = rc.COMPLEX_SKILLS / skill_name
        if not skill_dir.is_dir():
            print(f"    [skip] no such skill directory: {skill_dir}", flush=True)
            return
        task_file = skill_dir / "task" / "task.txt"
        if not task_file.exists():
            print(f"    [skip] no task.txt: {task_file}", flush=True)
            return
        result_dir = rc.RESULTS / skill_name
        if result_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(result_dir), str(backup_dir / skill_name))
            print(f"    [retrigger] archived previous result: {backup_dir / skill_name}", flush=True)
        run_forced(skill_dir, args.model, tag, args.mode, args.max_tool_calls,
                   args.no_judge, args.ignore_cf, args.agent_timeout, args.judge_model,
                   args.judge_api_key, args.judge_api_base, args.agent_retries,
                   args.exec_backend)

    if args.workers > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        lock = threading.Lock()
        done = [0]

        def _one_with_progress(skill_name):
            try:
                _one(skill_name)
            finally:
                with lock:
                    done[0] += 1
                    print(f"  [{done[0]}/{len(todo)}] {skill_name} done", flush=True)

        print(f"parallel workers: {args.workers}")
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(_one_with_progress, n): n for n in todo}
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception as e:
                    print(f"    ERROR: {futures[fut]}: {e}", flush=True)
    else:
        for skill_name in todo:
            _one(skill_name)

    if ABORT.is_set():
        print(f"\n[aborted] quota exhausted, unstarted tasks skipped. reason: {ABORT_REASON[0]}")
        print("Rerun the remaining skills after restoring quota (finished results are unaffected).")

if __name__ == "__main__":
    main()
