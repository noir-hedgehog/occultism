#!/usr/bin/env python3
"""Record a low-risk oracle-card draw."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import oracle_card_request_guard


SPREAD_ALIASES = {
    "单张": "single_card",
    "一张": "single_card",
    "三张": "three_card_reflection",
    "3张": "three_card_reflection",
    "过去现在未来": "past_present_next",
}

POSITION_HINTS = {
    "single_card": ["focus_prompt"],
    "three_card_reflection": ["current_theme", "support_or_block", "next_step"],
    "past_present_next": ["past_context", "present_focus", "next_step"],
}


def detect_spread(text: str) -> str:
    for keyword, spread in SPREAD_ALIASES.items():
        if keyword in text:
            return spread
    return "three_card_reflection"


def normalize_cards(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|", "；", ";"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("question_text, request_text, or text is required")
    guard = oracle_card_request_guard.guard({"request_text": text})
    spread = str(payload.get("spread_type", "")).strip() or detect_spread(text)
    cards = normalize_cards(payload.get("cards", payload.get("drawn_cards", "")))
    deck_name = str(payload.get("deck_name", "")).strip()
    source = str(payload.get("source", "user_reported_or_manual_draw")).strip()
    missing_fields = []
    if not deck_name:
        missing_fields.append("deck_name_or_source")
    if not cards:
        missing_fields.append("drawn_cards_or_card_keywords")
    expected_count = len(POSITION_HINTS.get(spread, POSITION_HINTS["three_card_reflection"]))
    if cards and len(cards) != expected_count:
        missing_fields.append(f"{spread}_expects_{expected_count}_cards")
    return {
        "tool": "oracle_card_draw_recorder",
        "system": "oracle_card_symbolic_reflection",
        "is_valid": bool(guard["can_continue_oracle_card"]),
        "can_continue_oracle_card": bool(guard["can_continue_oracle_card"]),
        "question_text": text,
        "deck_name": deck_name,
        "spread_type": spread,
        "positions": POSITION_HINTS.get(spread, POSITION_HINTS["three_card_reflection"]),
        "cards": cards,
        "card_count": len(cards),
        "source": source,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_oracle_card_symbol_motifs",
            "build_oracle_card_interpretation_plan",
            "compare_real_world_evidence_first",
        ] if guard["can_continue_oracle_card"] else ["pause_oracle_card_reading", "reframe_to_real_world_support"],
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
    if args.deck_name:
        payload["deck_name"] = args.deck_name
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
    parser.add_argument("--text", help="Oracle-card question or session notes.")
    parser.add_argument("--cards", help="Drawn card names, titles, or keywords.")
    parser.add_argument("--deck-name", help="Deck/source name if known.")
    parser.add_argument("--spread-type", help="single_card, three_card_reflection, or past_present_next.")
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
