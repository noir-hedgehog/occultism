#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for Western geomancy charts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import western_geomancy_chart_recorder
import western_geomancy_figure_lookup


def build_figure_plan(query: str, focus: str, position: str) -> dict[str, Any]:
    try:
        symbol = western_geomancy_figure_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "figure": query,
            "figure_code": "unknown_or_custom_geomancy_figure",
            "position": position,
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是自定义图形、拼写差异或外部应用写法；先询问图形来源和用户约定，不编造固定权威解释。",
            "reflection_questions": ["图形名称、四行点形和所在位置是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果、灵异事实或第三方真实想法。",
        }
    return {
        "figure": symbol["canonical_name"],
        "figure_code": symbol["figure_code"],
        "position": position,
        "category": symbol["category"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def extend_with_position(plans: list[dict[str, Any]], figures: list[str], position: str, focus: str) -> None:
    for figure in figures:
        plans.append(build_figure_plan(figure, focus, position))


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = western_geomancy_chart_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_western_geomancy"]:
        return {
            "tool": "western_geomancy_interpretation_planner",
            "is_valid": False,
            "can_continue_western_geomancy": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "figure_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_western_geomancy_consultation", "reframe_to_real_world_support"],
        }
    figure_plans: list[dict[str, Any]] = []
    extend_with_position(figure_plans, record["mothers"], "mother", focus)
    extend_with_position(figure_plans, record["daughters"], "daughter", focus)
    extend_with_position(figure_plans, record["nieces"], "niece", focus)
    extend_with_position(figure_plans, record["witnesses"], "witness", focus)
    extend_with_position(figure_plans, record["judge"], "judge", focus)
    return {
        "tool": "western_geomancy_interpretation_planner",
        "is_valid": True,
        "can_continue_western_geomancy": True,
        "question_text": record["question_text"],
        "chart_source": record["chart_source"],
        "generation_method": record["generation_method"],
        "focus": record["focus"],
        "mothers": record["mothers"],
        "daughters": record["daughters"],
        "nieces": record["nieces"],
        "witnesses": record["witnesses"],
        "judge": record["judge"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "figure_plans": figure_plans,
        "interpretation_plan": {
            "core_prompt": "这个西洋土占盾形盘能帮助用户整理哪种现实问题、可验证线索和低风险行动？",
            "figure_count": len(figure_plans),
            "reading_order": [
                "先声明西洋土占只作象征反思，不作确定预言、灵异证明或事实证明。",
                "标注起盘来源、四行点/外部应用方法、母亲图、女儿图、侄子图、见证者、裁判者和缺失字段。",
                "从母亲图看输入条件，从见证者看两侧张力，从裁判者收束成一个复盘问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及财务赌博、专业问题、灵异恐惧、第三方窥探、操控或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present geomantic figures as fact, prediction, diagnosis, spirit confirmation, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not repeat-chart until the desired answer appears.",
        ],
        "next_steps": ["draft_western_geomancy_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
    if args.chart_source:
        payload["chart_source"] = args.chart_source
    if args.generation_method:
        payload["generation_method"] = args.generation_method
    if args.mothers:
        payload["mothers"] = args.mothers
    if args.daughters:
        payload["daughters"] = args.daughters
    if args.nieces:
        payload["nieces"] = args.nieces
    if args.witnesses:
        payload["witnesses"] = args.witnesses
    if args.judge:
        payload["judge"] = args.judge
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
    parser.add_argument("--text", help="Western geomancy question or request notes.")
    parser.add_argument("--chart-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--generation-method", help="four_line_points, app_generated, historical_example, custom.")
    parser.add_argument("--mothers", help="Four mother figures.")
    parser.add_argument("--daughters", help="Daughter figures.")
    parser.add_argument("--nieces", help="Niece figures.")
    parser.add_argument("--witnesses", help="Two witness figures.")
    parser.add_argument("--judge", help="Judge figure.")
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
