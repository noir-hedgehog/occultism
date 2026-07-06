#!/usr/bin/env python3
"""Record a low-risk astrodice or divination-dice consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import dice_request_guard


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
    guard = dice_request_guard.guard({"request_text": question})
    dice_system = str(payload.get("dice_system", "astrodice")).strip() or "astrodice"
    dice_faces = normalize_list(payload.get("dice_faces", ""))
    planet = str(payload.get("planet", "")).strip()
    sign = str(payload.get("sign", "")).strip()
    house = str(payload.get("house", "")).strip()
    if not dice_faces:
        dice_faces = [item for item in (planet, sign, house) if item]
    roll_source = str(payload.get("roll_source", "user_provided")).strip() or "user_provided"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    missing_fields = []
    if not dice_faces:
        missing_fields.append("dice_faces_or_planet_sign_house")
    if dice_system == "astrodice" and len(dice_faces) < 3:
        missing_fields.append("complete_planet_sign_house_triplet")
    return {
        "tool": "dice_roll_recorder",
        "system": "dice_symbolic_reflection",
        "is_valid": bool(guard["can_continue_dice"]),
        "can_continue_dice": bool(guard["can_continue_dice"]),
        "question_text": question,
        "dice_system": dice_system,
        "dice_faces": dice_faces,
        "roll_source": roll_source,
        "focus": focus,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_dice_symbols",
            "build_dice_interpretation_plan",
            "keep_roll_source_and_limits_visible",
        ] if guard["can_continue_dice"] else ["pause_dice_consultation", "reframe_to_real_world_support"],
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
    if args.dice_system:
        payload["dice_system"] = args.dice_system
    if args.dice_faces:
        payload["dice_faces"] = args.dice_faces
    if args.planet:
        payload["planet"] = args.planet
    if args.sign:
        payload["sign"] = args.sign
    if args.house:
        payload["house"] = args.house
    if args.roll_source:
        payload["roll_source"] = args.roll_source
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
    parser.add_argument("--text", help="Dice question or request notes.")
    parser.add_argument("--dice-system", help="astrodice, symbol_dice, custom.")
    parser.add_argument("--dice-faces", help="Dice faces, e.g. Mars Aries 10th-house.")
    parser.add_argument("--planet", help="Astrodice planet face.")
    parser.add_argument("--sign", help="Astrodice sign face.")
    parser.add_argument("--house", help="Astrodice house face.")
    parser.add_argument("--roll-source", help="user_provided, simulated_with_consent, external_app.")
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
