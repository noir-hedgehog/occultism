#!/usr/bin/env python3
"""Record a low-risk sigil, seal, or magic-circle symbolism context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import sigil_request_guard


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
    guard = sigil_request_guard.guard({"request_text": question})
    intention_text = str(payload.get("intention_text", payload.get("intention", ""))).strip()
    symbol_elements = normalize_list(payload.get("symbol_elements", payload.get("elements", payload.get("symbols", ""))))
    source_context = str(payload.get("source_context", payload.get("source", "user_created_or_existing_symbol"))).strip() or "user_created_or_existing_symbol"
    medium = str(payload.get("medium", payload.get("material", "paper_or_digital_draft"))).strip() or "paper_or_digital_draft"
    activation_mode = str(payload.get("activation_mode", payload.get("use_mode", "quiet_review_or_visibility_prompt"))).strip() or "quiet_review_or_visibility_prompt"
    display_location = str(payload.get("display_location", payload.get("location", ""))).strip()
    duration = str(payload.get("duration", payload.get("time_limit", ""))).strip()
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    safety_context = normalize_list(payload.get("safety_context", payload.get("safety_notes", "")))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    notes = str(payload.get("notes", payload.get("context_notes", ""))).strip()
    missing_fields = []
    if not intention_text:
        missing_fields.append("intention_text")
    if not symbol_elements:
        missing_fields.append("symbol_elements")
    if not medium:
        missing_fields.append("medium")
    if not focus:
        missing_fields.append("focus")
    return {
        "tool": "sigil_context_recorder",
        "system": "sigil_seal_symbolic_reflection",
        "is_valid": bool(guard["can_continue_sigil"]),
        "can_continue_sigil": bool(guard["can_continue_sigil"]),
        "question_text": question,
        "intention_text": intention_text,
        "symbol_elements": symbol_elements,
        "source_context": source_context,
        "medium": medium,
        "activation_mode": activation_mode,
        "display_location": display_location,
        "duration": duration,
        "focus": focus,
        "safety_context": safety_context,
        "reality_constraints": reality_constraints,
        "context_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_sigil_symbols",
            "build_sigil_practice_plan",
            "keep_safety_context_visible",
        ] if guard["can_continue_sigil"] else ["pause_sigil_consultation", "reframe_to_safety_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "intention_text", "symbol_elements", "source_context", "medium", "activation_mode", "display_location", "duration", "focus"):
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
    parser.add_argument("--text", help="Sigil request or context notes.")
    parser.add_argument("--intention-text", help="Intention statement.")
    parser.add_argument("--symbol-elements", help="Comma-separated symbol parts.")
    parser.add_argument("--source-context", help="User-created, historical motif, book, existing image, etc.")
    parser.add_argument("--medium", help="Paper, digital draft, card, notebook, removable sticker, etc.")
    parser.add_argument("--activation-mode", help="Quiet review, journaling, visibility prompt, archive, etc.")
    parser.add_argument("--display-location", help="Where the symbol is seen or stored.")
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
