#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for astrodice and divination dice."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import dice_roll_recorder
import dice_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = dice_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_face",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是自定义骰、牌组骰或外部应用中的骰面；先要求骰子体系和说明，不编造固定权威含义。",
            "reflection_questions": ["骰子体系和骰面来源是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果或第三方事实。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = dice_roll_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_dice"]:
        return {
            "tool": "dice_interpretation_planner",
            "is_valid": False,
            "can_continue_dice": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_dice_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans = [build_symbol_plan(face, focus) for face in record["dice_faces"]]
    return {
        "tool": "dice_interpretation_planner",
        "is_valid": True,
        "can_continue_dice": True,
        "question_text": record["question_text"],
        "dice_system": record["dice_system"],
        "dice_faces": record["dice_faces"],
        "roll_source": record["roll_source"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个骰面组合能帮助用户整理哪种现实问题、可验证线索和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明骰子只作象征反思，不作确定预言或事实证明。",
                "标注骰面来源、骰子体系和缺失字段。",
                "逐个骰面解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及财务赌博、专业问题、第三方窥探、操控或反复依赖，暂停骰子流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present dice as fact, prediction, diagnosis, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not repeat-roll until the desired answer appears.",
        ],
        "next_steps": ["draft_dice_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
