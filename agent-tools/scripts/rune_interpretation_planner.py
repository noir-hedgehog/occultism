#!/usr/bin/env python3
"""Build a safe interpretation plan for rune divination."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import rune_cast_recorder
import rune_symbol_lookup


def build_symbol_plan(query: str, focus: str, position: str) -> dict[str, Any]:
    symbol = rune_symbol_lookup.lookup({"query": query, "focus": focus})
    return {
        "position": position,
        "symbol": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "keywords": symbol["keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = rune_cast_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["spread_type"]
    if not record["can_continue_rune"]:
        return {
            "tool": "rune_interpretation_planner",
            "is_valid": False,
            "can_continue_rune": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_rune_reading", "reframe_to_real_world_support"],
        }
    positions = record["positions"]
    symbol_plans = []
    for index, rune in enumerate(record["runes"]):
        position = positions[index] if index < len(positions) else f"rune_{index + 1}"
        try:
            symbol_plans.append(build_symbol_plan(rune, focus, position))
        except ValueError:
            symbol_plans.append(
                {
                    "position": position,
                    "symbol": rune,
                    "symbol_code": "unknown",
                    "keywords": [],
                    "interpretation_prompt": "用户提供的符文不在当前索引中；先要求确认拼写或来源。",
                    "reflection_questions": ["是否为 Elder Futhark 符文？", "是否需要用户补充来源或图片转写？"],
                    "action_guidance": "不强行解释未知符文。",
                }
            )
    return {
        "tool": "rune_interpretation_planner",
        "is_valid": True,
        "can_continue_rune": True,
        "question_text": record["question_text"],
        "spread_type": record["spread_type"],
        "positions": positions,
        "runes": record["runes"],
        "orientation_policy": record["orientation_policy"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": [
            "先说明符文只作象征反思和文化解释，不证明事实或替用户决定。",
            "确认牌阵位置和抽取来源，未知符文先要求确认。",
            "逐枚解释符文关键词，并绑定到位置问题。",
            "把现实证据、专业边界、当事人沟通和用户价值排序放在象征之前。",
            "若出现依赖、恐惧、专业替代、财务投机或第三方操控，暂停符文流程。",
        ],
        "synthesis": {
            "core_prompt": "这组符文能帮助用户澄清哪个资源、阻力、边界或低风险下一步？",
            "symbol_count": len(symbol_plans),
            "grounded_actions": [
                "把解读拆成现实事实、个人偏好和下一步行动三列。",
                "对每个符文提示给出一个可核查或可撤回的行动。",
                "为同一问题设置停止追问条件，避免反复依赖。",
            ],
        },
        "limits": [
            "Use symbolic reflection language only.",
            "Do not present rune results as fact, diagnosis, prediction, curse confirmation, or instruction.",
            "Do not decide medical, legal, financial, safety, or third-party matters.",
        ],
        "next_steps": ["draft_rune_answer_from_plan", "run_mystic_output_lint", "offer_reality_evidence_checklist"],
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
    if args.runes:
        payload["runes"] = args.runes
    if args.spread_type:
        payload["spread_type"] = args.spread_type
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
    parser.add_argument("--text", help="Rune question or session notes.")
    parser.add_argument("--runes", help="Drawn runes separated by space, comma, or Chinese comma.")
    parser.add_argument("--spread-type", help="single_rune, three_rune, or past_present_future.")
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
