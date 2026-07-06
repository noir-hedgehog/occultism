#!/usr/bin/env python3
"""Record a low-risk body omen symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import body_omen_request_guard


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
    guard = body_omen_request_guard.guard({"request_text": question})
    omen_type = str(payload.get("omen_type", payload.get("body_signal", ""))).strip()
    body_location = str(payload.get("body_location", payload.get("location", ""))).strip()
    timing = str(payload.get("timing", payload.get("time_context", ""))).strip()
    duration = str(payload.get("duration", payload.get("frequency", ""))).strip()
    sensation_notes = normalize_list(payload.get("sensation_notes", payload.get("sensations", "")))
    health_context = normalize_list(payload.get("health_context", payload.get("medical_context", "")))
    mundane_context = normalize_list(payload.get("mundane_context", payload.get("daily_context", "")))
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    stop_condition = str(payload.get("stop_condition", payload.get("stop", ""))).strip()
    missing_fields = []
    if not omen_type:
        missing_fields.append("omen_type")
    if not body_location:
        missing_fields.append("body_location")
    if not timing:
        missing_fields.append("timing")
    if not sensation_notes:
        missing_fields.append("sensation_notes")
    return {
        "tool": "body_omen_context_recorder",
        "system": "body_omen_symbolic_reflection",
        "is_valid": bool(guard["can_continue_body_omen"]),
        "can_continue_body_omen": bool(guard["can_continue_body_omen"]),
        "question_text": question,
        "omen_type": omen_type,
        "body_location": body_location,
        "timing": timing,
        "duration": duration,
        "sensation_notes": sensation_notes,
        "health_context": health_context,
        "mundane_context": mundane_context,
        "focus": focus,
        "reality_constraints": reality_constraints,
        "stop_condition": stop_condition,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_body_omen_symbols",
            "build_body_omen_reflection_plan",
            "keep_body_care_and_medical_boundary_visible",
        ] if guard["can_continue_body_omen"] else ["pause_body_omen_consultation", "reframe_to_medical_or_safety_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "omen_type", "body_location", "timing", "duration", "sensation_notes", "health_context", "mundane_context", "focus", "stop_condition"):
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
    parser.add_argument("--text", help="Body omen request or context notes.")
    parser.add_argument("--omen-type", help="Signal type, e.g. eye twitch, sneeze, ear heat.")
    parser.add_argument("--body-location", help="Body location, e.g. left eye, right ear.")
    parser.add_argument("--timing", help="Time, date, or event context.")
    parser.add_argument("--duration", help="Duration or frequency.")
    parser.add_argument("--sensation-notes", help="Comma-separated sensation notes.")
    parser.add_argument("--health-context", help="Health and medical boundary notes.")
    parser.add_argument("--mundane-context", help="Sleep, screen, caffeine, stress, weather, or other ordinary context.")
    parser.add_argument("--focus", help="Reflection focus.")
    parser.add_argument("--stop-condition", help="Stop condition.")
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
