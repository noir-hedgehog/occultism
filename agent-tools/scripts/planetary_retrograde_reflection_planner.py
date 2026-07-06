#!/usr/bin/env python3
"""Build a safe reflection plan for planetary retrograde and astrology weather."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import planetary_retrograde_context_recorder
import planetary_retrograde_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = planetary_retrograde_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_retrograde_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人联想、现实事项或星象背景词；先询问用户语境，不编造灾祸、行星惩罚、未来保证或第三方读心。",
            "reflection_questions": ["它对应哪个现实事项？", "有哪些可控检查或复盘动作？", "是否像宿命归因、专业替代或反复查询？"],
            "action_guidance": "不编造行星惩罚或必然结果；只把它放回现实事项、复盘时间和可控行动。",
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
    record = planetary_retrograde_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_planetary_retrograde"]:
        return {
            "tool": "planetary_retrograde_reflection_planner",
            "is_valid": False,
            "can_continue_planetary_retrograde": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_planetary_retrograde_consultation", "reframe_to_grounded_review_or_professional_support"],
        }
    queries = []
    for group in ([record["retrograde_focus"]], record["affected_areas"], record["emotions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "planetary_retrograde_reflection_planner",
        "is_valid": True,
        "can_continue_planetary_retrograde": True,
        "context_text": record["context_text"],
        "retrograde_focus": record["retrograde_focus"],
        "affected_areas": record["affected_areas"],
        "current_events": record["current_events"],
        "emotions": record["emotions"],
        "reality_constraints": record["reality_constraints"],
        "practical_actions": record["practical_actions"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次水逆/行星逆行请求能怎样被改写为沟通检查、备份、复盘和节奏调整？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把星象作为背景语言，不把延迟或冲突全部归因给水逆。",
                "列出正在发生的现实事项、已知限制和需要确认的信息。",
                "安排 1-3 个可控动作，例如备份文件、确认时间、复核合同摘要、延后非必要争执。",
                "涉及专业事项时转向现实资料和专业支持，不用星象替代判断。",
                "设置复盘时间和停止查询条件，避免每天反复查星象寻求确定感。",
            ],
        },
        "limits": [
            "Use astrology-weather language as symbolic reflection only.",
            "Do not claim inevitable misfortune, planetary punishment, professional advice, third-party mind reading, or fate certainty.",
            "Do not replace medical, legal, financial, career, mental-health, or safety judgment.",
            "Do not encourage dangerous rituals, expensive remedial purchases, or repeated dependency.",
        ],
        "next_steps": ["draft_planetary_retrograde_answer_from_plan", "run_mystic_output_lint", "offer_review_checklist_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "retrograde_focus", "affected_areas", "current_events", "emotions", "reality_constraints", "practical_actions", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Planetary retrograde notes.")
    parser.add_argument("--retrograde-focus", help="Retrograde or astrology-weather focus.")
    parser.add_argument("--affected-areas", help="Affected life/work areas.")
    parser.add_argument("--current-events", help="Current grounded events.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--reality-constraints", help="Reality constraints.")
    parser.add_argument("--practical-actions", help="Practical actions.")
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
