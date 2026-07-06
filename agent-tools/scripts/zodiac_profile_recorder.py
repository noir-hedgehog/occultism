#!/usr/bin/env python3
"""Record a low-risk zodiac or Tai Sui consultation context."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

import zodiac_request_guard


ZODIAC_ALIASES = {
    "鼠": "rat",
    "牛": "ox",
    "虎": "tiger",
    "兔": "rabbit",
    "龙": "dragon",
    "蛇": "snake",
    "马": "horse",
    "羊": "goat",
    "猴": "monkey",
    "鸡": "rooster",
    "狗": "dog",
    "猪": "pig",
}

FOCUS_ALIASES = {
    "本命年": "benmingnian_reflection",
    "太岁": "taisui_culture",
    "犯太岁": "taisui_culture",
    "关系": "relationship_reflection",
    "合不合": "relationship_reflection",
    "工作": "work_reflection",
    "事业": "work_reflection",
    "搬家": "life_planning",
}


def normalize_zodiac(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower()
    if lowered in set(ZODIAC_ALIASES.values()):
        return lowered
    for keyword, code in ZODIAC_ALIASES.items():
        if keyword in text:
            return code
    return lowered


def detect_focus(text: str) -> str:
    for keyword, focus in FOCUS_ALIASES.items():
        if keyword in text:
            return focus
    return "symbolic_reflection"


def detect_year(text: str) -> str:
    match = re.search(r"(19|20)\d{2}", text)
    return match.group(0) if match else ""


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("question_text, request_text, or text is required")
    guard = zodiac_request_guard.guard({"request_text": text})
    birth_year = str(payload.get("birth_year", "")).strip() or detect_year(text)
    zodiac = normalize_zodiac(payload.get("zodiac", ""))
    focus = str(payload.get("focus", "")).strip() or detect_focus(text)
    subject_scope = str(payload.get("subject_scope", "self")).strip() or "self"
    source_note = str(payload.get("source_note", "")).strip()
    missing_fields = []
    if not birth_year and not zodiac:
        missing_fields.append("birth_year_or_zodiac")
    if subject_scope != "self" and "consent" not in subject_scope:
        missing_fields.append("third_party_consent_or_scope_limit")
    if not source_note:
        missing_fields.append("source_or_context_note")
    return {
        "tool": "zodiac_profile_recorder",
        "system": "zodiac_symbolic_reflection",
        "is_valid": bool(guard["can_continue_zodiac"]),
        "can_continue_zodiac": bool(guard["can_continue_zodiac"]),
        "question_text": text,
        "birth_year": birth_year,
        "zodiac": zodiac,
        "focus": focus,
        "subject_scope": subject_scope,
        "source_note": source_note,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_zodiac_symbols",
            "build_zodiac_interpretation_plan",
            "keep_source_and_scope_visible",
        ] if guard["can_continue_zodiac"] else ["pause_zodiac_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["question_text"] = args.text
    if args.birth_year:
        payload["birth_year"] = args.birth_year
    if args.zodiac:
        payload["zodiac"] = args.zodiac
    if args.focus:
        payload["focus"] = args.focus
    if args.subject_scope:
        payload["subject_scope"] = args.subject_scope
    if args.source_note:
        payload["source_note"] = args.source_note
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
    parser.add_argument("--text", help="Zodiac question or request notes.")
    parser.add_argument("--birth-year", help="Birth year if relevant.")
    parser.add_argument("--zodiac", help="生肖/属相, e.g. 龙, rabbit, dog.")
    parser.add_argument("--focus", help="benmingnian_reflection, taisui_culture, relationship_reflection, etc.")
    parser.add_argument("--subject-scope", help="self, third_party_with_consent, generalized.")
    parser.add_argument("--source-note", help="Source, context, or practical note.")
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
