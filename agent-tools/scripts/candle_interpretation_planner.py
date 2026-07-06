#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for candle observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import candle_observation_recorder
import candle_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = candle_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_ambiguous_candle_observation",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是模糊观察、照片描述或个人联想；先要求观察来源、安全状态和用户自己的联想，不编造固定权威含义。",
            "reflection_questions": ["观察是否已经安全结束？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、驱邪证明、诊断、财富结果、第三方事实或点火步骤。",
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
    record = candle_observation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_candle"]:
        return {
            "tool": "candle_interpretation_planner",
            "is_valid": False,
            "can_continue_candle": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_candle_consultation", "reframe_to_fire_safety_or_real_world_support"],
        }
    observations = record["flame_notes"] + record["wax_shapes"] + record["smoke_notes"]
    symbol_plans = [build_symbol_plan(item, focus) for item in observations]
    return {
        "tool": "candle_interpretation_planner",
        "is_valid": True,
        "can_continue_candle": True,
        "question_text": record["question_text"],
        "observation_source": record["observation_source"],
        "observation_state": record["observation_state"],
        "focus": record["focus"],
        "flame_notes": record["flame_notes"],
        "wax_shapes": record["wax_shapes"],
        "smoke_notes": record["smoke_notes"],
        "observation_description": record["observation_description"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这些火焰/蜡泪观察能帮助用户整理哪种现实问题、可验证线索、安全边界和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明只处理已安全结束或无火观察，不提供点火或燃烧步骤。",
                "标注观察来源、安全状态、观察内容和缺失字段。",
                "逐个观察解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及明火操作、危险仪式、专业问题、鬼神恐惧、财务赌博、第三方窥探、操控或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present flame or wax observations as fact, prediction, diagnosis, exorcism proof, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not provide ignition, burning, fire ritual, blood, enclosed combustion, or unattended flame instructions.",
        ],
        "next_steps": ["draft_candle_answer_from_plan", "run_mystic_output_lint", "offer_fire_safety_and_reality_check_questions"],
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
    if args.observation_source:
        payload["observation_source"] = args.observation_source
    if args.observation_state:
        payload["observation_state"] = args.observation_state
    if args.flame_notes:
        payload["flame_notes"] = args.flame_notes
    if args.wax_shapes:
        payload["wax_shapes"] = args.wax_shapes
    if args.smoke_notes:
        payload["smoke_notes"] = args.smoke_notes
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
    parser.add_argument("--text", help="Candle observation question or notes.")
    parser.add_argument("--observation-source", help="user_described, image_notes, led_candle, external_app.")
    parser.add_argument("--observation-state", help="already_extinguished, led_candle, photo_notes, unknown.")
    parser.add_argument("--flame-notes", help="Observed flame qualities.")
    parser.add_argument("--wax-shapes", help="Observed wax shapes.")
    parser.add_argument("--smoke-notes", help="Observed smoke notes.")
    parser.add_argument("--description", help="Free-text observation description.")
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
