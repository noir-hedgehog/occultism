#!/usr/bin/env python3
"""Record low-risk animal-omen observations before symbolic interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import animal_omen_request_guard


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
    observation_text = str(payload.get("observation_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not observation_text:
        raise ValueError("observation_text, request_text, or text is required")
    guard = animal_omen_request_guard.guard({"request_text": observation_text})
    animals = normalize_list(payload.get("animals", payload.get("animal", "")))
    behavior = str(payload.get("behavior", "")).strip()
    location = str(payload.get("location", "")).strip()
    timing = str(payload.get("timing", "")).strip()
    frequency = str(payload.get("frequency", "single_observation")).strip() or "single_observation"
    source = str(payload.get("source", "user_observed")).strip() or "user_observed"
    safety_context = str(payload.get("safety_context", "")).strip()
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    missing_fields = []
    if not animals:
        missing_fields.append("animals")
    if not behavior:
        missing_fields.append("behavior")
    if not location:
        missing_fields.append("location")
    return {
        "tool": "animal_omen_observation_recorder",
        "system": "animal_omen_symbolic_consultation",
        "is_valid": bool(guard["can_continue_animal_omen"]),
        "can_continue_animal_omen": bool(guard["can_continue_animal_omen"]),
        "observation_text": observation_text,
        "animals": animals,
        "behavior": behavior,
        "location": location,
        "timing": timing,
        "frequency": frequency,
        "source": source,
        "safety_context": safety_context,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_animal_omen_symbols",
            "build_animal_omen_interpretation_plan",
            "keep_real_world_safety_visible",
        ] if guard["can_continue_animal_omen"] else ["pause_animal_omen_consultation", "reframe_to_real_world_safety"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "animals", "behavior", "location", "timing", "frequency", "source", "safety_context", "focus"):
        value = getattr(args, key)
        if value:
            payload["observation_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"observation_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Animal observation or omen request notes.")
    parser.add_argument("--animals", help="Animal names.")
    parser.add_argument("--behavior", help="Observed behavior.")
    parser.add_argument("--location", help="Observed location.")
    parser.add_argument("--timing", help="Observed timing.")
    parser.add_argument("--frequency", help="single_observation, repeated, seasonal, unknown, etc.")
    parser.add_argument("--source", help="user_observed, photo_notes, family_story, cultural_learning, etc.")
    parser.add_argument("--safety-context", help="Bite, pest, injured animal, wildlife, building, pet, or other safety notes.")
    parser.add_argument("--focus", help="Optional reflection focus.")
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
