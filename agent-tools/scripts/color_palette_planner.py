#!/usr/bin/env python3
"""Build a safe five-elements color palette plan."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import color_profile_recorder
import color_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = color_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "color": query,
            "symbol_code": "unknown_or_personal_color",
            "element": "source_specific",
            "keywords": [],
            "interpretation_prompt": "这可能是个人、品牌、地区或商家语境中的颜色名称；先要求实物、场景和偏好说明，不编造开运功效。",
            "reflection_questions": ["这个颜色用于什么场景？", "用户已有物件、预算、舒适度和现实限制是什么？"],
            "action_guidance": "不编造招财、疗愈、桃花或避灾功效。",
        }
    return {
        "color": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "element": symbol["element"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def candidate_colors(record: dict[str, Any]) -> list[str]:
    colors = list(record.get("colors", []))
    desired = str(record.get("desired_element", "")).strip()
    if desired and desired not in colors:
        colors.append(desired)
    return colors or ["绿色", "白色"]


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = color_profile_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["scene"]
    if not record["can_continue_color"]:
        return {
            "tool": "color_palette_planner",
            "is_valid": False,
            "can_continue_color": False,
            "intention_text": record["intention_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "palette_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_color_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans = [build_symbol_plan(color, focus) for color in candidate_colors(record)]
    return {
        "tool": "color_palette_planner",
        "is_valid": True,
        "can_continue_color": True,
        "intention_text": record["intention_text"],
        "scene": record["scene"],
        "colors": record["colors"],
        "desired_element": record["desired_element"],
        "existing_items": record["existing_items"],
        "budget_note": record["budget_note"],
        "practical_constraints": record["practical_constraints"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "palette_plan": {
            "core_prompt": "这个配色能帮助用户建立哪种情绪锚点、行动提醒、空间秩序或场景适配？",
            "color_count": len(symbol_plans),
            "practical_steps": [
                "先使用已有衣物、配件、桌面物件或低成本色块，不为了开运新买昂贵物品。",
                "把颜色解释为提醒和场景语言，例如专注、清晰、休息、行动或稳定。",
                "保持场合规范、舒适度、安全、预算和个人偏好优先。",
                "不评价外貌、身份、肤色、体型或他人价值。",
                "若选择颜色引发恐惧、专业问题或购买压力，暂停颜色流程并回到现实支持。",
            ],
        },
        "limits": [
            "Use cultural and symbolic reflection language only.",
            "Do not present colors as fate proof, wealth promise, medical treatment, disaster protection, romance guarantee, or professional advice.",
            "Do not create appearance shaming, identity labels, expensive purchase pressure, or dependency.",
        ],
        "next_steps": ["draft_color_answer_from_plan", "run_mystic_output_lint", "offer_low_cost_palette_checklist"],
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
    if args.focus:
        payload["focus"] = args.focus
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
    parser.add_argument("--focus", help="Optional focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
