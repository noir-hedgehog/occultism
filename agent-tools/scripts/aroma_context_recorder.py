#!/usr/bin/env python3
"""Record a low-risk aroma and scent symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import aroma_request_guard


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
    guard = aroma_request_guard.guard({"request_text": question})
    scent_items = normalize_list(payload.get("scent_items", payload.get("oils", payload.get("scents", ""))))
    scent_source = str(payload.get("scent_source", payload.get("source", "user_provided_or_existing_item"))).strip() or "user_provided_or_existing_item"
    use_mode = str(payload.get("use_mode", payload.get("method", "non_contact_symbolic_reminder"))).strip() or "non_contact_symbolic_reminder"
    space = str(payload.get("space", payload.get("location", ""))).strip()
    duration = str(payload.get("duration", payload.get("time_limit", ""))).strip()
    ventilation = str(payload.get("ventilation", "")).strip()
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    safety_context = normalize_list(payload.get("safety_context", payload.get("safety_notes", "")))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    notes = str(payload.get("notes", payload.get("context_notes", ""))).strip()
    missing_fields = []
    if not scent_items:
        missing_fields.append("scent_items")
    if not use_mode:
        missing_fields.append("use_mode")
    if not focus:
        missing_fields.append("focus")
    return {
        "tool": "aroma_context_recorder",
        "system": "aroma_scent_symbolic_reflection",
        "is_valid": bool(guard["can_continue_aroma"]),
        "can_continue_aroma": bool(guard["can_continue_aroma"]),
        "question_text": question,
        "scent_items": scent_items,
        "scent_source": scent_source,
        "use_mode": use_mode,
        "space": space,
        "duration": duration,
        "ventilation": ventilation,
        "focus": focus,
        "safety_context": safety_context,
        "reality_constraints": reality_constraints,
        "context_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_aroma_symbols",
            "build_aroma_practice_plan",
            "keep_safety_context_visible",
        ] if guard["can_continue_aroma"] else ["pause_aroma_consultation", "reframe_to_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "scent_items", "scent_source", "use_mode", "space", "duration", "ventilation", "focus"):
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
    parser.add_argument("--text", help="Aroma request or context notes.")
    parser.add_argument("--scent-items", help="Comma-separated scents, oils, or aromatic items.")
    parser.add_argument("--scent-source", help="Existing item, gift, shop sample, recipe, etc.")
    parser.add_argument("--use-mode", help="Diffuser, smelling strip, sachet, non-contact reminder, etc.")
    parser.add_argument("--space", help="Space or location.")
    parser.add_argument("--duration", help="Short time box or stop condition.")
    parser.add_argument("--ventilation", help="Ventilation note.")
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
