#!/usr/bin/env python3
"""Build a safe reflection plan for deity, ancestor, altar, offering, and vow-return requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import deity_ancestor_context_recorder
import deity_ancestor_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = deity_ancestor_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_deity_ancestor_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人、家庭或地方传统联想；先询问来源和语境，不编造神明命令、祖先命令、灵体事实、灾祸或法事必要性。",
            "reflection_questions": ["它来自哪个家庭/地方/宗教语境？", "它对应纪念、感恩、秩序还是现实行动？", "是否像命令恐吓、危险仪式、强迫供奉或反复依赖？"],
            "action_guidance": "不编造神谕、祖先讯息或灾祸惩罚；只放回文化来源、纪念表达、家庭边界和现实安全。",
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
    record = deity_ancestor_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_deity_ancestor"]:
        return {
            "tool": "deity_ancestor_reflection_planner",
            "is_valid": False,
            "can_continue_deity_ancestor": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_deity_ancestor_consultation", "reframe_to_cultural_memorial_safety_or_professional_support"],
        }
    queries = []
    for group in ([record["focus_entity"], record["occasion"], record["user_intention"]], record["existing_items"], record["offering_or_memorial_actions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "deity_ancestor_reflection_planner",
        "is_valid": True,
        "can_continue_deity_ancestor": True,
        "context_text": record["context_text"],
        "tradition_context": record["tradition_context"],
        "focus_entity": record["focus_entity"],
        "occasion": record["occasion"],
        "user_intention": record["user_intention"],
        "existing_items": record["existing_items"],
        "offering_or_memorial_actions": record["offering_or_memorial_actions"],
        "household_boundaries": record["household_boundaries"],
        "safety_context": record["safety_context"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次神明/祖先/供奉/还愿请求能怎样被改写为文化学习、纪念感恩、家庭边界和低风险现实提醒？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先标注来源传统：家庭习俗、地方民俗、宗教传统、个人纪念或现代改编。",
                "把供奉和祭拜语言限制为纪念、感恩、秩序和生活提醒，不写成命令或惩罚。",
                "列出 1-3 个低风险动作，例如清洁整理、写感谢句、摆放已有照片或清水、与家人沟通边界。",
                "检查消防、食品、宠物儿童、家庭同意和预算边界；避免明火、摄入、强迫和高价消费。",
                "设置复盘时间和停止条件，避免反复求确认、还愿焦虑或不做就害怕。",
            ],
        },
        "limits": [
            "Use cultural, memorial, gratitude, and grounded-reflection language only.",
            "Do not confirm deity commands, ancestor commands, dream facts, punishments, spirit facts, disasters, or third-party privacy.",
            "Do not provide dangerous ritual, ingestion, professional replacement, coercion, retaliation, or forced worship.",
            "Do not encourage expensive rituals, paid consecration packages, purchase pressure, or repeated dependency.",
        ],
        "next_steps": ["draft_deity_ancestor_answer_from_plan", "run_mystic_output_lint", "offer_low_risk_memorial_actions_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "tradition_context", "focus_entity", "occasion", "user_intention", "existing_items", "offering_or_memorial_actions", "household_boundaries", "safety_context", "review_time", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["context_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"context_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Deity or ancestor context notes.")
    parser.add_argument("--tradition-context", help="Tradition, family, or source context.")
    parser.add_argument("--focus-entity", help="Deity, ancestor, altar, or memorial focus.")
    parser.add_argument("--occasion", help="Occasion.")
    parser.add_argument("--user-intention", help="User intention.")
    parser.add_argument("--existing-items", help="Existing items.")
    parser.add_argument("--offering-or-memorial-actions", help="Offering or memorial actions.")
    parser.add_argument("--household-boundaries", help="Household consent and boundary notes.")
    parser.add_argument("--safety-context", help="Fire, food, child, pet, and practical safety context.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stopping condition.")
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
