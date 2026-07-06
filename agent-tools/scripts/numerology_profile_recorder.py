#!/usr/bin/env python3
"""Record non-sensitive number material for numerology-style consultation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

import numerology_request_guard


DIGIT_RE = re.compile(r"\d")
LONG_NUMBER_RE = re.compile(r"\d{7,}")
ALIASES = {
    "手机号": "phone_suffix",
    "尾号": "phone_suffix",
    "车牌": "license_plate",
    "门牌": "house_number",
    "生日": "birth_date",
    "生命灵数": "life_path",
    "幸运数字": "lucky_number",
}


def detect_context(text: str) -> str:
    for keyword, context in ALIASES.items():
        if keyword in text:
            return context
    return "number_symbol"


def extract_digits(text: str) -> list[str]:
    return DIGIT_RE.findall(text)


def has_sensitive_long_number(text: str) -> bool:
    return bool(LONG_NUMBER_RE.search(text))


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("number_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("number_text, request_text, or text is required")
    guard = numerology_request_guard.guard({"request_text": text})
    digits = list(payload.get("digits", []) or []) or extract_digits(text)
    context = str(payload.get("number_context", "")).strip() or detect_context(text)
    risk_flags = list(guard["risk_flags"])
    if has_sensitive_long_number(text) and "privacy_sensitive_identifier" not in risk_flags:
        risk_flags.append("privacy_sensitive_identifier")
    can_continue = bool(guard["can_continue_numerology"]) and "privacy_sensitive_identifier" not in risk_flags
    missing_fields = []
    if not digits:
        missing_fields.append("digits")
    if len(digits) > 6:
        missing_fields.append("redact_to_suffix_or_selected_digits")
    return {
        "tool": "numerology_profile_recorder",
        "system": "number_symbolism",
        "is_valid": can_continue,
        "can_continue_numerology": can_continue,
        "number_text": text,
        "number_context": context,
        "digits": digits[:6],
        "digit_count": len(digits),
        "risk_flags": risk_flags,
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_digit_symbols",
            "compare_real_world_constraints",
            "build_numerology_interpretation_plan",
        ] if can_continue else ["pause_numerology_reading", "remove_sensitive_identifier_or_reframe"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"number_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"number_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Number material text.")
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
