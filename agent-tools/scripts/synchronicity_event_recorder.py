#!/usr/bin/env python3
"""Record low-risk synchronicity, angel-number, and repeating-sign context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import synchronicity_request_guard


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
    event_text = str(payload.get("event_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not event_text:
        raise ValueError("event_text, request_text, or text is required")
    guard = synchronicity_request_guard.guard({"request_text": event_text})
    repeated_signs = normalize_list(payload.get("repeated_signs", ""))
    frequency_context = str(payload.get("frequency_context", "")).strip()
    situation_context = str(payload.get("situation_context", "")).strip()
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    practical_actions = normalize_list(payload.get("practical_actions", ""))
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "routine_reflection")).strip() or "routine_reflection"
    missing_fields = []
    if not repeated_signs:
        missing_fields.append("repeated_signs")
    if not frequency_context:
        missing_fields.append("frequency_context")
    if not situation_context:
        missing_fields.append("situation_context")
    if not reality_anchor:
        missing_fields.append("reality_anchor")
    if not practical_actions:
        missing_fields.append("practical_actions")
    if not stop_condition:
        missing_fields.append("stop_condition")
    return {
        "tool": "synchronicity_event_recorder",
        "system": "synchronicity_symbolic_consultation",
        "is_valid": bool(guard["can_continue_synchronicity"]),
        "can_continue_synchronicity": bool(guard["can_continue_synchronicity"]),
        "event_text": event_text,
        "repeated_signs": repeated_signs,
        "frequency_context": frequency_context,
        "situation_context": situation_context,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "practical_actions": practical_actions,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_synchronicity_symbols",
            "build_synchronicity_reflection_plan",
            "separate_symbolic_signs_from_commands_or_professional_decisions",
        ] if guard["can_continue_synchronicity"] else ["pause_synchronicity_consultation", "reframe_to_grounded_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "repeated_signs", "frequency_context", "situation_context", "emotions", "reality_anchor", "practical_actions", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["event_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"event_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Synchronicity notes.")
    parser.add_argument("--repeated-signs", help="Repeated signs or motifs.")
    parser.add_argument("--frequency-context", help="Frequency notes.")
    parser.add_argument("--situation-context", help="Situation notes.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--practical-actions", help="Practical actions.")
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
