#!/usr/bin/env python3
"""Build a safe symbolic plan for synchronicity reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import synchronicity_event_recorder
import synchronicity_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = synchronicity_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_synchronicity_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人联想、情绪线索或场景提醒；先询问用户自己的语境，不编造宇宙命令、天使/灵体事实、未来保证或第三方读心。",
            "reflection_questions": ["它自然出现在哪里？", "它和哪些现实议题、情绪或行动有关？", "是否像命令、专业替代、读心或反复确认？"],
            "action_guidance": "不编造来源、不下命令、不保证结果；只把它放回用户的现实锚点和可控行动。",
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
    record = synchronicity_event_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_synchronicity"]:
        return {
            "tool": "synchronicity_reflection_planner",
            "is_valid": False,
            "can_continue_synchronicity": False,
            "event_text": record["event_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_synchronicity_consultation", "reframe_to_grounded_safety_or_professional_support"],
        }
    queries = []
    for group in (record["repeated_signs"], record["emotions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "synchronicity_reflection_planner",
        "is_valid": True,
        "can_continue_synchronicity": True,
        "event_text": record["event_text"],
        "repeated_signs": record["repeated_signs"],
        "frequency_context": record["frequency_context"],
        "situation_context": record["situation_context"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "practical_actions": record["practical_actions"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次同步性请求能怎样被改写为重复征兆记录、情绪整理、现实锚点和可控行动？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "只记录自然出现的符号、场景、频率和当时情绪，不主动危险寻找。",
                "把象征解释限制为用户的注意力、情绪主题和现实锚点，不写成外部命令。",
                "列出 1-3 个低风险可控行动，例如记录睡眠、调整出门时间、整理任务清单。",
                "涉及财务、职业、医疗、法律或心理健康问题时，转向现实信息和专业支持。",
                "设置停止条件和复盘时间，避免每天反复确认数字寻求确定感。",
            ],
        },
        "limits": [
            "Use symbolic journaling and low-risk reflection language only.",
            "Do not claim cosmic commands, angel/spirit facts, future guarantees, professional advice, third-party mind reading, or supernatural proof.",
            "Do not encourage checking signs while driving, crossing roads, or in unsafe contexts.",
            "Do not encourage expensive decoding purchases or repeated dependency.",
        ],
        "next_steps": ["draft_synchronicity_answer_from_plan", "run_mystic_output_lint", "offer_grounded_tracking_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "repeated_signs", "frequency_context", "situation_context", "emotions", "reality_anchor", "practical_actions", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["event_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"event_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Synchronicity notes.")
    parser.add_argument("--repeated-signs", help="Repeated signs or motifs.")
    parser.add_argument("--frequency-context", help="Frequency notes.")
    parser.add_argument("--situation-context", help="Situation notes.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--practical-actions", help="Practical actions.")
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
