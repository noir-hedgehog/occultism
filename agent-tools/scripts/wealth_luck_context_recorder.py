#!/usr/bin/env python3
"""Record low-risk wealth-luck and prosperity-symbol context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import wealth_luck_request_guard


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
    guard = wealth_luck_request_guard.guard({"request_text": context_text})
    wealth_focus = str(payload.get("wealth_focus", "")).strip()
    current_context = str(payload.get("current_context", "")).strip()
    income_channels = normalize_list(payload.get("income_channels", ""))
    budget_boundaries = str(payload.get("budget_boundaries", "")).strip()
    existing_symbols = normalize_list(payload.get("existing_symbols", ""))
    practical_actions = normalize_list(payload.get("practical_actions", ""))
    risk_notes = str(payload.get("risk_notes", "")).strip()
    review_time = str(payload.get("review_time", "")).strip()
    stop_condition = str(payload.get("stop_condition", "")).strip()
    focus = str(payload.get("focus", "budget_action_reflection")).strip() or "budget_action_reflection"
    missing_fields = []
    for key, value in (
        ("wealth_focus", wealth_focus),
        ("current_context", current_context),
        ("budget_boundaries", budget_boundaries),
        ("risk_notes", risk_notes),
        ("review_time", review_time),
        ("stop_condition", stop_condition),
    ):
        if not value:
            missing_fields.append(key)
    if not income_channels:
        missing_fields.append("income_channels")
    if not practical_actions:
        missing_fields.append("practical_actions")
    return {
        "tool": "wealth_luck_context_recorder",
        "system": "wealth_luck_symbolic_consultation",
        "is_valid": bool(guard["can_continue_wealth_luck"]),
        "can_continue_wealth_luck": bool(guard["can_continue_wealth_luck"]),
        "context_text": context_text,
        "wealth_focus": wealth_focus,
        "current_context": current_context,
        "income_channels": income_channels,
        "budget_boundaries": budget_boundaries,
        "existing_symbols": existing_symbols,
        "practical_actions": practical_actions,
        "risk_notes": risk_notes,
        "review_time": review_time,
        "stop_condition": stop_condition,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_wealth_luck_symbols",
            "build_wealth_luck_action_plan",
            "separate_symbolic_prosperity_from_financial_advice",
        ] if guard["can_continue_wealth_luck"] else ["pause_wealth_luck_consultation", "reframe_to_budget_action_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "wealth_focus", "current_context", "income_channels", "budget_boundaries", "existing_symbols", "practical_actions", "risk_notes", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Wealth-luck notes.")
    parser.add_argument("--wealth-focus", help="Wealth or prosperity focus.")
    parser.add_argument("--current-context", help="Current money or work context.")
    parser.add_argument("--income-channels", help="Income channels.")
    parser.add_argument("--budget-boundaries", help="Budget boundaries.")
    parser.add_argument("--existing-symbols", help="Existing symbols or reminder items.")
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
