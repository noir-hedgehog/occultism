#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for Chinese character divination."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import cezi_character_recorder
import cezi_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = cezi_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_character_feature",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是用户的私人联想、具体写法或未收录部件；先询问来源和用户第一联想，不编造固定权威含义。",
            "reflection_questions": ["这个字形线索从哪里来？", "用户自己的第一联想是什么？", "它能如何转成现实问题和低风险行动？"],
            "action_guidance": "不编造预言、诊断、寿命、财富、灵异事实或第三方真实想法。",
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
    record = cezi_character_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_cezi"]:
        return {
            "tool": "cezi_interpretation_planner",
            "is_valid": False,
            "can_continue_cezi": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_cezi_consultation", "reframe_to_real_world_support"],
        }
    queries = record["components"] or record["visible_features"]
    if record["user_association"]:
        queries = queries + [record["user_association"]]
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "cezi_interpretation_planner",
        "is_valid": True,
        "can_continue_cezi": True,
        "question_text": record["question_text"],
        "character": record["character"],
        "character_source": record["character_source"],
        "focus": record["focus"],
        "components": record["components"],
        "visible_features": record["visible_features"],
        "user_association": record["user_association"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个字例能帮助用户整理哪种现实问题、表达线索、可验证证据和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明测字/拆字只作汉字象征反思，不作确定预言、事实证明或人格/寿命判断。",
                "标注字例来源、字、部件/结构、用户联想和缺失字段。",
                "逐个部件、结构或联想解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及专业替代、财务赌博、寿命/人格标签、儿童标签、灵异恐惧、第三方窥探、操控或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present character divination as fact, prediction, diagnosis, spirit confirmation, lifespan judgment, personality ranking, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not repeat-read characters until the desired answer appears.",
        ],
        "next_steps": ["draft_cezi_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
    if args.character:
        payload["character"] = args.character
    if args.character_source:
        payload["character_source"] = args.character_source
    if args.components:
        payload["components"] = args.components
    if args.visible_features:
        payload["visible_features"] = args.visible_features
    if args.user_association:
        payload["user_association"] = args.user_association
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
    parser.add_argument("--text", help="Cezi question or request notes.")
    parser.add_argument("--character", help="Character being interpreted.")
    parser.add_argument("--character-source", help="user_provided, random_draw, dream, name, simulated_with_consent, other.")
    parser.add_argument("--components", help="Components/radicals, e.g. 木 日 门.")
    parser.add_argument("--visible-features", help="Visible form notes, e.g. 左右结构 开口.")
    parser.add_argument("--user-association", help="User's own association with the character.")
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
