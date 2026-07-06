#!/usr/bin/env python3
"""Build a safe symbolic plan for manifestation and intention reflection."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import manifestation_intention_recorder
import manifestation_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = manifestation_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_manifestation_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人象征、愿望措辞或场景线索；先询问用户自己的联想，不编造宇宙回应、神灵命令或结果保证。",
            "reflection_questions": ["这个象征来自哪里？", "它对应哪个现实行动或约束？", "是否像结果保证、专业替代或第三方操控？"],
            "action_guidance": "不编造显化成功、命运保证、神灵事实、第三方讯息或确定结论。",
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
    record = manifestation_intention_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_manifestation"]:
        return {
            "tool": "manifestation_reflection_planner",
            "is_valid": False,
            "can_continue_manifestation": False,
            "intention_text": record["intention_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_manifestation_consultation", "reframe_to_grounded_action_or_real_world_support"],
        }
    queries = []
    for group in ([record["wish_theme"], record["intention_statement"]], record["symbols"], record["emotions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "manifestation_reflection_planner",
        "is_valid": True,
        "can_continue_manifestation": True,
        "intention_text": record["intention_text"],
        "wish_theme": record["wish_theme"],
        "intention_statement": record["intention_statement"],
        "symbols": record["symbols"],
        "emotions": record["emotions"],
        "reality_anchor": record["reality_anchor"],
        "controllable_actions": record["controllable_actions"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这个愿望能怎样被改写为低风险意图、现实约束、可控行动和复盘节奏？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把愿望改写成不保证结果的意图句。",
                "列出用户可控的 1-3 个行动和不可控因素。",
                "为每个象征只保留提醒功能，不写成宇宙保证、命令或成功率。",
                "设置复盘时间和停止条件，避免反复许愿寻求确定感。",
                "涉及医疗、法律、财务、安全或心理健康时，转向现实专业支持。",
            ],
        },
        "limits": [
            "Use symbolic intention-setting language only.",
            "Do not promise manifestation success, divine command, fate guarantee, third-party control, curse, revenge, or supernatural proof.",
            "Do not replace medical/legal/financial/mental-health support, emergency help, or practical decision-making.",
            "Do not encourage dangerous rituals, ingestion, blood, unsafe fire, expensive purchases, or repeated dependency.",
        ],
        "next_steps": ["draft_manifestation_answer_from_plan", "run_mystic_output_lint", "offer_grounded_action_and_review_options"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "wish_theme", "intention_statement", "symbols", "emotions", "reality_anchor", "controllable_actions", "review_time", "stop_condition", "focus"):
        value = getattr(args, key)
        if value:
            payload["intention_text" if key == "text" else key] = value
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"intention_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Manifestation intention notes.")
    parser.add_argument("--wish-theme", help="Wish theme.")
    parser.add_argument("--intention-statement", help="Grounded intention statement.")
    parser.add_argument("--symbols", help="Symbols or objects.")
    parser.add_argument("--emotions", help="Emotions.")
    parser.add_argument("--reality-anchor", help="Current practical anchor.")
    parser.add_argument("--controllable-actions", help="Controllable actions.")
    parser.add_argument("--review-time", help="Review time.")
    parser.add_argument("--stop-condition", help="Stop condition.")
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
