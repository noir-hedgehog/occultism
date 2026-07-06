#!/usr/bin/env python3
"""Record low-risk evil-eye, energy-protection, and cord-cutting context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import spiritual_protection_request_guard


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
    guard = spiritual_protection_request_guard.guard({"request_text": context_text})
    protection_focus = str(payload.get("protection_focus", "")).strip()
    trigger_context = str(payload.get("trigger_context", "")).strip()
    sensations = normalize_list(payload.get("sensations", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    reality_safety_context = str(payload.get("reality_safety_context", "")).strip()
    boundary_actions = normalize_list(payload.get("boundary_actions", ""))
    symbolic_items = normalize_list(payload.get("symbolic_items", ""))
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "boundary_reflection")).strip() or "boundary_reflection"
    missing_fields = []
    if not protection_focus:
        missing_fields.append("protection_focus")
    if not trigger_context:
        missing_fields.append("trigger_context")
    if not reality_safety_context:
        missing_fields.append("reality_safety_context")
    if not boundary_actions:
        missing_fields.append("boundary_actions")
    if not review_time:
        missing_fields.append("review_time")
    if not stop_condition:
        missing_fields.append("stop_condition")
    return {
        "tool": "spiritual_protection_context_recorder",
        "system": "spiritual_protection_symbolic_consultation",
        "is_valid": bool(guard["can_continue_spiritual_protection"]),
        "can_continue_spiritual_protection": bool(guard["can_continue_spiritual_protection"]),
        "context_text": context_text,
        "protection_focus": protection_focus,
        "trigger_context": trigger_context,
        "sensations": sensations,
        "emotions": emotions,
        "reality_safety_context": reality_safety_context,
        "boundary_actions": boundary_actions,
        "symbolic_items": symbolic_items,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_spiritual_protection_symbols",
            "build_spiritual_protection_reflection_plan",
            "separate_symbolic_protection_from_blame_or_retaliation",
        ] if guard["can_continue_spiritual_protection"] else ["pause_spiritual_protection_consultation", "reframe_to_boundary_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "protection_focus", "trigger_context", "sensations", "emotions", "reality_safety_context", "boundary_actions", "symbolic_items", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Spiritual protection notes.")
    parser.add_argument("--protection-focus", help="Protection or cord-cutting focus.")
    parser.add_argument("--trigger-context", help="Triggering situation.")
    parser.add_argument("--sensations", help="Body or energy sensations.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--reality-safety-context", help="Reality safety context.")
    parser.add_argument("--boundary-actions", help="Practical boundary actions.")
    parser.add_argument("--symbolic-items", help="Symbolic items or reminders.")
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
