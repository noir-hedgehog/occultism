#!/usr/bin/env python3
"""Record low-risk flower-language or plant-symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import flower_request_guard


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
    intention = str(payload.get("intention_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not intention:
        raise ValueError("intention_text, request_text, or text is required")
    guard = flower_request_guard.guard({"request_text": intention})
    items = normalize_list(payload.get("flowers", payload.get("items", "")))
    colors = normalize_list(payload.get("colors", ""))
    scene = str(payload.get("scene", "symbolic_reflection")).strip() or "symbolic_reflection"
    recipient = str(payload.get("recipient", "")).strip()
    source = str(payload.get("source", "user_provided")).strip() or "user_provided"
    budget_note = str(payload.get("budget_note", "no_required_purchase")).strip() or "no_required_purchase"
    safety_constraints = str(payload.get("safety_constraints", "")).strip()
    focus = str(payload.get("focus", scene)).strip() or scene
    missing_fields = []
    if not items:
        missing_fields.append("flowers_or_items")
    if not scene:
        missing_fields.append("scene")
    if not budget_note:
        missing_fields.append("budget_note")
    return {
        "tool": "flower_item_recorder",
        "system": "flower_symbolic_consultation",
        "is_valid": bool(guard["can_continue_flower"]),
        "can_continue_flower": bool(guard["can_continue_flower"]),
        "intention_text": intention,
        "flowers": items,
        "colors": colors,
        "scene": scene,
        "recipient": recipient,
        "source": source,
        "budget_note": budget_note,
        "safety_constraints": safety_constraints,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_flower_symbols",
            "build_flower_interpretation_plan",
            "keep_budget_and_safety_constraints_visible",
        ] if guard["can_continue_flower"] else ["pause_flower_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "flowers", "colors", "scene", "recipient", "source", "budget_note", "safety_constraints", "focus"):
        value = getattr(args, key)
        if value:
            payload["intention_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Flower-language intention or request notes.")
    parser.add_argument("--flowers", help="Flower or plant names.")
    parser.add_argument("--colors", help="Flower colors.")
    parser.add_argument("--scene", help="gift, home, desk, reflection, ritualized_journaling, etc.")
    parser.add_argument("--recipient", help="Recipient or audience, if relevant.")
    parser.add_argument("--source", help="user_provided, existing_items, simulated_with_consent, cultural_learning.")
    parser.add_argument("--budget-note", help="Budget or no-purchase note.")
    parser.add_argument("--safety-constraints", help="Allergy, pet, child, scent, venue, or other constraints.")
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
