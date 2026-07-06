#!/usr/bin/env python3
"""Record a low-risk tea-leaf or coffee-ground reading observation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import tasseography_request_guard


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
    guard = tasseography_request_guard.guard({"request_text": question})
    medium = str(payload.get("medium", "tea_leaves")).strip() or "tea_leaves"
    cup_zone = str(payload.get("cup_zone", "")).strip()
    pattern_source = str(payload.get("pattern_source", "user_described")).strip() or "user_described"
    focus = str(payload.get("focus", "symbolic_reflection")).strip() or "symbolic_reflection"
    observed_shapes = normalize_list(payload.get("observed_shapes", payload.get("shapes", "")))
    description = str(payload.get("description", payload.get("pattern_description", ""))).strip()
    if not observed_shapes and description:
        observed_shapes = normalize_list(description)
    missing_fields = []
    if not observed_shapes and not description:
        missing_fields.append("observed_shapes_or_description")
    if not cup_zone:
        missing_fields.append("cup_zone")
    return {
        "tool": "tasseography_pattern_recorder",
        "system": "tasseography_symbolic_reflection",
        "is_valid": bool(guard["can_continue_tasseography"]),
        "can_continue_tasseography": bool(guard["can_continue_tasseography"]),
        "question_text": question,
        "medium": medium,
        "cup_zone": cup_zone,
        "pattern_source": pattern_source,
        "focus": focus,
        "observed_shapes": observed_shapes,
        "pattern_description": description,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_tasseography_symbols",
            "build_tasseography_interpretation_plan",
            "keep_source_zone_and_uncertainty_visible",
        ] if guard["can_continue_tasseography"] else ["pause_tasseography_consultation", "reframe_to_real_world_support"],
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
    if args.medium:
        payload["medium"] = args.medium
    if args.cup_zone:
        payload["cup_zone"] = args.cup_zone
    if args.pattern_source:
        payload["pattern_source"] = args.pattern_source
    if args.observed_shapes:
        payload["observed_shapes"] = args.observed_shapes
    if args.description:
        payload["description"] = args.description
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
    parser.add_argument("--text", help="Tasseography question or request notes.")
    parser.add_argument("--medium", help="tea_leaves, coffee_grounds, cup_stain, mixed.")
    parser.add_argument("--cup-zone", help="rim, wall, base, handle_side, opposite_handle, unknown.")
    parser.add_argument("--pattern-source", help="user_described, image_notes, simulated_with_consent, external_app.")
    parser.add_argument("--observed-shapes", help="Observed shapes, e.g. bird road mountain.")
    parser.add_argument("--description", help="Free-text cup pattern description.")
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
