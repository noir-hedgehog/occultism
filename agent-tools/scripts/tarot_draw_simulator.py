#!/usr/bin/env python3
"""Simulate a Tarot draw that can be validated by tarot_draw_recorder."""

from __future__ import annotations

import argparse
import json
import random
import secrets
import sys
from typing import Any

import tarot_draw_recorder


ORIENTATION_MODES = {"upright_only", "mixed", "reversed_allowed"}


def canonical_deck() -> list[str]:
    return sorted(set(tarot_draw_recorder.CARD_ALIASES.values()))


def spread_positions(spread_id: str, custom_positions: object = None, card_count: object = None) -> list[str]:
    if isinstance(custom_positions, list) and custom_positions:
        return [str(position).strip() for position in custom_positions if str(position).strip()]
    if spread_id in tarot_draw_recorder.SPREADS:
        return list(tarot_draw_recorder.SPREADS[spread_id].positions)
    if card_count is not None:
        count = int(card_count)
        if count < 1 or count > 78:
            raise ValueError("card_count must be between 1 and 78")
        return [f"牌位 {index + 1}" for index in range(count)]
    raise ValueError("known spread_id, positions, or card_count is required")


def normalize_mode(value: object) -> str:
    mode = str(value or "mixed").strip().lower()
    aliases = {
        "upright": "upright_only",
        "正位": "upright_only",
        "mixed": "mixed",
        "allow_reversed": "reversed_allowed",
        "reversed": "reversed_allowed",
        "可逆位": "reversed_allowed",
    }
    mode = aliases.get(mode, mode)
    if mode not in ORIENTATION_MODES:
        raise ValueError(f"unknown orientation_mode: {value}")
    return mode


def normalize_probability(value: object, mode: str) -> float:
    if mode == "upright_only":
        return 0.0
    if value in (None, ""):
        return 0.5
    probability = float(value)
    if probability < 0 or probability > 1:
        raise ValueError("reversal_probability must be between 0 and 1")
    return probability


def draw_orientation(rng: random.Random, mode: str, probability: float) -> str:
    if mode == "upright_only":
        return "upright"
    if mode == "reversed_allowed":
        return "reversed" if rng.random() < probability else "upright"
    return "reversed" if rng.random() < probability else "upright"


def simulate(payload: dict[str, Any]) -> dict[str, Any]:
    spread_id = str(payload.get("spread_id", "single_focus")).strip() or "single_focus"
    positions = spread_positions(spread_id, payload.get("positions"), payload.get("card_count"))
    deck = canonical_deck()
    if len(positions) > len(deck):
        raise ValueError("cannot draw more cards than the 78-card deck")

    seed = payload.get("seed")
    generated_seed = False
    if seed in (None, ""):
        seed = secrets.randbits(64)
        generated_seed = True
    mode = normalize_mode(payload.get("orientation_mode"))
    probability = normalize_probability(payload.get("reversal_probability"), mode)

    rng = random.Random(str(seed))
    selected_cards = rng.sample(deck, len(positions))
    cards = [
        {
            "card": card,
            "orientation": draw_orientation(rng, mode, probability),
            "position": positions[index],
        }
        for index, card in enumerate(selected_cards)
    ]
    record_payload = {
        "question_text": str(payload.get("question_text", payload.get("request_text", ""))).strip(),
        "spread_id": spread_id,
        "positions": positions if spread_id not in tarot_draw_recorder.SPREADS else None,
        "cards": cards,
    }
    recorded = tarot_draw_recorder.record(record_payload)

    return {
        "question_text": record_payload["question_text"],
        "spread_id": spread_id,
        "seed": str(seed),
        "seed_generated": generated_seed,
        "deck_size": len(deck),
        "orientation_mode": mode,
        "reversal_probability": probability,
        "cards": cards,
        "recorded_draw": recorded,
        "limits": [
            "Simulated draws are randomization aids for symbolic reflection, not evidence of fate or prediction.",
            "Use a seed when the draw must be reproducible for audit or tests.",
            "Continue with tarot_card_lookup and mystic_output_lint before final interpretation.",
        ],
        "next_steps": [
            "review_recorded_draw_is_valid",
            "lookup_each_card_with_tarot_card_lookup",
            "interpret_by_position_and_question",
            "lint_final_output_with_mystic_output_lint",
        ],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json:
        payload.update(json.loads(args.json))
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            payload.update(json.load(f))
    if args.spread_id:
        payload["spread_id"] = args.spread_id
    if args.question:
        payload["question_text"] = args.question
    if args.seed:
        payload["seed"] = args.seed
    if args.orientation_mode:
        payload["orientation_mode"] = args.orientation_mode
    if args.card_count is not None:
        payload["card_count"] = args.card_count
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"question_text": raw}
    raise ValueError("Provide --json, --file, --spread-id, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", help="JSON input.")
    parser.add_argument("--file", help="Path to JSON input.")
    parser.add_argument("--spread-id", help="Known spread id.")
    parser.add_argument("--question", help="Optional question text.")
    parser.add_argument("--seed", help="Optional deterministic seed.")
    parser.add_argument("--orientation-mode", help="upright_only, mixed, or reversed_allowed.")
    parser.add_argument("--card-count", type=int, help="Card count for generic custom draw.")
    args = parser.parse_args()
    try:
        result = simulate(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
