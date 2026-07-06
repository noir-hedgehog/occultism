#!/usr/bin/env python3
"""Record a low-risk rune casting session."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import rune_request_guard


SPREAD_ALIASES = {
    "单符": "single_rune",
    "一枚": "single_rune",
    "三符": "three_rune",
    "三枚": "three_rune",
    "过去现在未来": "past_present_future",
}

POSITION_HINTS = {
    "single_rune": ["focus"],
    "three_rune": ["context", "challenge", "next_step"],
    "past_present_future": ["past", "present", "future_tendency"],
}


def detect_spread(text: str) -> str:
    for keyword, spread in SPREAD_ALIASES.items():
        if keyword in text:
            return spread
    return "single_rune"


def normalize_runes(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("question_text, request_text, or text is required")
    guard = rune_request_guard.guard({"request_text": text})
    spread = str(payload.get("spread_type", "")).strip() or detect_spread(text)
    runes = normalize_runes(payload.get("runes", payload.get("drawn_runes", "")))
    orientation = str(payload.get("orientation_policy", "upright_only")).strip() or "upright_only"
    source = str(payload.get("source", "user_reported_or_manual_draw")).strip()
    missing_fields = []
    if not runes:
        missing_fields.append("drawn_runes")
    if spread == "three_rune" and len(runes) not in {0, 3}:
        missing_fields.append("three_rune_requires_three_items")
    if spread == "past_present_future" and len(runes) not in {0, 3}:
        missing_fields.append("past_present_future_requires_three_items")
    return {
        "tool": "rune_cast_recorder",
        "system": "rune_divination",
        "is_valid": bool(guard["can_continue_rune"]),
        "can_continue_rune": bool(guard["can_continue_rune"]),
        "question_text": text,
        "spread_type": spread,
        "positions": POSITION_HINTS.get(spread, POSITION_HINTS["single_rune"]),
        "runes": runes,
        "rune_count": len(runes),
        "orientation_policy": orientation,
        "source": source,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_rune_symbols",
            "build_rune_interpretation_plan",
            "compare_real_world_evidence_first",
        ] if guard["can_continue_rune"] else ["pause_rune_reading", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["question_text"] = args.text
    if args.runes:
        payload["runes"] = args.runes
    if args.spread_type:
        payload["spread_type"] = args.spread_type
    if args.orientation_policy:
        payload["orientation_policy"] = args.orientation_policy
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Rune question or session notes.")
    parser.add_argument("--runes", help="Drawn runes separated by space, comma, or Chinese comma.")
    parser.add_argument("--spread-type", help="single_rune, three_rune, or past_present_future.")
    parser.add_argument("--orientation-policy", help="upright_only or user_reported_reversals.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = record(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
