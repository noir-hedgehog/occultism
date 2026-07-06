#!/usr/bin/env python3
"""Record a low-risk herbal and plant magic symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import herbal_request_guard


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
    guard = herbal_request_guard.guard({"request_text": question})
    plant_items = normalize_list(payload.get("plant_items", payload.get("herbs", payload.get("items", ""))))
    plant_source = str(payload.get("plant_source", payload.get("source", "user_provided_or_existing_item"))).strip() or "user_provided_or_existing_item"
    use_mode = str(payload.get("use_mode", payload.get("method", "non_contact_symbolic_reminder"))).strip() or "non_contact_symbolic_reminder"
    container_or_form = str(payload.get("container_or_form", payload.get("form", ""))).strip()
    space = str(payload.get("space", payload.get("location", ""))).strip()
    duration = str(payload.get("duration", payload.get("time_limit", ""))).strip()
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    safety_context = normalize_list(payload.get("safety_context", payload.get("safety_notes", "")))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    notes = str(payload.get("notes", payload.get("context_notes", ""))).strip()
    missing_fields = []
    if not plant_items:
        missing_fields.append("plant_items")
    if not use_mode:
        missing_fields.append("use_mode")
    if not focus:
        missing_fields.append("focus")
    return {
        "tool": "herbal_context_recorder",
        "system": "herbal_plant_magic_symbolic_reflection",
        "is_valid": bool(guard["can_continue_herbal"]),
        "can_continue_herbal": bool(guard["can_continue_herbal"]),
        "question_text": question,
        "plant_items": plant_items,
        "plant_source": plant_source,
        "use_mode": use_mode,
        "container_or_form": container_or_form,
        "space": space,
        "duration": duration,
        "focus": focus,
        "safety_context": safety_context,
        "reality_constraints": reality_constraints,
        "context_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_herbal_symbols",
            "build_herbal_practice_plan",
            "keep_safety_context_visible",
        ] if guard["can_continue_herbal"] else ["pause_herbal_consultation", "reframe_to_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "plant_items", "plant_source", "use_mode", "container_or_form", "space", "duration", "focus"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
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
    parser.add_argument("--text", help="Herbal request or context notes.")
    parser.add_argument("--plant-items", help="Comma-separated herbs, plants, or symbolic items.")
    parser.add_argument("--plant-source", help="Existing item, shop-bought, gift, book list, etc.")
    parser.add_argument("--use-mode", help="Dried bundle, sachet, altar card, journal prompt, non-contact reminder, etc.")
    parser.add_argument("--container-or-form", help="Sachet, jar, dried bundle, card, pressed leaf, etc.")
    parser.add_argument("--space", help="Space or location.")
    parser.add_argument("--duration", help="Short time box or stop condition.")
    parser.add_argument("--focus", help="Reflection focus.")
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
