#!/usr/bin/env python3
"""Record low-risk sound-cleansing and space-reset context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sound_cleansing_request_guard


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
    guard = sound_cleansing_request_guard.guard({"request_text": context_text})
    space_context = str(payload.get("space_context", "")).strip()
    sound_tools = normalize_list(payload.get("sound_tools", ""))
    practice_intention = str(payload.get("practice_intention", "")).strip()
    volume_duration = str(payload.get("volume_duration", "")).strip()
    safety_boundaries = str(payload.get("safety_boundaries", "")).strip()
    sensory_notes = str(payload.get("sensory_notes", "")).strip()
    grounding_actions = normalize_list(payload.get("grounding_actions", ""))
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "space_reset_reflection")).strip() or "space_reset_reflection"
    missing_fields = []
    for key, value in (
        ("space_context", space_context),
        ("practice_intention", practice_intention),
        ("volume_duration", volume_duration),
        ("safety_boundaries", safety_boundaries),
        ("sensory_notes", sensory_notes),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not sound_tools:
        missing_fields.append("sound_tools")
    if not grounding_actions:
        missing_fields.append("grounding_actions")
    return {
        "tool": "sound_cleansing_context_recorder",
        "system": "sound_cleansing_symbolic_consultation",
        "is_valid": bool(guard["can_continue_sound_cleansing"]),
        "can_continue_sound_cleansing": bool(guard["can_continue_sound_cleansing"]),
        "context_text": context_text,
        "space_context": space_context,
        "sound_tools": sound_tools,
        "practice_intention": practice_intention,
        "volume_duration": volume_duration,
        "safety_boundaries": safety_boundaries,
        "sensory_notes": sensory_notes,
        "grounding_actions": grounding_actions,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_sound_cleansing_symbols",
            "build_sound_cleansing_practice_plan",
            "separate_symbolic_space_reset_from_exorcism_or_medical_claims",
        ] if guard["can_continue_sound_cleansing"] else ["pause_sound_cleansing_consultation", "reframe_to_low_risk_space_reset_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "space_context", "sound_tools", "practice_intention", "volume_duration", "safety_boundaries", "sensory_notes", "grounding_actions", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Sound-cleansing notes.")
    parser.add_argument("--space-context", help="Space and timing context.")
    parser.add_argument("--sound-tools", help="Sound tools or voice practice.")
    parser.add_argument("--practice-intention", help="Practice intention.")
    parser.add_argument("--volume-duration", help="Volume and duration boundaries.")
    parser.add_argument("--safety-boundaries", help="Safety boundaries.")
    parser.add_argument("--sensory-notes", help="Sensory or body notes.")
    parser.add_argument("--grounding-actions", help="Grounding actions.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stopping condition.")
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
