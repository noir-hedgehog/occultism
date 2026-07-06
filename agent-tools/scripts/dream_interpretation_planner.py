#!/usr/bin/env python3
"""Build a safe interpretation plan for symbolic dream consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import dream_record_builder
import dream_symbol_lookup


def build_symbol_plan(symbol: str, focus: str) -> dict[str, Any]:
    lookup = dream_symbol_lookup.lookup({"query": symbol, "focus": focus})
    return {
        "symbol": lookup["canonical_name"],
        "symbol_code": lookup["symbol_code"],
        "symbol_layer": lookup["symbol_layer"],
        "keywords": lookup["keywords"],
        "interpretation_prompt": lookup["interpretation_prompt"],
        "reflection_questions": lookup["reflection_questions"],
        "action_guidance": lookup["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = dream_record_builder.build(payload)
    if not record["can_continue_dream_reflection"]:
        return {
            "tool": "dream_interpretation_planner",
            "is_valid": False,
            "can_continue_dream_reflection": False,
            "dream_excerpt": record["dream_excerpt"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_dream_symbolic_reading", "offer_sleep_or_mental_health_support_if_needed"],
        }
    symbols = record["symbol_candidates"][:3]
    focus = record["user_goal"]
    symbol_plans = []
    for symbol in symbols:
        try:
            symbol_plans.append(build_symbol_plan(symbol, focus))
        except ValueError:
            continue
    layers = [
        "先重述梦境素材和醒后感受，不补写用户没说的细节。",
        "逐一解释主要符号的象征层，而不是给出单一答案。",
        "把符号连接到现实压力、关系、变化、身体疲劳或创作主题。",
        "收束为 1-3 个低风险现实动作或反思问题。",
    ]
    if not symbol_plans:
        layers.insert(1, "如果符号库没有命中，优先询问用户个人联想。")
    return {
        "tool": "dream_interpretation_planner",
        "is_valid": True,
        "can_continue_dream_reflection": True,
        "dream_excerpt": record["dream_excerpt"],
        "user_goal": record["user_goal"],
        "emotion_labels": record["emotion_labels"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": layers,
        "synthesis": {
            "core_prompt": "这个梦最适合被当成哪类现实感受或变化的象征材料？",
            "reality_anchor": record["waking_context"] or "需要补问最近现实背景后再综合。",
            "grounded_actions": [
                "写下梦里最强烈的感受和现实中的相似场景。",
                "选择一个可控的小行动处理现实压力或边界。",
                "若梦境反复影响睡眠，优先寻求现实支持。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not diagnose, predict death or disaster, or confirm supernatural causation.",
            "Repeated nightmares, trauma cues, severe distress, or sleep impairment require real-world support.",
        ],
        "next_steps": ["draft_dream_answer_from_plan", "run_mystic_output_lint", "offer_journaling_or_grounding_step"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    payload: dict[str, Any] = {}
    if args.text:
        payload["dream_text"] = args.text
    if args.context:
        payload["waking_context"] = args.context
    if args.goal:
        payload["user_goal"] = args.goal
    if payload:
        return payload
    if not sys.stdin.isatty():
        return json.loads(sys.stdin.read())
    raise ValueError("Provide --text, --json, --file, or JSON stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Dream text.")
    parser.add_argument("--context", help="Recent waking-life context.")
    parser.add_argument("--goal", help="User goal.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON object input.")
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
