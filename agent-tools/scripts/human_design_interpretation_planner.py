#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for Human Design chart contexts."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import human_design_chart_recorder
import human_design_symbol_lookup


def build_symbol_plan(query: str, focus: str, layer: str) -> dict[str, Any]:
    try:
        symbol = human_design_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_custom_human_design_symbol",
            "layer": layer,
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是外部应用写法、课程术语或自定义标签；先询问来源和用户理解，不编造固定权威解释。",
            "reflection_questions": ["符号名称、图表层级、来源和用户想整理的现实问题是什么？"],
            "action_guidance": "不编造人格定论、预言、诊断、关系筛选、职业保证或付费压力。",
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
    record = human_design_chart_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_human_design"]:
        return {
            "tool": "human_design_interpretation_planner",
            "is_valid": False,
            "can_continue_human_design": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_human_design_consultation", "reframe_to_real_world_support"],
        }
    symbol_plans: list[dict[str, Any]] = []
    add_if_present(symbol_plans, record["type"], focus, "type")
    add_if_present(symbol_plans, record["authority"], focus, "authority")
    add_if_present(symbol_plans, "profile" if record["profile"] else "", focus, f"profile:{record['profile']}")
    for center in record["centers"]:
        add_if_present(symbol_plans, "defined_center", focus, f"center:{center}")
    for channel in record["channels"]:
        add_if_present(symbol_plans, "channel", focus, f"channel:{channel}")
    for gate in record["gates"]:
        add_if_present(symbol_plans, "gate", focus, f"gate:{gate}")
    return {
        "tool": "human_design_interpretation_planner",
        "is_valid": True,
        "can_continue_human_design": True,
        "question_text": record["question_text"],
        "chart_source": record["chart_source"],
        "data_scope": record["data_scope"],
        "focus": record["focus"],
        "type": record["type"],
        "strategy": record["strategy"],
        "authority": record["authority"],
        "profile": record["profile"],
        "definition": record["definition"],
        "centers": record["centers"],
        "channels": record["channels"],
        "gates": record["gates"],
        "reality_constraints": record["reality_constraints"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_plan": {
            "core_prompt": "这个人类图资料能帮助用户整理哪种自我观察、决策节奏、能量边界和现实下一步？",
            "symbol_count": len(symbol_plans),
            "reading_order": [
                "先声明人类图只作象征反思，不作人格定论、诊断、关系筛选、职业保证或专业建议。",
                "标注资料来源、出生资料最小化范围、已知类型、策略、权威、profile、中心/通道/闸门和缺失字段。",
                "从类型看互动节奏，从权威看决策复盘，从 profile 看学习/互动视角，从中心/通道/闸门看具体观察问题。",
                "把每个象征收束为现实证据、沟通边界、预算/时间限制和 1-3 个可撤回小动作。",
                "若涉及专业替代、第三方隐私、关系筛选、职业/财务保证、操控、付费压力或反复依赖，暂停流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present Human Design as fact, diagnosis, identity destiny, relationship screening, career guarantee, financial advice, or professional advice.",
            "Minimize birth data, avoid third-party charting without consent, and do not create paid-course pressure or repeated dependency.",
        ],
        "next_steps": ["draft_human_design_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for attr in ("text", "chart_source", "data_scope", "type", "strategy", "authority", "profile", "definition", "centers", "channels", "gates", "focus"):
        value = getattr(args, attr)
        if value:
            payload["question_text" if attr == "text" else attr] = value
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
    parser.add_argument("--text", help="Human Design question or request notes.")
    parser.add_argument("--chart-source", help="user_provided, external_app, book_example.")
    parser.add_argument("--data-scope", help="already_generated_chart_preferred, birth_data_minimized.")
    parser.add_argument("--type", help="Human Design type.")
    parser.add_argument("--strategy", help="Strategy from chart.")
    parser.add_argument("--authority", help="Inner authority.")
    parser.add_argument("--profile", help="Profile, e.g. 2/4.")
    parser.add_argument("--definition", help="Definition.")
    parser.add_argument("--centers", help="Centers list.")
    parser.add_argument("--channels", help="Channels list.")
    parser.add_argument("--gates", help="Gates list.")
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
