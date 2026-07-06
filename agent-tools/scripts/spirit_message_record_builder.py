#!/usr/bin/env python3
"""Record low-risk spirit-message/higher-self symbolic context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import spirit_message_request_guard


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
    message_text = str(payload.get("message_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not message_text:
        raise ValueError("message_text, request_text, or text is required")
    guard = spirit_message_request_guard.guard({"request_text": message_text})
    sources = normalize_list(payload.get("sources", payload.get("source", "")))
    phrases = normalize_list(payload.get("phrases", ""))
    symbols = normalize_list(payload.get("symbols", ""))
    emotions = normalize_list(payload.get("emotions", ""))
    reality_anchor = str(payload.get("reality_anchor", "")).strip()
    consent_notes = str(payload.get("consent_notes", "")).strip()
    focus = str(payload.get("focus", "inner_dialogue_reflection")).strip() or "inner_dialogue_reflection"
    missing_fields = []
    if not sources:
        missing_fields.append("sources")
    if not phrases and not symbols and not emotions:
        missing_fields.append("phrases_symbols_or_emotions")
    return {
        "tool": "spirit_message_record_builder",
        "system": "spirit_message_symbolic_consultation",
        "is_valid": bool(guard["can_continue_spirit_message"]),
        "can_continue_spirit_message": bool(guard["can_continue_spirit_message"]),
        "message_text": message_text,
        "sources": sources,
        "phrases": phrases,
        "symbols": symbols,
        "emotions": emotions,
        "reality_anchor": reality_anchor,
        "consent_notes": consent_notes,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_spirit_message_symbols",
            "build_spirit_message_reflection_plan",
            "separate_symbolic_message_from_fact_or_command",
        ] if guard["can_continue_spirit_message"] else ["pause_spirit_message_consultation", "reframe_to_safety_or_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "sources", "phrases", "symbols", "emotions", "reality_anchor", "consent_notes", "focus"):
        value = getattr(args, key)
        if value:
            payload["message_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"message_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Spirit-message notes.")
    parser.add_argument("--sources", help="Dream, journaling, meditation, oracle card, etc.")
    parser.add_argument("--phrases", help="Message phrases.")
    parser.add_argument("--symbols", help="Message symbols.")
    parser.add_argument("--emotions", help="Emotions or tones.")
    parser.add_argument("--reality-anchor", help="Current-life practical anchor.")
    parser.add_argument("--consent-notes", help="Consent/privacy notes.")
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
