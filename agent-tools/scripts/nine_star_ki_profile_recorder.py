#!/usr/bin/env python3
"""Record a low-risk Nine Star Ki profile and consultation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import nine_star_ki_request_guard


STAR_ALIASES = {
    "1": "one_white_water",
    "一白": "one_white_water",
    "一白水星": "one_white_water",
    "one white": "one_white_water",
    "one_white_water": "one_white_water",
    "2": "two_black_earth",
    "二黑": "two_black_earth",
    "二黑土星": "two_black_earth",
    "two black": "two_black_earth",
    "two_black_earth": "two_black_earth",
    "3": "three_jade_wood",
    "三碧": "three_jade_wood",
    "三碧木星": "three_jade_wood",
    "three jade": "three_jade_wood",
    "three_jade_wood": "three_jade_wood",
    "4": "four_green_wood",
    "四绿": "four_green_wood",
    "四绿木星": "four_green_wood",
    "four green": "four_green_wood",
    "four_green_wood": "four_green_wood",
    "5": "five_yellow_earth",
    "五黄": "five_yellow_earth",
    "五黄土星": "five_yellow_earth",
    "five yellow": "five_yellow_earth",
    "five_yellow_earth": "five_yellow_earth",
    "6": "six_white_metal",
    "六白": "six_white_metal",
    "六白金星": "six_white_metal",
    "six white": "six_white_metal",
    "six_white_metal": "six_white_metal",
    "7": "seven_red_metal",
    "七赤": "seven_red_metal",
    "七赤金星": "seven_red_metal",
    "seven red": "seven_red_metal",
    "seven_red_metal": "seven_red_metal",
    "8": "eight_white_earth",
    "八白": "eight_white_earth",
    "八白土星": "eight_white_earth",
    "eight white": "eight_white_earth",
    "eight_white_earth": "eight_white_earth",
    "9": "nine_purple_fire",
    "九紫": "nine_purple_fire",
    "九紫火星": "nine_purple_fire",
    "nine purple": "nine_purple_fire",
    "nine_purple_fire": "nine_purple_fire",
}


def normalize_star(raw: object) -> str:
    text = str(raw or "").strip()
    if not text:
        return ""
    lowered = text.lower().replace("-", "_")
    return STAR_ALIASES.get(text, STAR_ALIASES.get(lowered, lowered.replace(" ", "_")))


def normalize_list(raw: object) -> list[str]:
    if isinstance(raw, list):
        parts = [str(item).strip() for item in raw if str(item).strip()]
    else:
        text = str(raw or "").strip()
        if not text:
            return []
        for sep in ("、", ",", "，", "/", "|", "；", ";", "+", "和"):
            text = text.replace(sep, " ")
        parts = [part.strip() for part in text.split() if part.strip()]
    return parts


def record(payload: dict[str, Any]) -> dict[str, Any]:
    question = str(payload.get("question_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not question:
        raise ValueError("question_text, request_text, or text is required")
    guard = nine_star_ki_request_guard.guard({"request_text": question})
    system_variant = str(payload.get("system_variant", "nine_star_ki_general")).strip() or "nine_star_ki_general"
    source = str(payload.get("source", "user_provided_or_external_reference")).strip() or "user_provided_or_external_reference"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    birth_year = str(payload.get("birth_year", "")).strip()
    birth_month = str(payload.get("birth_month", "")).strip()
    current_year = str(payload.get("current_year", "")).strip()
    home_star = normalize_star(payload.get("home_star", payload.get("birth_star", payload.get("main_star", ""))))
    month_star = normalize_star(payload.get("month_star", ""))
    annual_star = normalize_star(payload.get("annual_star", payload.get("year_star", "")))
    directions = normalize_list(payload.get("directions", payload.get("direction_focus", "")))
    reality_constraints = normalize_list(payload.get("reality_constraints", payload.get("constraints", "")))
    notes = str(payload.get("notes", payload.get("profile_notes", ""))).strip()
    missing_fields = []
    if not birth_year and not home_star:
        missing_fields.append("birth_year_or_known_home_star")
    if not focus:
        missing_fields.append("focus")
    if not current_year and annual_star:
        missing_fields.append("current_year_for_annual_star_context")
    return {
        "tool": "nine_star_ki_profile_recorder",
        "system": "nine_star_ki_symbolic_reflection",
        "is_valid": bool(guard["can_continue_nine_star_ki"]),
        "can_continue_nine_star_ki": bool(guard["can_continue_nine_star_ki"]),
        "question_text": question,
        "system_variant": system_variant,
        "source": source,
        "focus": focus,
        "birth_year": birth_year,
        "birth_month": birth_month,
        "current_year": current_year,
        "home_star": home_star,
        "month_star": month_star,
        "annual_star": annual_star,
        "directions": directions,
        "reality_constraints": reality_constraints,
        "profile_notes": notes,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_nine_star_ki_symbols",
            "build_nine_star_ki_interpretation_plan",
            "keep_source_and_missing_fields_visible",
        ] if guard["can_continue_nine_star_ki"] else ["pause_nine_star_ki_consultation", "reframe_to_real_world_support"],
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
    if args.birth_month:
        payload["birth_month"] = args.birth_month
    if args.current_year:
        payload["current_year"] = args.current_year
    if args.home_star:
        payload["home_star"] = args.home_star
    if args.month_star:
        payload["month_star"] = args.month_star
    if args.annual_star:
        payload["annual_star"] = args.annual_star
    if args.directions:
        payload["directions"] = args.directions
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
    parser.add_argument("--text", help="Nine Star Ki question or request notes.")
    parser.add_argument("--birth-year", help="Birth year or known year context.")
    parser.add_argument("--birth-month", help="Birth month if relevant to the user's system.")
    parser.add_argument("--current-year", help="Current year for annual star context.")
    parser.add_argument("--home-star", help="Known home/birth star.")
    parser.add_argument("--month-star", help="Known month star.")
    parser.add_argument("--annual-star", help="Known annual star.")
    parser.add_argument("--directions", help="Direction focus list.")
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
