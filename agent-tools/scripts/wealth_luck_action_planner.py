#!/usr/bin/env python3
"""Build a safe action plan for wealth-luck and prosperity-symbol requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import wealth_luck_context_recorder
import wealth_luck_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    try:
        symbol = wealth_luck_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "symbol": query,
            "symbol_code": "unknown_or_personal_wealth_symbol",
            "category": "custom",
            "keywords": [],
            "interpretation_prompt": "这可能是私人资源、职业或消费联想；先询问语境，不编造发财、投资收益、财神命令或法事必要性。",
            "reflection_questions": ["它对应收入、预算、客户、技能还是消费边界？", "有哪些可控行动？", "是否像投资建议、收益保证、高价法事或反复依赖？"],
            "action_guidance": "不编造发财或回本承诺；只放回预算、收入渠道、职业动作和复盘。",
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
    record = wealth_luck_context_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_wealth_luck"]:
        return {
            "tool": "wealth_luck_action_planner",
            "is_valid": False,
            "can_continue_wealth_luck": False,
            "context_text": record["context_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "action_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_wealth_luck_consultation", "reframe_to_budget_action_or_professional_support"],
        }
    queries = []
    for group in ([record["wealth_focus"]], record["income_channels"], record["existing_symbols"], record["practical_actions"]):
        for item in group:
            if item and item not in queries:
                queries.append(item)
    symbol_plans = [build_symbol_plan(query, focus) for query in queries]
    return {
        "tool": "wealth_luck_action_planner",
        "is_valid": True,
        "can_continue_wealth_luck": True,
        "context_text": record["context_text"],
        "wealth_focus": record["wealth_focus"],
        "current_context": record["current_context"],
        "income_channels": record["income_channels"],
        "budget_boundaries": record["budget_boundaries"],
        "existing_symbols": record["existing_symbols"],
        "practical_actions": record["practical_actions"],
        "risk_notes": record["risk_notes"],
        "review_time": record["review_time"],
        "stop_condition": record["stop_condition"],
        "focus": record["focus"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "action_plan": {
            "core_prompt": "这次招财/财运请求能怎样被改写为预算、收入渠道、职业行动、消费边界和复盘提醒？",
            "symbol_count": len(symbol_plans),
            "practical_steps": [
                "把招财或财库语言限制为资源整理和行动提醒，不承诺发财或收益。",
                "记录当前收入渠道、预算边界、已有物件、现实风险和可控行动。",
                "列出 1-3 个可控动作，例如记账、跟进客户、整理报价、更新作品集、设消费上限。",
                "招财物件只用已有、低成本、可撤回物件；不制造购买或法事压力。",
                "设置复盘时间和停止条件，避免反复求财、查财运或冲动消费。",
            ],
        },
        "limits": [
            "Use symbolic prosperity, budget, income-channel, and grounded-action language only.",
            "Do not promise wealth, returns, luck changes, deity guarantees, or supernatural financial effects.",
            "Do not provide investment, debt, lottery, gambling, tax, legal, fraud, or professional financial advice.",
            "Do not encourage expensive rituals, paid prosperity packages, manipulative sales, illegal profit, or repeated dependency.",
        ],
        "next_steps": ["draft_wealth_luck_answer_from_plan", "run_mystic_output_lint", "offer_budget_actions_and_stop_condition"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    for key in ("text", "wealth_focus", "current_context", "income_channels", "budget_boundaries", "existing_symbols", "practical_actions", "risk_notes", "review_time", "stop_condition", "focus"):
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
    parser.add_argument("--text", help="Wealth-luck notes.")
    parser.add_argument("--wealth-focus", help="Wealth or prosperity focus.")
    parser.add_argument("--current-context", help="Current money or work context.")
    parser.add_argument("--income-channels", help="Income channels.")
    parser.add_argument("--budget-boundaries", help="Budget boundaries.")
    parser.add_argument("--existing-symbols", help="Existing symbols or reminder items.")
    parser.add_argument("--practical-actions", help="Practical actions.")
    parser.add_argument("--risk-notes", help="Risk notes.")
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
