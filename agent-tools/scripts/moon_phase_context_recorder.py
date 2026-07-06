#!/usr/bin/env python3
"""Record low-risk moon-phase/lunar-cycle reflection context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import moon_phase_request_guard


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
    context_text = str(payload.get("context_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not context_text:
        raise ValueError("context_text, request_text, or text is required")
    guard = moon_phase_request_guard.guard({"request_text": context_text})
    phases = normalize_list(payload.get("phases", payload.get("moon_phases", "")))
    themes = normalize_list(payload.get("themes", ""))
    intentions = normalize_list(payload.get("intentions", ""))
    constraints = normalize_list(payload.get("practical_constraints", payload.get("constraints", "")))
    date_note = str(payload.get("date_note", "")).strip()
    source_note = str(payload.get("source_note", "")).strip()
    focus = str(payload.get("focus", "cycle_reflection")).strip() or "cycle_reflection"
    missing_fields = []
    if not phases and not themes and not intentions:
        missing_fields.append("phases_themes_or_intentions")
    if not source_note:
        missing_fields.append("source_note")
    return {
        "tool": "moon_phase_context_recorder",
        "system": "moon_phase_symbolic_consultation",
        "is_valid": bool(guard["can_continue_moon_phase"]),
        "can_continue_moon_phase": bool(guard["can_continue_moon_phase"]),
        "context_text": context_text,
        "phases": phases,
        "themes": themes,
        "intentions": intentions,
        "practical_constraints": constraints,
        "date_note": date_note,
        "source_note": source_note,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_moon_phase_symbols",
            "build_moon_phase_reflection_plan",
            "keep_source_and_real_world_constraints_visible",
        ] if guard["can_continue_moon_phase"] else ["pause_moon_phase_consultation", "reframe_to_real_world_support_or_safe_reflection"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "phases", "themes", "intentions", "practical_constraints", "date_note", "source_note", "focus"):
        value = getattr(args, key)
        if value:
            payload["context_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"context_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Moon-phase/lunar-cycle context notes.")
    parser.add_argument("--phases", help="Moon phases, such as 新月, 满月, 上弦月.")
    parser.add_argument("--themes", help="Reflection themes.")
    parser.add_argument("--intentions", help="Intentions or review items.")
    parser.add_argument("--practical-constraints", help="Real-world constraints.")
    parser.add_argument("--date-note", help="Date/time note.")
    parser.add_argument("--source-note", help="Calendar, app, or user-provided source note.")
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
