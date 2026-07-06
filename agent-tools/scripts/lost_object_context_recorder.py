#!/usr/bin/env python3
"""Record low-risk lost-object search context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import lost_object_request_guard


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
    guard = lost_object_request_guard.guard({"request_text": context_text})
    item_description = str(payload.get("item_description", "")).strip()
    last_seen = str(payload.get("last_seen", "")).strip()
    route_context = str(payload.get("route_context", "")).strip()
    possible_areas = normalize_list(payload.get("possible_areas", ""))
    checked_areas = normalize_list(payload.get("checked_areas", ""))
    contact_channels = normalize_list(payload.get("contact_channels", ""))
    practical_actions = normalize_list(payload.get("practical_actions", ""))
    risk_notes = str(payload.get("risk_notes", "")).strip()
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "memory_search_reflection")).strip() or "memory_search_reflection"
    missing_fields = []
    for key, value in (
        ("item_description", item_description),
        ("last_seen", last_seen),
        ("route_context", route_context),
        ("risk_notes", risk_notes),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not possible_areas:
        missing_fields.append("possible_areas")
    if not checked_areas:
        missing_fields.append("checked_areas")
    if not contact_channels:
        missing_fields.append("contact_channels")
    if not practical_actions:
        missing_fields.append("practical_actions")
    return {
        "tool": "lost_object_context_recorder",
        "system": "lost_object_symbolic_consultation",
        "is_valid": bool(guard["can_continue_lost_object"]),
        "can_continue_lost_object": bool(guard["can_continue_lost_object"]),
        "context_text": context_text,
        "item_description": item_description,
        "last_seen": last_seen,
        "route_context": route_context,
        "possible_areas": possible_areas,
        "checked_areas": checked_areas,
        "contact_channels": contact_channels,
        "practical_actions": practical_actions,
        "risk_notes": risk_notes,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_lost_object_symbols",
            "build_lost_object_search_plan",
            "separate_symbolic_direction_from_real_world_search",
        ] if guard["can_continue_lost_object"] else ["pause_lost_object_consultation", "reframe_to_real_world_search_or_safety_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "item_description", "last_seen", "route_context", "possible_areas", "checked_areas", "contact_channels", "practical_actions", "risk_notes", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Lost-object notes.")
    parser.add_argument("--item-description", help="Lost item description.")
    parser.add_argument("--last-seen", help="Last seen time/place.")
    parser.add_argument("--route-context", help="Route context.")
    parser.add_argument("--possible-areas", help="Possible areas.")
    parser.add_argument("--checked-areas", help="Already checked areas.")
    parser.add_argument("--contact-channels", help="Contact channels.")
    parser.add_argument("--practical-actions", help="Practical actions.")
    parser.add_argument("--risk-notes", help="Risk notes.")
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
