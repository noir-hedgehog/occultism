#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for tasseography readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import tasseography_pattern_recorder
import tasseography_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = tasseography_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_ambiguous_pattern",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是模糊图案、个人联想或照片描述；先要求观察来源和用户自己的联想，不编造固定权威含义。",
            "reflection_questions": ["图案来源、杯底位置和用户第一联想是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果、第三方事实或食品安全建议。",
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
    record = tasseography_pattern_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_tasseography"]:
        return {
            "tool": "tasseography_interpretation_planner",
            "is_valid": False,
            "can_continue_tasseography": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_tasseography_consultation", "reframe_to_real_world_support"],
        }
    symbols = record["observed_shapes"]
    symbol_plans = [build_symbol_plan(shape, focus) for shape in symbols]
    return {
        "tool": "tasseography_interpretation_planner",
        "is_valid": True,
        "can_continue_tasseography": True,
        "question_text": record["question_text"],
        "medium": record["medium"],
        "cup_zone": record["cup_zone"],
        "pattern_source": record["pattern_source"],
        "focus": record["focus"],
        "observed_shapes": record["observed_shapes"],
        "pattern_description": record["pattern_description"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个杯底图案组合能帮助用户整理哪种现实问题、可验证线索和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明茶叶/咖啡渣图案只作象征反思，不作确定预言或事实证明。",
                "标注媒介、图案来源、杯底位置和缺失字段。",
                "逐个图案解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及财务赌博、专业问题、第三方窥探、操控、不安全摄入或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present cup patterns as fact, prediction, diagnosis, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not repeat-read, rebrew, or reinterpret until the desired answer appears.",
        ],
        "next_steps": ["draft_tasseography_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
        result = plan(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["is_valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
