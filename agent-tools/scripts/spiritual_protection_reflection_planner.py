#!/usr/bin/env python3
"""Build a safe reflection plan for spiritual protection and cord cutting."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import spiritual_protection_context_recorder
import spiritual_protection_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = spiritual_protection_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_protection_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人联想、情绪线索或现实边界提醒；先询问用户语境，不编造加害者、下咒事实、灵体事实或报复步骤。",
            "reflection_questions": ["它对应哪个边界或现实安全议题？", "有哪些可控边界动作？", "是否像指认、报复、危险仪式或反复依赖？"],
            "action_guidance": "不编造恶眼来源、下咒事实或攻击步骤；只把它放回现实边界、提醒物和可控行动。",
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
    record = spiritual_protection_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_spiritual_protection"]:
        return {
            "tool": "spiritual_protection_reflection_planner",
            "is_valid": False,
            "can_continue_spiritual_protection": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "reflection_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_spiritual_protection_consultation", "reframe_to_boundary_safety_or_professional_support"],
        }
    queries = []
    for group in ([record["protection_focus"]], record["sensations"], record["emotions"], record["symbolic_items"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "spiritual_protection_reflection_planner",
        "is_valid": True,
        "can_continue_spiritual_protection": True,
        "context_text": record["context_text"],
        "protection_focus": record["protection_focus"],
        "trigger_context": record["trigger_context"],
        "sensations": record["sensations"],
        "emotions": record["emotions"],
        "reality_safety_context": record["reality_safety_context"],
        "boundary_actions": record["boundary_actions"],
        "symbolic_items": record["symbolic_items"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "reflection_plan": {
            "core_prompt": "这次恶眼/能量防护/断联请求能怎样被改写为边界整理、现实安全检查和低风险提醒物使用？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把恶眼或负能量语言限制为情绪和边界的象征表达，不指认加害者。",
                "记录触发场景、身体感、情绪和现实安全背景。",
                "列出 1-3 个可控边界动作，例如减少接触、整理通知设置、找可信任的人复盘。",
                "提醒物只用已有、低成本、可逆物件；不制造购买或仪式压力。",
                "设置复盘时间和停止条件，避免反复清理、断联或寻找小人。",
            ],
        },
        "limits": [
            "Use symbolic boundary-reflection language only.",
            "Do not identify attackers, confirm curses, spirit facts, surveillance, third-party privacy, or supernatural proof.",
            "Do not provide retaliation, curse, dangerous ritual, stalking, professional replacement, or coercive relationship control.",
            "Do not encourage expensive purchases or repeated dependency.",
        ],
        "next_steps": ["draft_spiritual_protection_answer_from_plan", "run_mystic_output_lint", "offer_boundary_actions_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "protection_focus", "trigger_context", "sensations", "emotions", "reality_safety_context", "boundary_actions", "symbolic_items", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Spiritual protection notes.")
    parser.add_argument("--protection-focus", help="Protection or cord-cutting focus.")
    parser.add_argument("--trigger-context", help="Triggering situation.")
    parser.add_argument("--sensations", help="Body or energy sensations.")
    parser.add_argument("--emotions", help="User emotions.")
    parser.add_argument("--reality-safety-context", help="Reality safety context.")
    parser.add_argument("--boundary-actions", help="Practical boundary actions.")
    parser.add_argument("--symbolic-items", help="Symbolic items or reminders.")
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
