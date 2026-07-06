#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for scrying observations."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import scrying_observation_recorder
import scrying_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = scrying_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_ambiguous_scrying_observation",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是模糊观察、视觉联想或个人感受；先要求观察来源、短时结束状态和用户自己的联想，不编造固定权威含义。",
            "reflection_questions": ["观察是否已经结束且用户状态稳定？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、灵体讯息、驱邪证明、诊断、财富结果、第三方事实或长时间凝视步骤。",
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
    record = scrying_observation_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_scrying"]:
        return {
            "tool": "scrying_interpretation_planner",
            "is_valid": False,
            "can_continue_scrying": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_scrying_consultation", "reframe_to_grounding_or_real_world_support"],
        }
    observations = record["visual_notes"] + record["surface_notes"] + record["feeling_notes"]
    symbol_plans = [build_symbol_plan(item, focus) for item in observations]
    return {
        "tool": "scrying_interpretation_planner",
        "is_valid": True,
        "can_continue_scrying": True,
        "question_text": record["question_text"],
        "observation_source": record["observation_source"],
        "observation_state": record["observation_state"],
        "medium": record["medium"],
        "focus": record["focus"],
        "visual_notes": record["visual_notes"],
        "surface_notes": record["surface_notes"],
        "feeling_notes": record["feeling_notes"],
        "observation_description": record["observation_description"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这些水晶球/镜面/水面观察能帮助用户整理哪种现实问题、可验证线索、身心安全边界和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明只处理短时、已结束的观察或文化学习，不引导继续凝视或追求幻觉。",
                "标注观察来源、安全状态、媒介、观察内容和缺失字段。",
                "逐个观察解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及不适、幻觉恐惧、专业问题、鬼神恐惧、财务赌博、第三方窥探、操控、身份标签或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present scrying visuals as fact, prediction, diagnosis, exorcism proof, spirit message, gambling advice, investment advice, third-party mind reading, identity label, or professional advice.",
            "Do not provide long-staring, trance induction, sleep deprivation, or hallucination-seeking instructions.",
        ],
        "next_steps": ["draft_scrying_answer_from_plan", "run_mystic_output_lint", "offer_grounding_and_reality_check_questions"],
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
    if args.medium:
        payload["medium"] = args.medium
    if args.visual_notes:
        payload["visual_notes"] = args.visual_notes
    if args.surface_notes:
        payload["surface_notes"] = args.surface_notes
    if args.feeling_notes:
        payload["feeling_notes"] = args.feeling_notes
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
    parser.add_argument("--text", help="Scrying observation question or notes.")
    parser.add_argument("--observation-source", help="user_described, image_notes, memory_notes.")
    parser.add_argument("--observation-state", help="short_completed, photo_notes, memory_notes, guided_visualization_ended, unknown.")
    parser.add_argument("--medium", help="crystal_ball, mirror, black_mirror, water_bowl, photo_notes, guided_visualization.")
    parser.add_argument("--visual-notes", help="Observed visual symbols.")
    parser.add_argument("--surface-notes", help="Observed surface qualities.")
    parser.add_argument("--feeling-notes", help="User feeling notes.")
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
