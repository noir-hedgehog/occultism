#!/usr/bin/env python3
"""Lookup safe symbolic prompts for playing-card cartomancy cards."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


SUITS = {
    "hearts": ("红桃", "感受、关系、价值、照顾", "不承诺恋爱、复合或他人回应。"),
    "spades": ("黑桃", "压力、思考、边界、结束", "不写成灾祸、死亡或必然失败。"),
    "diamonds": ("方片", "资源、交换、工作、现实条件", "不承诺财富、收益或投资结果。"),
    "clubs": ("梅花", "行动、协作、学习、推进", "不写成必须冲动行动或成功保证。"),
}

RANKS = {
    "ace": ("A", "开始、种子、单点焦点"),
    "2": ("2", "二选一、关系、平衡"),
    "3": ("3", "协作、扩展、初步结果"),
    "4": ("4", "结构、稳定、限制"),
    "5": ("5", "变化、摩擦、调整"),
    "6": ("6", "过渡、修复、节奏"),
    "7": ("7", "评估、等待、内在选择"),
    "8": ("8", "重复、练习、推进"),
    "9": ("9", "临近完成、压力或收束"),
    "10": ("10", "完成、负担、阶段总结"),
    "jack": ("J", "消息、学习者、试探行动"),
    "queen": ("Q", "接纳、判断、关系智慧"),
    "king": ("K", "掌控、责任、成熟策略"),
    "joker": ("Joker", "意外、自由牌、规则外因素"),
}

SUIT_ALIASES = {
    "红桃": "hearts",
    "heart": "hearts",
    "hearts": "hearts",
    "♥": "hearts",
    "黑桃": "spades",
    "spade": "spades",
    "spades": "spades",
    "♠": "spades",
    "方片": "diamonds",
    "方块": "diamonds",
    "diamond": "diamonds",
    "diamonds": "diamonds",
    "♦": "diamonds",
    "梅花": "clubs",
    "club": "clubs",
    "clubs": "clubs",
    "♣": "clubs",
}

RANK_ALIASES = {
    "a": "ace",
    "A": "ace",
    "ace": "ace",
    "j": "jack",
    "J": "jack",
    "jack": "jack",
    "q": "queen",
    "Q": "queen",
    "queen": "queen",
    "k": "king",
    "K": "king",
    "king": "king",
    "joker": "joker",
    "Joker": "joker",
    "小王": "joker",
    "大王": "joker",
}


def parse_card(raw: object) -> tuple[str, str]:
    text = str(raw or "").strip()
    if not text:
        raise ValueError("card, query, or symbol is required")
    lowered = text.lower().replace(" of ", " ").replace("-", " ")
    if lowered in ("joker", "小王", "大王"):
        return "joker", "joker"
    for suit_text, suit_code in SUIT_ALIASES.items():
        if suit_text.lower() in lowered or suit_text in text:
            rank_text = text.replace(suit_text, "").strip()
            rank_text = lowered.replace(suit_text.lower(), "").strip() if not rank_text else rank_text
            rank_text = re.sub(r"[^0-9A-Za-z]", "", rank_text) or rank_text
            rank = RANK_ALIASES.get(rank_text, RANK_ALIASES.get(rank_text.upper(), rank_text))
            if rank in RANKS:
                return rank, suit_code
    parts = lowered.split()
    if len(parts) >= 2:
        rank = RANK_ALIASES.get(parts[0], parts[0])
        suit = SUIT_ALIASES.get(parts[-1], parts[-1])
        if rank in RANKS and suit in SUITS:
            return rank, suit
    raise ValueError(f"unknown cartomancy card: {text}")


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    raw_card = payload.get("card", payload.get("query", payload.get("symbol", "")))
    rank, suit = parse_card(raw_card)
    focus = str(payload.get("focus", "")).strip() or "symbolic_reflection"
    if rank == "joker":
        rank_name, rank_keywords = RANKS["joker"][0], RANKS["joker"][1]
        canonical = "Joker"
        suit_name = "无花色"
        suit_keywords = "意外、自由、规则外因素"
        action = "不把 Joker 写成失控、灾祸或必然反转。"
        symbol_code = "joker"
    else:
        rank_name, rank_keywords = RANKS[rank][0], RANKS[rank][1]
        suit_name, suit_keywords, action = SUITS[suit]
        canonical = f"{suit_name}{rank_name}"
        symbol_code = f"{rank}_of_{suit}"
    return {
        "tool": "cartomancy_card_lookup",
        "query": str(raw_card).strip(),
        "canonical_name": canonical,
        "system": "cartomancy_symbolic_reflection",
        "symbol_code": symbol_code,
        "rank": rank,
        "suit": suit,
        "rank_keywords": [part.strip() for part in rank_keywords.split("、") if part.strip()],
        "suit_keywords": [part.strip() for part in suit_keywords.split("、") if part.strip()],
        "interpretation_prompt": f"把「{canonical}」作为扑克牌占卜象征，围绕{focus}整理个人联想、现实证据、边界和低风险下一步。",
        "reflection_questions": [
            "这张牌来自用户已抽结果、模拟同意，还是外部应用？",
            "花色更像情绪、压力、资源，还是行动层面？",
            "点数/人物牌提示的是开始、选择、协作、限制、调整、收束，还是责任策略？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不把扑克牌写成确定预言、事实证明、诊断、财富结果、赌博建议或专业意见。",
            "不使用牌面窥探第三方真实想法、控制他人或决定重大风险事项。",
            "不反复抽牌直到满意。",
        ],
        "next_steps": ["combine_with_cartomancy_draw_record", "prefer_reality_check_and_low_risk_action", "run_mystic_output_lint"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.query:
        return {"query": args.query, "focus": args.focus}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"query": raw}
    raise ValueError("Provide --query, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="Playing card, e.g. 红桃A, 黑桃10, queen hearts.")
    parser.add_argument("--focus", help="Optional consultation focus.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = lookup(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
