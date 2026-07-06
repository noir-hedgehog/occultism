#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for casting-lots layouts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import casting_lots_layout_recorder
import casting_lots_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = casting_lots_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_object",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是自定义符物或私人象征；先询问用户给它的约定含义，不编造固定权威解释。",
            "reflection_questions": ["这个物件的来源、用户约定含义和落点是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果、灵异事实或第三方真实想法。",
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
    record = casting_lots_layout_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_casting_lots"]:
        return {
            "tool": "casting_lots_interpretation_planner",
            "is_valid": False,
            "can_continue_casting_lots": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_casting_lots_consultation", "reframe_to_real_world_support"],
        }
    queries = record["objects"] + record["zones"]
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "casting_lots_interpretation_planner",
        "is_valid": True,
        "can_continue_casting_lots": True,
        "question_text": record["question_text"],
        "casting_system": record["casting_system"],
        "casting_surface": record["casting_surface"],
        "layout_source": record["layout_source"],
        "focus": record["focus"],
        "objects": record["objects"],
        "zones": record["zones"],
        "relationships": record["relationships"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个符物抛掷盘面能帮助用户整理哪种现实问题、可验证线索和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明符物抛掷只作象征反思，不作确定预言、灵异证明或事实证明。",
                "标注符物体系、投掷垫/区域、盘面来源、物件、方位关系和缺失字段。",
                "逐个物件与区域解释象征层，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及遗骸/动物伤害、财务赌博、专业问题、灵异恐惧、第三方窥探、操控或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present casting lots as fact, prediction, diagnosis, spirit confirmation, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not use human remains, animal harm, blood sacrifice, illegal materials, or repeat-casting until the desired answer appears.",
        ],
        "next_steps": ["draft_casting_lots_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
    if args.casting_system:
        payload["casting_system"] = args.casting_system
    if args.casting_surface:
        payload["casting_surface"] = args.casting_surface
    if args.layout_source:
        payload["layout_source"] = args.layout_source
    if args.objects:
        payload["objects"] = args.objects
    if args.zones:
        payload["zones"] = args.zones
    if args.relationships:
        payload["relationships"] = args.relationships
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
    parser.add_argument("--text", help="Casting lots question or request notes.")
    parser.add_argument("--casting-system", help="bone_casting, shell_casting, stone_casting, charm_casting, custom.")
    parser.add_argument("--casting-surface", help="mat, cloth, bowl, floor, table, drawn_zones, unknown.")
    parser.add_argument("--layout-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--objects", help="Cast objects, e.g. shell key stone feather.")
    parser.add_argument("--zones", help="Layout zones, e.g. center left future.")
    parser.add_argument("--relationships", help="Free-text relation notes.")
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
