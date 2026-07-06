#!/usr/bin/env python3
"""Build a safe symbolic plan for moon-phase/lunar-cycle reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import moon_phase_context_recorder
import moon_phase_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = moon_phase_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_source_specific_moon_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是具体日历、应用、课程或私人说法；先询问来源，不编造天文或仪式权威。",
            "reflection_questions": ["这个月相或术语来自哪里？", "用户希望整理哪个现实主题？", "可复盘的小行动是什么？"],
            "action_guidance": "不编造显化保证、灾祸预言、天文权威、仪式必要性或第三方结论。",
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
    record = moon_phase_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_moon_phase"]:
        return {
            "tool": "moon_phase_reflection_planner",
            "is_valid": False,
            "can_continue_moon_phase": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_moon_phase_consultation", "reframe_to_real_world_support_or_safe_reflection"],
        }
    queries = []
    for group in (record["phases"], record["themes"], record["intentions"]):
        for item in group:
            if item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "moon_phase_reflection_planner",
        "is_valid": True,
        "can_continue_moon_phase": True,
        "context_text": record["context_text"],
        "phases": record["phases"],
        "themes": record["themes"],
        "intentions": record["intentions"],
        "practical_constraints": record["practical_constraints"],
        "date_note": record["date_note"],
        "source_note": record["source_note"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这个月相周期能怎样帮助用户整理意图、复盘现实进展、调整约束并选择下一步？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "先注明月相来源：用户提供、日历、应用或文化学习；不声称实时天文计算。",
                "把月相解释写成周期隐喻，例如开始、推进、复盘、整理或休息。",
                "将愿望改写成可执行行动：一个小任务、一个沟通、一项复盘或一个可停止的记录练习。",
                "涉及医疗/生育/心理健康、投资赌博、关系操控、危险仪式或强烈依赖时暂停象征流程。",
                "优先无火、低成本、可复盘动作：写意图、整理清单、检查日程、休息、联系现实支持。",
            ],
        },
        "limits": [
            "Use symbolic cycle-reflection language only.",
            "Do not present moon phases as astronomical authority, manifestation guarantee, disaster prediction, fertility or medical advice, financial signal, relationship proof, or professional advice.",
            "Do not create dangerous ritual steps, paid-course pressure, third-party coercion, or repeated dependency.",
        ],
        "next_steps": ["draft_moon_phase_answer_from_plan", "run_mystic_output_lint", "offer_grounding_and_real_world_action_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "phases", "themes", "intentions", "practical_constraints", "date_note", "source_note", "focus"):
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
    parser.add_argument("--text", help="Moon-phase/lunar-cycle context notes.")
    parser.add_argument("--phases", help="Moon phases.")
    parser.add_argument("--themes", help="Reflection themes.")
    parser.add_argument("--intentions", help="Intentions or review items.")
    parser.add_argument("--practical-constraints", help="Real-world constraints.")
    parser.add_argument("--date-note", help="Date/time note.")
    parser.add_argument("--source-note", help="Calendar, app, or user-provided source note.")
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
