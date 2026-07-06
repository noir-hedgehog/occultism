#!/usr/bin/env python3
"""Record low-risk sleep-paralysis, nightmare, and night-fear context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sleep_paralysis_request_guard


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
    guard = sleep_paralysis_request_guard.guard({"request_text": context_text})
    episode_pattern = str(payload.get("episode_pattern", "")).strip()
    wake_state = str(payload.get("wake_state", "")).strip()
    body_sensations = normalize_list(payload.get("body_sensations", ""))
    perceived_images = normalize_list(payload.get("perceived_images", ""))
    room_context = str(payload.get("room_context", "")).strip()
    recent_stressors = normalize_list(payload.get("recent_stressors", ""))
    sleep_context = str(payload.get("sleep_context", "")).strip()
    grounding_actions = normalize_list(payload.get("grounding_actions", ""))
    daytime_impact = str(payload.get("daytime_impact", "")).strip()
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "sleep_grounding_reflection")).strip() or "sleep_grounding_reflection"
    missing_fields = []
    for key, value in (
        ("episode_pattern", episode_pattern),
        ("wake_state", wake_state),
        ("room_context", room_context),
        ("sleep_context", sleep_context),
        ("daytime_impact", daytime_impact),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not body_sensations:
        missing_fields.append("body_sensations")
    if not grounding_actions:
        missing_fields.append("grounding_actions")
    return {
        "tool": "sleep_paralysis_context_recorder",
        "system": "sleep_paralysis_symbolic_consultation",
        "is_valid": bool(guard["can_continue_sleep_paralysis"]),
        "can_continue_sleep_paralysis": bool(guard["can_continue_sleep_paralysis"]),
        "context_text": context_text,
        "episode_pattern": episode_pattern,
        "wake_state": wake_state,
        "body_sensations": body_sensations,
        "perceived_images": perceived_images,
        "room_context": room_context,
        "recent_stressors": recent_stressors,
        "sleep_context": sleep_context,
        "grounding_actions": grounding_actions,
        "daytime_impact": daytime_impact,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_sleep_paralysis_symbols",
            "build_sleep_paralysis_reflection_plan",
            "separate_sleep_experience_from_spirit_fact_claims",
        ] if guard["can_continue_sleep_paralysis"] else ["pause_sleep_paralysis_consultation", "reframe_to_sleep_safety_grounding_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "episode_pattern", "wake_state", "body_sensations", "perceived_images", "room_context", "recent_stressors", "sleep_context", "grounding_actions", "daytime_impact", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Sleep paralysis or night fear notes.")
    parser.add_argument("--episode-pattern", help="Episode timing or pattern.")
    parser.add_argument("--wake-state", help="Waking state.")
    parser.add_argument("--body-sensations", help="Body sensations.")
    parser.add_argument("--perceived-images", help="Images or perceptions.")
    parser.add_argument("--room-context", help="Room and environment context.")
    parser.add_argument("--recent-stressors", help="Recent stressors.")
    parser.add_argument("--sleep-context", help="Sleep timing, fatigue, and routine context.")
    parser.add_argument("--grounding-actions", help="Grounding or safety actions.")
    parser.add_argument("--daytime-impact", help="Daytime impact.")
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
