#!/usr/bin/env python3
"""Record a low-risk dowsing rod symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import dowsing_request_guard


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
    question = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not question:
        raise ValueError("question_text, request_text, or text is required")
    guard = dowsing_request_guard.guard({"request_text": question})
    tool_type = str(payload.get("tool_type", payload.get("rod_type", "dowsing_rods_or_symbolic_tool"))).strip() or "dowsing_rods_or_symbolic_tool"
    observation_target = str(payload.get("observation_target", payload.get("target", ""))).strip()
    space_or_map = str(payload.get("space_or_map", payload.get("location", payload.get("map", "")))).strip()
    movement_notes = normalize_list(payload.get("movement_notes", payload.get("movements", "")))
    authorization_context = str(payload.get("authorization_context", payload.get("authorization", "self_authorized_space"))).strip() or "self_authorized_space"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    safety_context = normalize_list(payload.get("safety_context", payload.get("safety_notes", "")))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    duration = str(payload.get("duration", payload.get("time_limit", ""))).strip()
    notes = str(payload.get("notes", payload.get("context_notes", ""))).strip()
    missing_fields = []
    if not observation_target:
        missing_fields.append("observation_target")
    if not space_or_map:
        missing_fields.append("space_or_map")
    if not movement_notes:
        missing_fields.append("movement_notes")
    if not focus:
        missing_fields.append("focus")
    return {
        "tool": "dowsing_context_recorder",
        "system": "dowsing_rod_symbolic_reflection",
        "is_valid": bool(guard["can_continue_dowsing"]),
        "can_continue_dowsing": bool(guard["can_continue_dowsing"]),
        "question_text": question,
        "tool_type": tool_type,
        "observation_target": observation_target,
        "space_or_map": space_or_map,
        "movement_notes": movement_notes,
        "authorization_context": authorization_context,
        "focus": focus,
        "safety_context": safety_context,
        "reality_constraints": reality_constraints,
        "duration": duration,
        "context_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_dowsing_symbols",
            "build_dowsing_practice_plan",
            "keep_authorization_and_safety_visible",
        ] if guard["can_continue_dowsing"] else ["pause_dowsing_consultation", "reframe_to_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "tool_type", "observation_target", "space_or_map", "movement_notes", "authorization_context", "focus", "duration"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
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
    parser.add_argument("--text", help="Dowsing request or context notes.")
    parser.add_argument("--tool-type", help="Tool type, e.g. L-rods, branch, map pointer.")
    parser.add_argument("--observation-target", help="Low-risk target, e.g. desk route reflection.")
    parser.add_argument("--space-or-map", help="Authorized room, desk, garden path, or map.")
    parser.add_argument("--movement-notes", help="Comma-separated movement notes.")
    parser.add_argument("--authorization-context", help="Self-authorized space or permitted context.")
    parser.add_argument("--focus", help="Reflection focus.")
    parser.add_argument("--duration", help="Time box or stop condition.")
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
