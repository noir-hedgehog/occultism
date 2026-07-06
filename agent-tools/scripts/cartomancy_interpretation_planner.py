#!/usr/bin/env python3
"""Build a safe symbolic interpretation plan for playing-card cartomancy."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import cartomancy_card_lookup
import cartomancy_draw_recorder


def build_card_plan(card: dict[str, str], focus: str) -> dict[str, Any]:
    card_name = card.get("card", "")
    try:
        symbol = cartomancy_card_lookup.lookup({"query": card_name, "focus": focus})
    except ValueError:
        return {
            "card": card_name,
            "symbol_code": "unknown_or_custom_playing_card",
            "position": card.get("position", ""),
            "orientation": card.get("orientation", "upright"),
            "rank_keywords": [],
            "suit_keywords": [],
            "interpretation_prompt": "这可能是自定义纸牌、花色写法不明或外部应用中的牌面；先要求牌面说明，不编造固定权威含义。",
            "reflection_questions": ["牌面、花色、点数和抽牌来源是什么？", "用户要整理哪个现实问题和低风险下一步？"],
            "action_guidance": "不编造预言、诊断、财富结果或第三方事实。",
        }
    return {
        "card": symbol["canonical_name"],
        "symbol_code": symbol["symbol_code"],
        "position": card.get("position", ""),
        "orientation": card.get("orientation", "upright"),
        "rank_keywords": symbol["rank_keywords"],
        "suit_keywords": symbol["suit_keywords"],
        "interpretation_prompt": symbol["interpretation_prompt"],
        "reflection_questions": symbol["reflection_questions"],
        "action_guidance": symbol["action_guidance"],
    }


def plan(payload: dict[str, Any]) -> dict[str, Any]:
    record = cartomancy_draw_recorder.record(payload)
    focus = str(payload.get("focus", "")).strip() or record["focus"]
    if not record["can_continue_cartomancy"]:
        return {
            "tool": "cartomancy_interpretation_planner",
            "is_valid": False,
            "can_continue_cartomancy": False,
            "question_text": record["question_text"],
            "risk_flags": record["risk_flags"],
            "card_plans": [],
            "interpretation_plan": {},
            "limits": record["safety_notes"],
            "next_steps": ["pause_cartomancy_consultation", "reframe_to_real_world_support"],
        }
    card_plans = [build_card_plan(card, focus) for card in record["cards"]]
    return {
        "tool": "cartomancy_interpretation_planner",
        "is_valid": True,
        "can_continue_cartomancy": True,
        "question_text": record["question_text"],
        "deck_type": record["deck_type"],
        "spread_type": record["spread_type"],
        "draw_source": record["draw_source"],
        "focus": record["focus"],
        "cards": record["cards"],
        "risk_flags": record["risk_flags"],
        "missing_fields": record["missing_fields"],
        "card_plans": card_plans,
        "interpretation_plan": {
            "core_prompt": "这组扑克牌能帮助用户整理哪种现实问题、可验证线索和低风险行动？",
            "card_count": len(card_plans),
            "reading_order": [
                "先声明扑克牌只作象征反思，不作确定预言或事实证明。",
                "标注牌阵、牌面、抽牌来源和缺失字段。",
                "逐张牌解释点数/人物和花色象征，再合成为一个现实问题。",
                "列出 1-3 个可验证、可撤回、非高风险的小动作。",
                "若涉及财务赌博、专业问题、第三方窥探、操控或反复依赖，暂停纸牌流程。",
            ],
        },
        "limits": [
            "Use symbolic and possibility language only.",
            "Do not present playing cards as fact, prediction, diagnosis, gambling advice, investment advice, third-party mind reading, or professional advice.",
            "Do not repeat-draw until the desired answer appears.",
        ],
        "next_steps": ["draft_cartomancy_answer_from_plan", "run_mystic_output_lint", "offer_reality_check_questions"],
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
    if args.spread_type:
        payload["spread_type"] = args.spread_type
    if args.deck_type:
        payload["deck_type"] = args.deck_type
    if args.draw_source:
        payload["draw_source"] = args.draw_source
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
    parser.add_argument("--text", help="Cartomancy question or request notes.")
    parser.add_argument("--cards", help="Drawn cards, comma-separated.")
    parser.add_argument("--spread-type", help="single_card, three_card, line, custom.")
    parser.add_argument("--deck-type", help="standard_52_card, standard_with_jokers, custom.")
    parser.add_argument("--draw-source", help="user_provided, simulated_with_consent, external_app.")
    parser.add_argument("--focus", help="Consultation focus.")
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
