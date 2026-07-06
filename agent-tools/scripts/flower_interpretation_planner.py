#!/usr/bin/env python3
"""Build a safe symbolic plan for flower-language consultations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import flower_item_recorder
import flower_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = flower_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "flower": query,
            "symbol_code": "unknown_or_local_flower",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是地方花名、商品名或私人联想；先询问实际花材、场景和用户自己的含义，不编造固定花语。",
            "reflection_questions": ["花材来源和使用场景是什么？", "用户自己的第一联想是什么？", "有哪些现实安全、预算或场合限制？"],
            "action_guidance": "不编造疗愈、招财、复合、驱邪、毒性或宠物安全结论。",
        }
    return {
        "flower": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = flower_item_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_flower"]:
        return {
            "tool": "flower_interpretation_planner",
            "is_valid": False,
            "can_continue_flower": False,
            "intention_text": record["intention_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "flower_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_flower_consultation", "reframe_to_real_world_support"],
        }
    queries = list(record["flowers"])
    for color in record["colors"]:
        if color not in queries:
            queries.append(color)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "flower_interpretation_planner",
        "is_valid": True,
        "can_continue_flower": True,
        "intention_text": record["intention_text"],
        "flowers": record["flowers"],
        "colors": record["colors"],
        "scene": record["scene"],
        "recipient": record["recipient"],
        "source": record["source"],
        "budget_note": record["budget_note"],
        "safety_constraints": record["safety_constraints"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "flower_plan": {
            "core_prompt": "这个花材组合能帮助用户表达哪种意图、建立哪种提醒、整理哪种关系边界或空间氛围？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先使用已有花材、低成本替代、图片或文字卡片，不为了开运/复合购买昂贵花材。",
                "把花语解释为表达和提醒，例如感谢、边界、鼓励、纪念、休息或清晰沟通。",
                "过敏、宠物、儿童、香味、场合和预算限制优先于象征含义。",
                "不读取收花人的真实想法，不承诺对方反应或关系结果。",
                "若涉及专业问题、恐惧升级、摄入药用或反复依赖，暂停花语流程。",
            ],
        },
        "limits": [
            "Use cultural and symbolic reflection language only.",
            "Do not present flowers as fate proof, wealth promise, medical treatment, poison/allergy guidance, disaster protection, romance guarantee, or professional advice.",
            "Do not create expensive purchase pressure, third-party mind reading, coercion, or dependency.",
        ],
        "next_steps": ["draft_flower_answer_from_plan", "run_mystic_output_lint", "offer_low_cost_safe_flower_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "flowers", "colors", "scene", "recipient", "source", "budget_note", "safety_constraints", "focus"):
        value = getattr(args, key)
        if value:
            payload["intention_text" if key == "text" else key] = value
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
    parser.add_argument("--text", help="Flower-language intention or request notes.")
    parser.add_argument("--flowers", help="Flower or plant names.")
    parser.add_argument("--colors", help="Flower colors.")
    parser.add_argument("--scene", help="gift, home, desk, reflection, ritualized_journaling, etc.")
    parser.add_argument("--recipient", help="Recipient or audience, if relevant.")
    parser.add_argument("--source", help="user_provided, existing_items, simulated_with_consent, cultural_learning.")
    parser.add_argument("--budget-note", help="Budget or no-purchase note.")
    parser.add_argument("--safety-constraints", help="Allergy, pet, child, scent, venue, or other constraints.")
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
