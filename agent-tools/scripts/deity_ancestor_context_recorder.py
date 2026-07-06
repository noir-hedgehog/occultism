#!/usr/bin/env python3
"""Record low-risk deity, ancestor, altar, offering, and vow-return context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import deity_ancestor_request_guard


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
    guard = deity_ancestor_request_guard.guard({"request_text": context_text})
    tradition_context = str(payload.get("tradition_context", "")).strip()
    focus_entity = str(payload.get("focus_entity", "")).strip()
    occasion = str(payload.get("occasion", "")).strip()
    user_intention = str(payload.get("user_intention", "")).strip()
    existing_items = normalize_list(payload.get("existing_items", ""))
    offering_or_memorial_actions = normalize_list(payload.get("offering_or_memorial_actions", ""))
    household_boundaries = str(payload.get("household_boundaries", "")).strip()
    safety_context = str(payload.get("safety_context", "")).strip()
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "cultural_memorial_reflection")).strip() or "cultural_memorial_reflection"
    missing_fields = []
    for key, value in (
        ("tradition_context", tradition_context),
        ("focus_entity", focus_entity),
        ("occasion", occasion),
        ("user_intention", user_intention),
        ("household_boundaries", household_boundaries),
        ("safety_context", safety_context),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not offering_or_memorial_actions:
        missing_fields.append("offering_or_memorial_actions")
    return {
        "tool": "deity_ancestor_context_recorder",
        "system": "deity_ancestor_symbolic_consultation",
        "is_valid": bool(guard["can_continue_deity_ancestor"]),
        "can_continue_deity_ancestor": bool(guard["can_continue_deity_ancestor"]),
        "context_text": context_text,
        "tradition_context": tradition_context,
        "focus_entity": focus_entity,
        "occasion": occasion,
        "user_intention": user_intention,
        "existing_items": existing_items,
        "offering_or_memorial_actions": offering_or_memorial_actions,
        "household_boundaries": household_boundaries,
        "safety_context": safety_context,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_deity_ancestor_symbols",
            "build_deity_ancestor_reflection_plan",
            "separate_cultural_memorial_practice_from_commands_or_fear",
        ] if guard["can_continue_deity_ancestor"] else ["pause_deity_ancestor_consultation", "reframe_to_cultural_memorial_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "tradition_context", "focus_entity", "occasion", "user_intention", "existing_items", "offering_or_memorial_actions", "household_boundaries", "safety_context", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Deity or ancestor context notes.")
    parser.add_argument("--tradition-context", help="Tradition, family, or source context.")
    parser.add_argument("--focus-entity", help="Deity, ancestor, altar, or memorial focus.")
    parser.add_argument("--occasion", help="Occasion.")
    parser.add_argument("--user-intention", help="User intention.")
    parser.add_argument("--existing-items", help="Existing items.")
    parser.add_argument("--offering-or-memorial-actions", help="Offering or memorial actions.")
    parser.add_argument("--household-boundaries", help="Household consent and boundary notes.")
    parser.add_argument("--safety-context", help="Fire, food, child, pet, and practical safety context.")
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
