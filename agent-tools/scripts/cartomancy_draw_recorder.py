#!/usr/bin/env python3
"""Record a low-risk playing-card cartomancy draw."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import cartomancy_request_guard


def normalize_cards(raw: object) -> list[dict[str, str]]:
    if isinstance(raw, list):
        cards = []
        for item in raw:
            if isinstance(item, dict):
                card = str(item.get("card", item.get("name", ""))).strip()
                position = str(item.get("position", "")).strip()
                orientation = str(item.get("orientation", "upright")).strip() or "upright"
            else:
                card = str(item).strip()
                position = ""
                orientation = "upright"
            if card:
                cards.append({"card": card, "position": position, "orientation": orientation})
        return cards
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", "，", "/", "|", "；", ";", "+"):
        text = text.replace(sep, ",")
    cards = []
    for part in text.split(","):
        card = part.strip()
        if card:
            cards.append({"card": card, "position": "", "orientation": "upright"})
    return cards


def record(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not question:
        raise ValueError("question_text, request_text, or text is required")
    guard = cartomancy_request_guard.guard({"request_text": question})
    spread_type = str(payload.get("spread_type", "single_or_three_card")).strip() or "single_or_three_card"
    deck_type = str(payload.get("deck_type", "standard_52_card")).strip() or "standard_52_card"
    draw_source = str(payload.get("draw_source", "user_provided")).strip() or "user_provided"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    cards = normalize_cards(payload.get("cards", payload.get("drawn_cards", "")))
    missing_fields = []
    if not cards:
        missing_fields.append("cards")
    if not spread_type:
        missing_fields.append("spread_type")
    return {
        "tool": "cartomancy_draw_recorder",
        "system": "cartomancy_symbolic_reflection",
        "is_valid": bool(guard["can_continue_cartomancy"]),
        "can_continue_cartomancy": bool(guard["can_continue_cartomancy"]),
        "question_text": question,
        "deck_type": deck_type,
        "spread_type": spread_type,
        "draw_source": draw_source,
        "focus": focus,
        "cards": cards,
        "card_count": len(cards),
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_cartomancy_cards",
            "build_cartomancy_interpretation_plan",
            "keep_draw_source_and_limits_visible",
        ] if guard["can_continue_cartomancy"] else ["pause_cartomancy_consultation", "reframe_to_real_world_support"],
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
    if args.deck_type:
        payload["deck_type"] = args.deck_type
    if args.draw_source:
        payload["draw_source"] = args.draw_source
    if args.focus:
        payload["focus"] = args.focus
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
    parser.add_argument("--text", help="Cartomancy question or request notes.")
    parser.add_argument("--cards", help="Drawn cards, comma-separated.")
    parser.add_argument("--spread-type", help="single_card, three_card, line, custom.")
    parser.add_argument("--deck-type", help="standard_52_card, standard_with_jokers, custom.")
    parser.add_argument("--draw-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--focus", help="Consultation focus.")
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
