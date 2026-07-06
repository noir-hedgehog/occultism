#!/usr/bin/env python3
"""Build a safe interpretation plan for number-symbol consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import numerology_profile_recorder
import numerology_symbol_lookup


def build_symbol_plan(query: str, focus: str) -> dict[str, Any]:
    symbol = numerology_symbol_lookup.lookup({"query": query, "focus": focus})
    return {
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "symbol_layer": symbol["symbol_layer"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = numerology_profile_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["number_context"]
    if not record["can_continue_numerology"]:
        return {
            "tool": "numerology_interpretation_planner",
            "is_valid": False,
            "can_continue_numerology": False,
            "number_text": record["number_text"],
            "number_context": record["number_context"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_numerology_reading", "remove_sensitive_identifier_or_reframe"],
        }
    queries = [record["number_context"]] + record["digits"][:4]
    symbol_plans = []
    for query in queries:
        try:
            symbol_plans.append(build_symbol_plan(query, focus))
        except ValueError:
            continue
    return {
        "tool": "numerology_interpretation_planner",
        "is_valid": True,
        "can_continue_numerology": True,
        "number_text": record["number_text"],
        "number_context": record["number_context"],
        "digits": record["digits"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": [
            "先确认只处理脱敏数字片段，不展示完整敏感号码。",
            "逐一解释数字的文化象征和个人偏好，不写成命运定论。",
            "把象征偏好放在现实条件之后：隐私、价格、记忆度、读音、可用性。",
            "输出低风险选择建议，不承诺发财、转运、复合或健康结果。",
        ],
        "synthesis": {
            "core_prompt": "这些数字更适合支持哪类偏好、记忆和现实使用条件？",
            "symbol_count": len(symbol_plans),
            "grounded_actions": [
                "先删去或隐藏完整敏感号码，只保留必要尾号。",
                "列出现实优先条件，再把数字象征作为最后一层偏好。",
                "若涉及投资、医疗、法律或第三方判断，暂停数字解读。",
            ],
        },
        "limits": [
            "Use symbolic and preference language only.",
            "Do not collect or reveal sensitive identifiers.",
            "Do not promise wealth, luck, relationship, health, or fate outcomes.",
        ],
        "next_steps": ["draft_numerology_answer_from_plan", "run_mystic_output_lint", "offer_reality_constraint_ranking"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["number_text"] = args.text
    if args.focus:
        payload["focus"] = args.focus
    if payload:
        return payload
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"number_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Number material text.")
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
