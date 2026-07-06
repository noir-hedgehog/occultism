#!/usr/bin/env python3
"""Record low-risk pet communication and care-observation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import pet_communication_request_guard


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
    guard = pet_communication_request_guard.guard({"request_text": context_text})
    pet_type = str(payload.get("pet_type", "")).strip()
    relationship = str(payload.get("relationship", "")).strip()
    observations = normalize_list(payload.get("observations", ""))
    time_context = str(payload.get("time_context", "")).strip()
    health_context = str(payload.get("health_context", "")).strip()
    emotions = normalize_list(payload.get("emotions", ""))
    care_actions = normalize_list(payload.get("care_actions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    focus = str(payload.get("focus", "pet_care_reflection")).strip() or "pet_care_reflection"
    missing_fields = []
    if not pet_type:
        missing_fields.append("pet_type")
    if not observations:
        missing_fields.append("observations")
    if not time_context:
        missing_fields.append("time_context")
    if not health_context:
        missing_fields.append("health_context_or_vet_boundary")
    if not care_actions:
        missing_fields.append("care_actions")
    return {
        "tool": "pet_communication_context_recorder",
        "system": "pet_communication_symbolic_consultation",
        "is_valid": bool(guard["can_continue_pet_communication"]),
        "can_continue_pet_communication": bool(guard["can_continue_pet_communication"]),
        "context_text": context_text,
        "pet_type": pet_type,
        "relationship": relationship,
        "observations": observations,
        "time_context": time_context,
        "health_context": health_context,
        "emotions": emotions,
        "care_actions": care_actions,
        "reality_anchor": reality_anchor,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_pet_communication_symbols",
            "build_pet_communication_reflection_plan",
            "separate_symbolic_message_from_veterinary_or_factual_claims",
        ] if guard["can_continue_pet_communication"] else ["pause_pet_communication_consultation", "reframe_to_veterinary_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "pet_type", "relationship", "observations", "time_context", "health_context", "emotions", "care_actions", "reality_anchor", "focus"):
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
    parser.add_argument("--text", help="Pet communication notes.")
    parser.add_argument("--pet-type", help="Pet type.")
    parser.add_argument("--relationship", help="Relationship to pet.")
    parser.add_argument("--observations", help="Observed behavior.")
    parser.add_argument("--time-context", help="Time and situation.")
    parser.add_argument("--health-context", help="Vet or health boundary.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--care-actions", help="Practical care actions.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
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
