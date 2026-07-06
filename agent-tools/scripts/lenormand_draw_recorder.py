#!/usr/bin/env python3
"""Record a low-risk Lenormand card draw."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import lenormand_request_guard


SPREAD_ALIASES = {
    "三张": "three_card_line",
    "3张": "three_card_line",
    "五张": "five_card_line",
    "5张": "five_card_line",
    "九宫格": "nine_card_box",
    "3x3": "nine_card_box",
}

POSITION_HINTS = {
    "three_card_line": ["left_context", "center_focus", "right_development"],
    "five_card_line": ["background", "near_context", "focus", "near_development", "far_development"],
    "nine_card_box": ["top_left", "top_center", "top_right", "middle_left", "center", "middle_right", "bottom_left", "bottom_center", "bottom_right"],
}


def detect_spread(text: str) -> str:
    for keyword, spread in SPREAD_ALIASES.items():
        if keyword in text:
            return spread
    return "three_card_line"


def normalize_cards(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("question_text, request_text, or text is required")
    guard = lenormand_request_guard.guard({"request_text": text})
    spread = str(payload.get("spread_type", "")).strip() or detect_spread(text)
    cards = normalize_cards(payload.get("cards", payload.get("drawn_cards", "")))
    source = str(payload.get("source", "user_reported_or_manual_draw")).strip()
    missing_fields = []
    if not cards:
        missing_fields.append("drawn_cards")
    expected_count = len(POSITION_HINTS.get(spread, POSITION_HINTS["three_card_line"]))
    if cards and len(cards) != expected_count:
        missing_fields.append(f"{spread}_expects_{expected_count}_cards")
    return {
        "tool": "lenormand_draw_recorder",
        "system": "lenormand_divination",
        "is_valid": bool(guard["can_continue_lenormand"]),
        "can_continue_lenormand": bool(guard["can_continue_lenormand"]),
        "question_text": text,
        "spread_type": spread,
        "positions": POSITION_HINTS.get(spread, POSITION_HINTS["three_card_line"]),
        "cards": cards,
        "card_count": len(cards),
        "source": source,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_lenormand_card_symbols",
            "build_lenormand_interpretation_plan",
            "compare_real_world_evidence_first",
        ] if guard["can_continue_lenormand"] else ["pause_lenormand_reading", "reframe_to_real_world_support"],
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
    if args.cards:
        payload["cards"] = args.cards
    if args.spread_type:
        payload["spread_type"] = args.spread_type
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
    parser.add_argument("--text", help="Lenormand question or session notes.")
    parser.add_argument("--cards", help="Drawn cards separated by space, comma, or Chinese comma.")
    parser.add_argument("--spread-type", help="three_card_line, five_card_line, or nine_card_box.")
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
