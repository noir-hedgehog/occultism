#!/usr/bin/env python3
"""Record a low-risk incense, ash, or smoke-symbol observation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import incense_request_guard


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
    guard = incense_request_guard.guard({"request_text": question})
    observation_source = str(payload.get("observation_source", "user_described")).strip() or "user_described"
    observation_state = str(payload.get("observation_state", "already_extinguished")).strip() or "already_extinguished"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    ash_shapes = normalize_list(payload.get("ash_shapes", ""))
    smoke_notes = normalize_list(payload.get("smoke_notes", ""))
    ember_notes = normalize_list(payload.get("ember_notes", ""))
    description = str(payload.get("description", payload.get("observation_description", ""))).strip()
    if not ash_shapes and not smoke_notes and not ember_notes and description:
        ash_shapes = normalize_list(description)
    missing_fields = []
    if not ash_shapes and not smoke_notes and not ember_notes and not description:
        missing_fields.append("observation_notes")
    if observation_state not in {"already_extinguished", "photo_notes", "electric_incense", "outdoor_safe_distance", "unknown"}:
        missing_fields.append("safe_observation_state")
    return {
        "tool": "incense_observation_recorder",
        "system": "incense_symbolic_reflection",
        "is_valid": bool(guard["can_continue_incense"]),
        "can_continue_incense": bool(guard["can_continue_incense"]),
        "question_text": question,
        "observation_source": observation_source,
        "observation_state": observation_state,
        "focus": focus,
        "ash_shapes": ash_shapes,
        "smoke_notes": smoke_notes,
        "ember_notes": ember_notes,
        "observation_description": description,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_incense_symbols",
            "build_incense_interpretation_plan",
            "keep_fire_and_smoke_safety_limits_visible",
        ] if guard["can_continue_incense"] else ["pause_incense_consultation", "reframe_to_fire_safety_or_real_world_support"],
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
    if args.observation_source:
        payload["observation_source"] = args.observation_source
    if args.observation_state:
        payload["observation_state"] = args.observation_state
    if args.ash_shapes:
        payload["ash_shapes"] = args.ash_shapes
    if args.smoke_notes:
        payload["smoke_notes"] = args.smoke_notes
    if args.ember_notes:
        payload["ember_notes"] = args.ember_notes
    if args.description:
        payload["description"] = args.description
    if args.focus:
        payload["focus"] = args.focus
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
    parser.add_argument("--text", help="Incense observation question or notes.")
    parser.add_argument("--observation-source", help="user_described, image_notes, electric_incense, external_app.")
    parser.add_argument("--observation-state", help="already_extinguished, photo_notes, electric_incense, outdoor_safe_distance, unknown.")
    parser.add_argument("--ash-shapes", help="Observed ash shapes, e.g. tower curl bridge.")
    parser.add_argument("--smoke-notes", help="Observed smoke notes, e.g. straight smoke, drifting smoke.")
    parser.add_argument("--ember-notes", help="Observed ember or incense-tip notes.")
    parser.add_argument("--description", help="Free-text observation description.")
    parser.add_argument("--focus", help="Consultation focus.")
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
