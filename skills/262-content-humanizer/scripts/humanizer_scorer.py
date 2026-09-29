#!/usr/bin/env python3
"""Humanity score for a piece of text: 0-100 with breakdown by signal type.

Signal types follow the Mode 1 categories in SKILL.md:
  filler_words, hedging, em_dash_density, sentence_uniformity,
  vagueness, false_certainty, formulaic_conclusion

Usage:
    python scripts/humanizer_scorer.py <file>
    cat draft.txt | python scripts/humanizer_scorer.py
    python scripts/humanizer_scorer.py --json <file>   # machine-readable output
"""

import re
import sys

# --- Signal definitions (word lists aligned with SKILL.md Mode 1) ---

FILLER_WORDS = re.compile(
    r"\b(delve|delve into|delve deeper|landscape|crucial|vital|pivotal|"
    r"leverage|furthermore|moreover|additionally|navigate|robust|"
    r"comprehensive|holistic|foster|facilitate|ensure)\b",
    re.IGNORECASE,
)

HEDGING = re.compile(
    r"\b(it is important to note that|it is worth mentioning that|"
    r"one could argue that|in many cases|in most scenarios|"
    r"needless to say|it goes without saying|it should be noted)\b",
    re.IGNORECASE,
)

VAGUENESS = re.compile(
    r"\b(many companies|studies show|significantly (improved|increased|reduced)|"
    r"leading brands|a lot|various stakeholders|some experts|industry experts say|"
    r"cutting-edge|state-of-the-art|world-class)\b",
    re.IGNORECASE,
)

FALSE_CERTAINTY = re.compile(
    r"\b(companies that .* are more successful|"
    r"teams that .* (always|invariably|definitely) |"
    r"the best .* is|no one .* can argue)\b",
    re.IGNORECASE,
)

FORMULAIC_CONCLUSION = re.compile(
    r"\b(in this (article|blog post|piece), we (explored|discussed|covered)|"
    r"by implementing these strategies, you can|in conclusion)\b",
    re.IGNORECASE,
)

# --- Scoring weights (max deduction per signal type) ---

WEIGHTS = {
    "filler_words": 25,
    "hedging": 20,
    "vagueness": 20,
    "sentence_uniformity": 15,
    "em_dash_density": 10,
    "false_certainty": 5,
    "formulaic_conclusion": 5,
}

EM_DASH_DENSITY_LIMIT = 0.2  # em-dashes per paragraph above this starts deducting


def _sentences(text: str) -> list[str]:
    # Split on sentence-ending punctuation, keep short pieces as fragments
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if len(p.strip()) > 1]


def _sentence_uniformity(text: str) -> float:
    """Deduction 0..15 based on how uniform sentence lengths are."""
    sents = _sentences(text)
    if len(sents) < 5:
        return 0.0
    lengths = [len(s.split()) for s in sents]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return 0.0
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    cv = variance ** 0.5 / mean  # coefficient of variation
    if cv < 0.15:
        return 15.0  # extremely uniform
    if cv < 0.25:
        return 8.0
    if cv < 0.35:
        return 3.0
    return 0.0


def _em_dash_density(text: str) -> float:
    """Deduction 0..10 based on em-dash density per paragraph."""
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return 0.0
    total = 0.0
    for para in paragraphs:
        dashes = para.count("—") + para.count("--")
        total += max(0.0, dashes - EM_DASH_DENSITY_LIMIT) * 2.0
    return min(10.0, total / len(paragraphs) * 4.0)


def score(text: str) -> dict:
    """Return breakdown dict: {signal: deduction, ...}, 'score', 'counts'."""
    text = text.strip()
    if not text:
        return {"score": 0, "counts": {}, "breakdown": {"empty input": 100}}

    counts = {
        "filler_words": len(FILLER_WORDS.findall(text)),
        "hedging": len(HEDGING.findall(text)),
        "vagueness": len(VAGUENESS.findall(text)),
        "false_certainty": len(FALSE_CERTAINTY.findall(text)),
        "formulaic_conclusion": len(FORMULAIC_CONCLUSION.findall(text)),
        "em_dashes": text.count("—"),
        "sentences": len(_sentences(text)),
    }

    # Cap deductions so a single category can't zero the score on its own
    deductions = {
        "filler_words": min(WEIGHTS["filler_words"], counts["filler_words"] * 3.5),
        "hedging": min(WEIGHTS["hedging"], counts["hedging"] * 5.0),
        "vagueness": min(WEIGHTS["vagueness"], counts["vagueness"] * 6.0),
        "sentence_uniformity": _sentence_uniformity(text),
        "em_dash_density": _em_dash_density(text),
        "false_certainty": min(WEIGHTS["false_certainty"], counts["false_certainty"] * 5.0),
        "formulaic_conclusion": min(WEIGHTS["formulaic_conclusion"], counts["formulaic_conclusion"] * 5.0),
    }

    score = max(0, round(100 - sum(deductions.values())))
    return {"score": score, "counts": counts, "breakdown": {k: round(v, 1) for k, v in deductions.items()}}


def _read_input(argv: list[str]) -> str:
    path = None
    for arg in argv:
        if arg != "--json" and not arg.startswith("-"):
            path = arg
            break
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def main() -> int:
    as_json = "--json" in sys.argv[1:]
    text = _read_input(sys.argv[1:])
    result = score(text)

    if as_json:
        import json

        print(json.dumps(result, indent=2))
        return 0

    print(f"Humanity score: {result['score']}/100")
    print("Breakdown by signal type (deduction from 100):")
    for signal, deduction in sorted(result["breakdown"].items(), key=lambda kv: -kv[1]):
        print(f"  {signal:<22} -{deduction:>5.1f}")
    print("Counts:")
    for name, count in sorted(result["counts"].items()):
        print(f"  {name:<22} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
