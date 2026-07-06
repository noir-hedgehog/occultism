#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for incense observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import incense_observation_recorder
import incense_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = incense_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_ambiguous_incense_observation",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是模糊观察、照片描述或个人联想；先要求观察来源、安全状态和用户自己的联想，不编造固定权威含义。",
            "reflection_questions": ["观察是否已经安全结束？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、驱邪证明、神明指令、诊断、财富结果、第三方事实或燃烧步骤。",
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
    record = incense_observation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_incense"]:
        return {
            "tool": "incense_interpretation_planner",
            "is_valid": False,
            "can_continue_incense": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_incense_consultation", "reframe_to_fire_safety_or_real_world_support"],
        }
    observations = record["ash_shapes"] + record["smoke_notes"] + record["ember_notes"]
    symbol_plans = [build_symbol_plan(item, focus) for item in observations]
    return {
        "tool": "incense_interpretation_planner",
        "is_valid": True,
        "can_continue_incense": True,
        "question_text": record["question_text"],
        "observation_source": record["observation_source"],
        "observation_state": record["observation_state"],
        "focus": record["focus"],
        "ash_shapes": record["ash_shapes"],
        "smoke_notes": record["smoke_notes"],
        "ember_notes": record["ember_notes"],
        "observation_description": record["observation_description"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这些香火/香灰/烟形观察能帮助用户整理哪种现实问题、可验证线索、安全边界和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明只处理已安全结束、照片记录或无烟替代观察，不提供点香或燃烧步骤。",
                "标注观察来源、安全状态、观察内容和缺失字段。",
                "逐个观察解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及明火操作、危险仪式、专业问题、鬼神恐惧、财务赌博、第三方窥探、操控、高价购买或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present incense, ash, or smoke observations as fact, prediction, diagnosis, exorcism proof, deity instruction, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not provide ignition, burning, smoke ritual, ash ingestion, blood, enclosed combustion, or unattended fire instructions.",
        ],
        "next_steps": ["draft_incense_answer_from_plan", "run_mystic_output_lint", "offer_fire_smoke_safety_and_reality_check_questions"],
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
    if args.ash_shapes:
        payload["ash_shapes"] = args.ash_shapes
    if args.smoke_notes:
        payload["smoke_notes"] = args.smoke_notes
    if args.ember_notes:
        payload["ember_notes"] = args.ember_notes
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
    parser.add_argument("--text", help="Incense observation question or notes.")
    parser.add_argument("--observation-source", help="user_described, image_notes, electric_incense, external_app.")
    parser.add_argument("--observation-state", help="already_extinguished, photo_notes, electric_incense, outdoor_safe_distance, unknown.")
    parser.add_argument("--ash-shapes", help="Observed ash shapes.")
    parser.add_argument("--smoke-notes", help="Observed smoke qualities.")
    parser.add_argument("--ember-notes", help="Observed ember or incense-tip notes.")
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
