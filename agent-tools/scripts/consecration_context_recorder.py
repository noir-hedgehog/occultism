#!/usr/bin/env python3
"""Record low-risk consecration, blessing, and object-cleansing context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import consecration_request_guard


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
    guard = consecration_request_guard.guard({"request_text": context_text})
    object_focus = str(payload.get("object_focus", "")).strip()
    source_context = str(payload.get("source_context", "")).strip()
    current_use = str(payload.get("current_use", "")).strip()
    existing_items = normalize_list(payload.get("existing_items", ""))
    safety_boundaries = str(payload.get("safety_boundaries", "")).strip()
    symbolic_actions = normalize_list(payload.get("symbolic_actions", ""))
    risk_notes = str(payload.get("risk_notes", "")).strip()
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "object_care_reflection")).strip() or "object_care_reflection"
    missing_fields = []
    for key, value in (
        ("object_focus", object_focus),
        ("source_context", source_context),
        ("current_use", current_use),
        ("safety_boundaries", safety_boundaries),
        ("risk_notes", risk_notes),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not existing_items:
        missing_fields.append("existing_items")
    if not symbolic_actions:
        missing_fields.append("symbolic_actions")
    return {
        "tool": "consecration_context_recorder",
        "system": "consecration_symbolic_consultation",
        "is_valid": bool(guard["can_continue_consecration"]),
        "can_continue_consecration": bool(guard["can_continue_consecration"]),
        "context_text": context_text,
        "object_focus": object_focus,
        "source_context": source_context,
        "current_use": current_use,
        "existing_items": existing_items,
        "safety_boundaries": safety_boundaries,
        "symbolic_actions": symbolic_actions,
        "risk_notes": risk_notes,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_consecration_symbols",
            "build_consecration_care_plan",
            "separate_symbolic_object_care_from_supernatural_guarantees",
        ] if guard["can_continue_consecration"] else ["pause_consecration_consultation", "reframe_to_low_risk_object_care_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "object_focus", "source_context", "current_use", "existing_items", "safety_boundaries", "symbolic_actions", "risk_notes", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Consecration notes.")
    parser.add_argument("--object-focus", help="Object or blessing focus.")
    parser.add_argument("--source-context", help="Object source context.")
    parser.add_argument("--current-use", help="Current use.")
    parser.add_argument("--existing-items", help="Existing items.")
    parser.add_argument("--safety-boundaries", help="Safety boundaries.")
    parser.add_argument("--symbolic-actions", help="Symbolic actions.")
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
