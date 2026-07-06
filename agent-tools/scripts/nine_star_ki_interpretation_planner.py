#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for Nine Star Ki contexts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import nine_star_ki_profile_recorder
import nine_star_ki_symbol_lookup


def build_symbol_plan(query: str, focus: str, layer: str) -> dict[str, Any]:
    try:
        symbol = nine_star_ki_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_nine_star_symbol",
            "layer": layer,
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是自定义命星、派别差异或外部应用写法；先询问来源和计算规则，不编造固定权威解释。",
            "reflection_questions": ["命星名称、计算来源、节气边界和所在层级是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果、方位恐吓或第三方真实想法。",
        }
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "layer": layer,
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def add_if_present(plans: list[dict[str, Any]], query: str, focus: str, layer: str) -> None:
    if query:
        plans.append(build_symbol_plan(query, focus, layer))


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = nine_star_ki_profile_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_nine_star_ki"]:
        return {
            "tool": "nine_star_ki_interpretation_planner",
            "is_valid": False,
            "can_continue_nine_star_ki": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_nine_star_ki_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans: list[dict[str, Any]] = []
    add_if_present(symbol_plans, record["home_star"], focus, "home_star")
    add_if_present(symbol_plans, record["month_star"], focus, "month_star")
    add_if_present(symbol_plans, record["annual_star"], focus, "annual_star")
    for direction in record["directions"]:
        add_if_present(symbol_plans, "direction", focus, f"direction:{direction}")
    return {
        "tool": "nine_star_ki_interpretation_planner",
        "is_valid": True,
        "can_continue_nine_star_ki": True,
        "question_text": record["question_text"],
        "system_variant": record["system_variant"],
        "source": record["source"],
        "focus": record["focus"],
        "birth_year": record["birth_year"],
        "birth_month": record["birth_month"],
        "current_year": record["current_year"],
        "home_star": record["home_star"],
        "month_star": record["month_star"],
        "annual_star": record["annual_star"],
        "directions": record["directions"],
        "reality_constraints": record["reality_constraints"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个九星气学资料能帮助用户整理哪种现实主题、节奏提醒和低风险行动？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明九星气学只作象征反思，不作确定预言、方位恐吓、关系标签或专业建议。",
                "标注出生年份/已知命星、节气边界、体系来源、年星、方位焦点和缺失字段。",
                "从本命星看长期惯性，从年星看阶段提醒，从方位看空间/动线的低成本整理。",
                "把每个象征收束为现实证据、预算/时间约束、沟通边界和 1-3 个可撤回小动作。",
                "若涉及医疗、投资、搬迁恐惧、关系筛选、高价化解、第三方窥探、操控或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present Nine Star Ki as fact, prediction, diagnosis, relationship screening, gambling advice, investment advice, moving command, or professional advice.",
            "Do not create direction fear, expensive cure pressure, or repeated calculation dependency.",
        ],
        "next_steps": ["draft_nine_star_ki_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
    if args.birth_year:
        payload["birth_year"] = args.birth_year
    if args.birth_month:
        payload["birth_month"] = args.birth_month
    if args.current_year:
        payload["current_year"] = args.current_year
    if args.home_star:
        payload["home_star"] = args.home_star
    if args.month_star:
        payload["month_star"] = args.month_star
    if args.annual_star:
        payload["annual_star"] = args.annual_star
    if args.directions:
        payload["directions"] = args.directions
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
    parser.add_argument("--text", help="Nine Star Ki question or request notes.")
    parser.add_argument("--birth-year", help="Birth year or known year context.")
    parser.add_argument("--birth-month", help="Birth month if relevant to the user's system.")
    parser.add_argument("--current-year", help="Current year for annual star context.")
    parser.add_argument("--home-star", help="Known home/birth star.")
    parser.add_argument("--month-star", help="Known month star.")
    parser.add_argument("--annual-star", help="Known annual star.")
    parser.add_argument("--directions", help="Direction focus list.")
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
