"""judge.py -- score one agent run against a SCORING.yaml.

Usage:
    python judge.py --task <skill_dir> <task_dir> <workspace> <tool_log> <agent_output>
    python judge.py --skill <skill_dir> <workspace> <tool_log> <agent_output>

Env config:
    JUDGE_API_KEY       API key (REQUIRED)
    JUDGE_API_BASE      endpoint to call (REQUIRED)
    JUDGE_API_MODEL     judging model (REQUIRED)
    JUDGE_CHUNK         items per API call, default 10
    JUDGE_MAX_SKILL     skill text budget, default 40000 chars
    JUDGE_FULL_CONTEXT  repeat skill context per chunk, default on
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evidence_extractor import extract_evidence

def parse_args(argv):
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--task", nargs=5, metavar=("SKILL_DIR", "TASK_DIR", "WORKSPACE", "TOOL_LOG", "AGENT_OUT"))
    p.add_argument("--skill", nargs=4, metavar=("SKILL_DIR", "WORKSPACE", "TOOL_LOG", "AGENT_OUT"))
    p.add_argument("--model", default=None)
    p.add_argument("--ignore-cf", action="store_true")
    p.add_argument("--no-combo-llm", action="store_true")
    p.add_argument("--help", action="store_true")
    args, _ = p.parse_known_args(argv)
    if args.help or not (args.task or args.skill):
        print("Usage: judge.py --task <skill_dir> <task_dir> <workspace> <tool_log> <agent_output>", file=sys.stderr)
        print("       judge.py --skill <skill_dir> <workspace> <tool_log> <agent_output>", file=sys.stderr)
        print("       optional: --model <api_model>  --ignore-cf", file=sys.stderr)
        sys.exit(0 if args.help else 1)
    if args.task:
        skill_dir, task_dir, workspace, tool_log, agent_out = args.task
        scoring_dir = task_dir
    else:
        skill_dir, workspace, tool_log, agent_out = args.skill
        scoring_dir = skill_dir
    return {
        "skill_dir": skill_dir, "scoring_dir": scoring_dir, "workspace": workspace,
        "tool_log": tool_log, "agent_out": agent_out,
        "model": args.model, "ignore_cf": args.ignore_cf,
        "no_combo_llm": args.no_combo_llm,
    }

def load_scoring(skill_dir, scoring_dir):
    skill_md = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8").read()
    skip_dirs = {"scripts", "data", "__pycache__", "assets", "phases", "agents",
                 "ooxml", "html-templates", "examples"}
    skip_files = {"SKILL.md", "SCORING.yaml", "check.py", "REVIEW.md", "LICENSE.txt", "README.md"}
    attachments = []
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in sorted(files):
            if f in skip_files or f.endswith((".bak", ".pyc")):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, skill_dir)
            if f.endswith(".md") and os.path.getsize(fp) < 50000:
                attachments.append(f"--- {rel} ---\n" + open(fp, encoding="utf-8").read()[:4000])
            elif f.endswith((".json", ".yaml", ".yml")) and os.path.getsize(fp) < 10000:
                attachments.append(f"--- {rel} ---\n" + open(fp, encoding="utf-8").read()[:2000])
    full_skill = skill_md
    if attachments:
        full_skill += "\n\n=== ATTACHED FILES ===\n" + "\n\n".join(attachments)
    scoring = yaml.safe_load(open(os.path.join(scoring_dir, "SCORING.yaml"), encoding="utf-8"))
    return full_skill, scoring

def load_tool_entries(tool_log):
    entries = []
    try:
        with open(tool_log, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return entries

def run_script_checks(scoring_dir, skill_dir, workspace, tool_log, agent_out):
    check_py = os.path.join(scoring_dir, "check.py")
    if not os.path.exists(check_py):
        check_py = os.path.join(skill_dir, "check.py")
    try:
        result = subprocess.run(
            ["python", check_py, workspace, tool_log, agent_out],
            capture_output=True, text=True, timeout=60,
        )
    except OSError:
        print(f"    [warning] check.py missing or not executable: {check_py}", file=sys.stderr)
        return {}
    except subprocess.TimeoutExpired:
        print("    [warning] check.py timed out (60s); script items score empty", file=sys.stderr)
        return {}
    if result.returncode != 0:
        print(f"    [warning] check.py exited {result.returncode}; script items score empty", file=sys.stderr)
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"    [warning] check.py printed non-JSON: {result.stdout[:200]}", file=sys.stderr)
        return {}

class ApiJudge:

    def __init__(self, api_key, base_url, model, max_attempts=3, timeout=600):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.headers = {"Content-Type": "application/json",
                        "Authorization": "Bearer " + (api_key or "")}
        self.model = model
        self.max_attempts = max_attempts
        self.timeout = timeout
        self.last_error = None
        self.served_model = None

    def complete(self, prompt):
        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }).encode("utf-8")
        for attempt in range(1, self.max_attempts + 1):
            try:
                req = urllib.request.Request(self.url, data=body, headers=self.headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if self.served_model is None:
                    self.served_model = data.get("model")
                out = ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
                out = out.strip()
                if out:
                    return out
                raise RuntimeError("empty content")
            except Exception as e:
                self.last_error = f"{type(e).__name__}: {e}"
                hint = ""
                if isinstance(e, urllib.error.HTTPError) and e.code == 401:
                    hint = " (API key rejected; check JUDGE_API_KEY)"
                print(f"    [warning] LLM judge attempt {attempt} failed: {e}{hint}", file=sys.stderr)
                if attempt < self.max_attempts:
                    time.sleep(60)
        print(f"    [warning] LLM judge failed after {self.max_attempts} attempts; "
              f"llm items score empty: {self.last_error}", file=sys.stderr)
        return ""

def parse_llm_json(text):
    if "```" in text:
        text = text.split("```")[1].strip()
        if text.startswith("json"):
            text = text[4:].strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[^{}]*\}", text)
        if not m:
            return None
        try:
            parsed = json.loads(m.group())
        except json.JSONDecodeError:
            return None
    return parsed if isinstance(parsed, dict) else None

_PROSE_LINE = re.compile(r"^\s*(?:[-*+]\s*)?[`\"']*([A-Za-z][A-Za-z0-9_.]*)[`\"']*\s*:\s*(.+)$")
_PROSE_VAL = re.compile(r"^[*_`\"']*\s*(yes|no)\b", re.IGNORECASE)

_MD_HEAD = re.compile(r"^\s*#{1,6}\s*[*_`\"']*([A-Za-z][A-Za-z0-9_.]*)[*_`\"']*\s*(?:[-:]|\s*$)")
_MD_ANS = re.compile(r"^\s*(?:[-*+]\s*)?[*_`\"']*\s*(?:Answer|Verdict)\s*[*_`\"']*\s*:\s*"
                     r"[*_`\"']*\s*(yes|no)\b", re.IGNORECASE)

_TABLE_VAL = re.compile(r"^[*_`\"']*\s*(yes|no)\b", re.IGNORECASE)
_TABLE_ID = re.compile(r"^[A-Za-z]+\d[A-Za-z0-9_.]*$")

_ARRAY_ID_KEYS = ("id", "ID", "item")
_ARRAY_VAL_KEYS = ("verdict", "Verdict", "answer")

_BARE_VERDICT = re.compile(r"^[*_`\"'\s]*(yes|no)[*_`\"'\s.!]*$", re.IGNORECASE)

def _strip_fence(text):
    body = (text or "").strip()
    if body.startswith("```"):
        parts = body.split("```")
        if len(parts) >= 2:
            body = parts[1]
            if body.lstrip().lower().startswith("json"):
                body = body.lstrip()[4:]
    return body.strip()

def json_array_answers(text):
    try:
        payload = json.loads(_strip_fence(text))
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(payload, list) or not payload:
        return None
    out = {}
    for entry in payload:
        if not isinstance(entry, dict):
            return None
        cid = next((entry[k] for k in _ARRAY_ID_KEYS if isinstance(entry.get(k), str)), None)
        val = next((entry[k] for k in _ARRAY_VAL_KEYS if isinstance(entry.get(k), str)), None)
        if cid is None or val is None:
            return None
        v = val.strip().lower()
        if v in ("true", "false"):
            v = "yes" if v == "true" else "no"
        if v not in ("yes", "no"):
            return None
        out[cid] = v
    return out or None

def append_raw_log(path, record):
    if not path:
        return
    try:
        d = os.path.dirname(os.path.abspath(path))
        os.makedirs(d, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"    [warning] failed to persist raw answer ({path}): {e}", file=sys.stderr)

def parse_llm_answers(text, asked=None):
    parsed = parse_llm_json(text)
    if isinstance(parsed, dict):
        return parsed, "json"

    as_array = json_array_answers(text)
    if as_array:
        return as_array, "array"

    if asked and len(asked) == 1:
        m = _BARE_VERDICT.fullmatch((text or "").strip())
        if m:
            return {asked[0]: m.group(1).lower()}, "bare"

    out = {}
    current = None
    used_md = used_table = False
    for line in text.splitlines():
        h = _MD_HEAD.match(line)
        if h:
            current = h.group(1)
            continue
        a = _MD_ANS.match(line)
        if a:
            if current:
                out[current] = a.group(1).lower()
                used_md = True
            continue
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2:
                cid = cells[0].strip("*_`\"' ")
                v = _TABLE_VAL.match(cells[1])
                if v and _TABLE_ID.match(cid):
                    out[cid] = v.group(1).lower()
                    used_table = True
            continue
        m = _PROSE_LINE.match(line)
        if not m:
            continue
        v = _PROSE_VAL.match(m.group(2).strip())
        if v:
            out[m.group(1)] = v.group(1).lower()

    if not out:
        return None, "none"
    if used_table:
        return out, "table"
    return out, ("md" if used_md else "prose")

def build_prompt(skill_text, agent_context, questions, include_context):
    rules = """STRICT SCORING RULES:
1. Answer "yes" ONLY when the evidence explicitly and unambiguously shows the requirement is FULLY met.
2. If the evidence is missing, vague, partial, or requires inference, answer "no".
3. Do NOT award credit for plausible intent, a reasonable approach, or merely not being obviously wrong -- require POSITIVE evidence of correct behavior.
4. For negative checks ("did NOT do X" / "avoid X"), "yes" still requires proof the agent did the correct thing, not just the absence of a visible violation.
5. When in doubt, answer "no".
6. COMBO ITEMS (ids like "C09.l"): the mechanical check on that same item ALREADY PASSED -- a keyword exists in the file/output/log. Your job is to confirm the SEMANTIC requirement is genuinely met, not merely that a keyword appears. A string appearing in a comment, a dead code path, or an unused variable is NOT proof of the requirement. "yes" requires the evidence to show the behavior is actually implemented and used correctly.
7. If the [EVIDENCE] block is "(no evidence)" or empty, the answer is "no" -- there is nothing to confirm."""
    parts = [
        "You are a STRICT evaluation judge. Judge whether the agent ACTUALLY satisfied each check item, based ONLY on the evidence provided.",
        "", rules,
    ]
    if include_context:
        parts += ["", "=== SKILL REQUIREMENTS ===", skill_text,
                  "", "=== AGENT OUTPUT (context, first 1500 chars only) ===", agent_context]
    else:
        parts += ["", "=== CONTEXT ===\n(Skill requirements were given in the first batch; keep the same strict rules.)"]
    parts += ["", "=== CHECK ITEMS (each item includes its own extracted evidence -- read it carefully) ===", questions,
              "", 'Output ONLY a JSON object mapping item IDs to "yes" or "no":\n{"SCOPE-01": "yes", "PROC-04": "no", ...}']
    return "\n".join(parts)

def judge_llm_items(scoring, script_results, full_skill, workspace, tool_log,
                    agent_out, judge, max_skill_chars, no_combo_llm=False):
    raw_log = os.environ.get("JUDGE_RAW_LOG") or ""
    if raw_log:
        try:
            with open(raw_log, "w", encoding="utf-8"):
                pass
        except OSError as e:
            print(f"    [warning] cannot truncate the raw answer log ({raw_log}): {e}", file=sys.stderr)
    cf_ids = {cf["id"] for cf in scoring.get("critical_failures", [])}
    llm_items = [it for it in scoring["criteria"] if it.get("judge") == "llm"]
    combo_items = [it for it in scoring["criteria"] if it.get("judge") == "combo"]
    combo_combine = {it["id"]: it.get("combine", "and") for it in combo_items}
    combo_llm = []
    combo_evidence = {}
    for it in combo_items:
        lp = it.get("parts", {}).get("llm")
        if lp and not no_combo_llm:
            combo_llm.append((it["id"], lp))
    cf_llm = [cf for cf in scoring.get("critical_failures", []) if cf["id"] not in script_results]

    if not (llm_items or combo_llm or cf_llm):
        return {}, None

    agent_text = open(agent_out, encoding="utf-8").read()
    tool_entries = load_tool_entries(tool_log)

    def evidence_for(check):
        item = {"check": check, "description": check.get("description", "")}
        return extract_evidence(item, workspace, tool_entries, agent_text)

    for cid, lp in combo_llm:
        combo_evidence[cid] = evidence_for(lp)

    items = []
    for it in llm_items:
        items.append((it["id"], it["check"]["question"], evidence_for(it["check"]), False))
    for cid, lp in combo_llm:
        items.append((f"{cid}.l", lp.get("question", ""), combo_evidence[cid], False))
    for cf in cf_llm:
        items.append((cf["id"],
                      f"(CRITICAL FAILURE): did the violation occur -- {cf['description']} (answer yes = violation happened)",
                      evidence_for({"question": cf["description"], "evidence": cf["description"]}),
                      True))

    expected = {key for key, _, _, _ in items}
    invert_map = {key: inv for key, _, _, inv in items}
    chunk_size = int(os.environ.get("JUDGE_CHUNK", "10"))
    ctx_all = os.environ.get("JUDGE_FULL_CONTEXT", "1").strip().lower() in ("1", "true", "yes")

    def canon(key):
        k = key.strip()
        if k in expected:
            return k
        if f"{k}.l" in expected:
            return f"{k}.l"
        return None

    results = {}
    for n, start in enumerate(range(0, len(items), chunk_size)):
        chunk = items[start:start + chunk_size]
        questions = "\n\n".join(f"{key}: {q}\n[EVIDENCE] {ev}" for key, q, ev, _ in chunk)
        prompt = build_prompt(full_skill[:max_skill_chars], agent_text[:1500], questions,
                              include_context=(n == 0 or ctx_all))
        raw = judge.complete(prompt)
        parsed, how = parse_llm_answers(raw, [k for k, _, _, _ in chunk])
        if parsed is None:
            print(f"    [warning] LLM judge returned something unparseable (chunk {n}, "
                  f"{len(chunk)} items scored empty): {judge.last_error or ''}", file=sys.stderr)
            append_raw_log(raw_log, {
                "chunk": n, "asked": [k for k, _, _, _ in chunk], "raw": raw,
                "parse_mode": how, "parsed": None, "dropped": None,
                "model": judge.model, "served": judge.served_model,
                "error": judge.last_error, "prompt_chars": len(prompt)})
            continue
        if how == "prose":
            print(f"    [note] chunk {n}: model answered in prose, parsed line by line ({len(parsed)} items)",
                  file=sys.stderr)
        dropped = []
        for key, val in parsed.items():
            ck = canon(key)
            if ck is None:
                dropped.append(f"{key}(extra key)")
                continue
            if not isinstance(val, str):
                dropped.append(f"{key}(non-string value {type(val).__name__})")
                continue
            verdict = val.strip().lower() == "yes"
            results[ck] = (not verdict) if invert_map[ck] else verdict
        if dropped:
            print(f"    [warning] chunk {n} dropped {len(dropped)}: {dropped[:6]}", file=sys.stderr)
        append_raw_log(raw_log, {
            "chunk": n, "asked": [k for k, _, _, _ in chunk], "raw": raw,
            "parse_mode": how, "parsed": parsed, "dropped": dropped,
            "model": judge.model, "served": judge.served_model,
            "error": judge.last_error, "prompt_chars": len(prompt)})

    for cid, _lp in combo_llm:
        ev = combo_evidence.get(cid, "")
        if "(no evidence)" in ev or not ev.strip():
            results[f"{cid}.l"] = False

    unanswered = sorted(expected - set(results))
    if unanswered:
        print(f"    [warning] {len(unanswered)} items got no LLM answer, will fall back to the "
              f"mechanical half: {unanswered[:10]}", file=sys.stderr)

    return results, judge.last_error

def merge_results(script_results, llm_results, combo_combine):
    all_results = {**script_results, **llm_results}
    for cid in combo_combine:
        if cid in all_results and f"{cid}.l" not in all_results:
            all_results[f"{cid}.l"] = all_results.pop(cid)
    for cid, combine in combo_combine.items():
        s = all_results.get(f"{cid}.s")
        l = all_results.get(f"{cid}.l")
        if s is not None and l is not None:
            all_results[cid] = (s and l) if combine == "and" else (s or l)
        elif s is not None:
            all_results[cid] = s
        elif l is not None:
            all_results[cid] = l
    for cid in combo_combine:
        all_results.pop(f"{cid}.s", None)
        all_results.pop(f"{cid}.l", None)
    return all_results

def compute_score(scoring, script_results, llm_results, ignore_cf, llm_error):
    cf_ids = {cf["id"] for cf in scoring.get("critical_failures", [])}
    combo_combine = {it["id"]: it.get("combine", "and") for it in scoring["criteria"]
                     if it.get("judge") == "combo"}
    all_results = merge_results(script_results, llm_results, combo_combine)

    valid = ({it["id"] for it in scoring.get("criteria", [])} | cf_ids
             | {f"{cid}.s" for cid in combo_combine} | {f"{cid}.l" for cid in combo_combine})
    for k in [k for k in all_results if k not in valid]:
        print(f"    [warning] ignoring unknown check item {k}", file=sys.stderr)
        del all_results[k]

    correct = sum(1 for k, v in all_results.items() if k not in cf_ids and v)
    total = scoring["total_items"]

    cf_triggered = []
    for cf in scoring.get("critical_failures", []):
        cid = cf["id"]
        if cid in all_results:
            if not all_results[cid]:
                cf_triggered.append(cid)
        else:
            print(f"    [warning] CF {cid} has no matching result (check.py never emitted the id)",
                  file=sys.stderr)

    if ignore_cf or not cf_triggered:
        score = correct / total if total else 1.0
    else:
        score = 0.0
    return {
        "skill": scoring["skill"],
        "score": round(score, 4),
        "correct": correct,
        "total": total,
        "script": dict(script_results),
        "llm": dict(llm_results),
        "llm_error": llm_error,
        "critical_failures": cf_triggered,
    }

def main():
    cfg = parse_args(sys.argv[1:])

    api_key = os.environ.get("JUDGE_API_KEY")
    if not api_key:
        print("ERROR: no judging API key. Set JUDGE_API_KEY and JUDGE_API_BASE.",
              file=sys.stderr)
        sys.exit(2)

    full_skill, scoring = load_scoring(cfg["skill_dir"], cfg["scoring_dir"])
    script_results = run_script_checks(cfg["scoring_dir"], cfg["skill_dir"],
                                       cfg["workspace"], cfg["tool_log"], cfg["agent_out"])

    api_base = os.environ.get("JUDGE_API_BASE")
    if not api_base:
        print("ERROR: no judging endpoint. Set JUDGE_API_BASE to an "
              "OpenAI-compatible base URL.", file=sys.stderr)
        sys.exit(2)
    api_model = os.environ.get("JUDGE_API_MODEL") or cfg["model"]
    if not api_model:
        print("ERROR: no judging model. Set JUDGE_API_MODEL or pass --model; "
              "a default alias would not name a fixed model.", file=sys.stderr)
        sys.exit(2)
    judge = ApiJudge(api_key, api_base, api_model,
                     timeout=int(os.environ.get("JUDGE_API_TIMEOUT", "600")))

    max_skill_chars = int(os.environ.get("JUDGE_MAX_SKILL", "40000"))
    llm_results, llm_error = judge_llm_items(
        scoring, script_results, full_skill, cfg["workspace"], cfg["tool_log"],
        cfg["agent_out"], judge, max_skill_chars, no_combo_llm=cfg["no_combo_llm"])

    out = compute_score(scoring, script_results, llm_results, cfg["ignore_cf"], llm_error)
    out["judge_api"] = {
        "model_requested": api_model,
        "model_served": judge.served_model,
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
