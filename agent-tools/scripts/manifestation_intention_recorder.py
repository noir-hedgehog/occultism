#!/usr/bin/env python3
"""Record low-risk manifestation intention context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import manifestation_request_guard


def normalize_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|", "；", ";", "+", "和"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    intention_text = str(payload.get("intention_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not intention_text:
        raise ValueError("intention_text, request_text, or text is required")
    guard = manifestation_request_guard.guard({"request_text": intention_text})
    wish_theme = str(payload.get("wish_theme", "")).strip()
    intention_statement = str(payload.get("intention_statement", "")).strip()
    symbols = normalize_list(payload.get("symbols", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    controllable_actions = normalize_list(payload.get("controllable_actions", ""))
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "grounded_intention_planning")).strip() or "grounded_intention_planning"
    missing_fields = []
    if not wish_theme:
        missing_fields.append("wish_theme")
    if not intention_statement:
        missing_fields.append("intention_statement")
    if not reality_anchor:
        missing_fields.append("reality_anchor")
    if not controllable_actions:
        missing_fields.append("controllable_actions")
    if not review_time:
        missing_fields.append("review_time")
    if not stop_condition:
        missing_fields.append("stop_condition")
    return {
        "tool": "manifestation_intention_recorder",
        "system": "manifestation_symbolic_consultation",
        "is_valid": bool(guard["can_continue_manifestation"]),
        "can_continue_manifestation": bool(guard["can_continue_manifestation"]),
        "intention_text": intention_text,
        "wish_theme": wish_theme,
        "intention_statement": intention_statement,
        "symbols": symbols,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "controllable_actions": controllable_actions,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_manifestation_symbols",
            "build_manifestation_reflection_plan",
            "separate_wish_from_guaranteed_result",
        ] if guard["can_continue_manifestation"] else ["pause_manifestation_consultation", "reframe_to_grounded_action_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "wish_theme", "intention_statement", "symbols", "emotions", "reality_anchor", "controllable_actions", "review_time", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["intention_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Manifestation intention notes.")
    parser.add_argument("--wish-theme", help="Wish theme.")
    parser.add_argument("--intention-statement", help="Grounded intention statement.")
    parser.add_argument("--symbols", help="Symbols or objects.")
    parser.add_argument("--emotions", help="Emotions.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--controllable-actions", help="Controllable actions.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stop condition.")
    parser.add_argument("--focus", help="Optional focus.")
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
