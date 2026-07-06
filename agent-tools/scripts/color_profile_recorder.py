#!/usr/bin/env python3
"""Record a low-risk five-elements color consultation context."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import color_request_guard


SCENE_ALIASES = {
    "穿搭": "outfit",
    "衣服": "outfit",
    "今天穿": "outfit",
    "饰品": "accessory",
    "办公桌": "workspace",
    "办公室": "workspace",
    "卧室": "bedroom",
    "家里": "home",
    "品牌": "brand",
    "海报": "brand",
}


def normalize_colors(raw: object) -> list[str]:
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    text = str(raw or "").strip()
    if not text:
        return []
    for sep in ("、", ",", "，", "/", "|", "；", ";", "和"):
        text = text.replace(sep, " ")
    return [part.strip() for part in text.split() if part.strip()]


def detect_scene(text: str) -> str:
    for keyword, scene in SCENE_ALIASES.items():
        if keyword in text:
            return scene
    return "symbolic_reflection"


def record(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("intention_text", payload.get("request_text", payload.get("text", "")))).strip()
    if not text:
        raise ValueError("intention_text, request_text, or text is required")
    guard = color_request_guard.guard({"request_text": text})
    scene = str(payload.get("scene", "")).strip() or detect_scene(text)
    colors = normalize_colors(payload.get("colors", payload.get("candidate_colors", "")))
    desired_element = str(payload.get("desired_element", "")).strip()
    existing_items = str(payload.get("existing_items", "")).strip()
    budget_note = str(payload.get("budget_note", "")).strip()
    practical_constraints = normalize_colors(payload.get("practical_constraints", ""))
    missing_fields = []
    if not colors and not desired_element:
        missing_fields.append("candidate_colors_or_desired_element")
    if not existing_items and not budget_note:
        missing_fields.append("existing_items_or_budget_note")
    return {
        "tool": "color_profile_recorder",
        "system": "color_symbolic_reflection",
        "is_valid": bool(guard["can_continue_color"]),
        "can_continue_color": bool(guard["can_continue_color"]),
        "intention_text": text,
        "scene": scene,
        "colors": colors,
        "desired_element": desired_element,
        "existing_items": existing_items,
        "budget_note": budget_note,
        "practical_constraints": practical_constraints,
        "risk_flags": guard["risk_flags"],
        "missing_fields": missing_fields,
        "safety_notes": guard["required_boundaries"],
        "next_steps": [
            "lookup_color_symbols",
            "build_color_palette_plan",
            "prefer_existing_items_and_low_cost_adjustments",
        ] if guard["can_continue_color"] else ["pause_color_consultation", "reframe_to_real_world_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["intention_text"] = args.text
    if args.scene:
        payload["scene"] = args.scene
    if args.colors:
        payload["colors"] = args.colors
    if args.desired_element:
        payload["desired_element"] = args.desired_element
    if args.existing_items:
        payload["existing_items"] = args.existing_items
    if args.budget_note:
        payload["budget_note"] = args.budget_note
    if args.practical_constraints:
        payload["practical_constraints"] = args.practical_constraints
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Color intention or request notes.")
    parser.add_argument("--scene", help="outfit, accessory, workspace, bedroom, brand, etc.")
    parser.add_argument("--colors", help="Candidate colors.")
    parser.add_argument("--desired-element", help="wood, fire, earth, metal, water.")
    parser.add_argument("--existing-items", help="Existing items or colors.")
    parser.add_argument("--budget-note", help="Budget or no-purchase note.")
    parser.add_argument("--practical-constraints", help="Practical constraints.")
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
