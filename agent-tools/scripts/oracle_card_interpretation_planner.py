#!/usr/bin/env python3
"""Build a safe interpretation plan for oracle-card readings."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import oracle_card_draw_recorder
import oracle_card_symbol_lookup


def build_symbol_plan(query: str, focus: str, position: str) -> dict[str, Any]:
    try:
        symbol = oracle_card_symbol_lookup.lookup({"query": query, "focus": focus})
    except ValueError:
        return {
            "position": position,
            "symbol": query,
            "symbol_code": "deck_specific_or_unknown",
            "keywords": [],
            "interpretation_prompt": "这可能是特定神谕卡牌组中的牌名或关键词；先要求用户提供牌面文字、图像元素或牌组说明。",
            "reflection_questions": ["牌组名称和牌面原文是什么？", "牌面上有哪些可见图像、关键词或颜色？"],
            "action_guidance": "不编造该牌组的固定权威牌义。",
        }
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
    record = oracle_card_draw_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["spread_type"]
    if not record["can_continue_oracle_card"]:
        return {
            "tool": "oracle_card_interpretation_planner",
            "is_valid": False,
            "can_continue_oracle_card": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "symbol_plans": [],
            "interpretation_layers": [],
            "synthesis": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_oracle_card_reading", "reframe_to_real_world_support"],
        }
    positions = record["positions"]
    symbol_plans = []
    for index, card in enumerate(record["cards"]):
        position = positions[index] if index < len(positions) else f"card_{index + 1}"
        symbol_plans.append(build_symbol_plan(card, focus, position))
    return {
        "tool": "oracle_card_interpretation_planner",
        "is_valid": True,
        "can_continue_oracle_card": True,
        "question_text": record["question_text"],
        "deck_name": record["deck_name"],
        "spread_type": record["spread_type"],
        "positions": positions,
        "cards": record["cards"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "symbol_plans": symbol_plans,
        "interpretation_layers": [
            "先说明神谕卡只作图像、关键词和个人联想的象征反思，不证明事实或替用户决定。",
            "确认牌组名称、牌名/关键词和抽牌来源；缺少牌组说明时不编造权威牌义。",
            "逐张整理图像母题、用户联想、现实证据和低风险下一步。",
            "把现实证据、专业边界、当事人沟通和用户价值排序放在象征之前。",
            "若出现依赖、恐惧、专业替代、财务投机或第三方操控，暂停神谕卡流程。",
        ],
        "synthesis": {
            "core_prompt": "这组神谕卡能帮助用户澄清哪种感受、价值排序、现实条件或低风险下一步？",
            "symbol_count": len(symbol_plans),
            "grounded_actions": [
                "把牌面关键词拆成感受、事实和行动三列。",
                "对每张牌给出一个可验证、可撤回或可暂停的现实动作。",
                "为同一问题设置停止追问条件，避免反复依赖。",
            ],
        },
        "limits": [
            "Use symbolic reflection language only.",
            "Do not present oracle cards as fact, diagnosis, prediction, spirit command, or instruction.",
            "Do not decide medical, legal, financial, safety, or third-party matters.",
        ],
        "next_steps": ["draft_oracle_card_answer_from_plan", "run_mystic_output_lint", "offer_reality_evidence_checklist"],
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
    if args.cards:
        payload["cards"] = args.cards
    if args.deck_name:
        payload["deck_name"] = args.deck_name
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
    parser.add_argument("--text", help="Oracle-card question or session notes.")
    parser.add_argument("--cards", help="Drawn cards or motifs separated by punctuation or spaces.")
    parser.add_argument("--deck-name", help="Deck/source name if known.")
    parser.add_argument("--spread-type", help="single_card, three_card_reflection, or past_present_next.")
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
