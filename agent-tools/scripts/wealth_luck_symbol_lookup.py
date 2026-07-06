#!/usr/bin/env python3
"""Lookup safe symbolic prompts for wealth-luck and prosperity motifs."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


SYMBOLS = {
    "wealth_luck": ("财运/招财", "theme", "资源、机会、现金流、行动提醒", "只作为资源整理和行动提醒，不承诺发财或收益。"),
    "wealth_vault": ("财库/开财库/补财库", "metaphor", "预算、储蓄、漏洞、账目整理", "改写成预算盘点和现金流整理，不提供法事或回本承诺。"),
    "caishen": ("财神", "deity_motif", "感恩、职业伦理、资源流动、节庆文化", "只作文化象征和职业行动提醒，不确认神明保证。"),
    "pixiu": ("貔貅", "object", "守护资源、入口边界、消费提醒", "不写成必招财或必须购买；已有物件可作预算提醒。"),
    "money_frog": ("金蟾", "object", "收支循环、客户入口、节制", "不承诺客流或财运；转成客户跟进和账款复盘。"),
    "wealth_bowl": ("聚宝盆", "object", "收纳、积累、清单、资源容器", "不承诺聚财；转成票据、账单和目标清单整理。"),
    "red_envelope": ("红包/利是", "object", "祝福、流动、边界、礼尚往来", "不诱导超预算送礼或借贷；保留预算边界。"),
    "ledger": ("账本/记账", "practice", "看见现金流、复盘、取舍、计划", "作为现实行动，不替代专业财务建议。"),
}

ALIASES = {
    "招财": "wealth_luck",
    "财运": "wealth_luck",
    "求财": "wealth_luck",
    "旺财": "wealth_luck",
    "wealth luck": "wealth_luck",
    "prosperity": "wealth_luck",
    "财库": "wealth_vault",
    "开财库": "wealth_vault",
    "补财库": "wealth_vault",
    "财神": "caishen",
    "貔貅": "pixiu",
    "金蟾": "money_frog",
    "聚宝盆": "wealth_bowl",
    "红包": "red_envelope",
    "利是": "red_envelope",
    "账本": "ledger",
    "记账": "ledger",
    "ledger": "ledger",
}


def normalize(raw: object) -> str:
    text = str(raw or "").strip()
    lowered = text.lower().replace(" ", "_").replace("-", "_")
    if lowered in SYMBOLS:
        return lowered
    if text.lower() in ALIASES or text in ALIASES:
        return ALIASES.get(text.lower(), ALIASES.get(text, lowered))
    for alias, code in ALIASES.items():
        if alias.lower() in text.lower():
            return code
    return lowered


def lookup(payload: dict[str, Any]) -> dict[str, Any]:
    code = normalize(payload.get("query", payload.get("symbol", "")))
    if not code:
        raise ValueError("query or symbol is required")
    if code not in SYMBOLS:
        raise ValueError(f"unknown wealth luck symbol: {code}")
    canonical, category, keywords_raw, action = SYMBOLS[code]
    focus = str(payload.get("focus", "")).strip() or "budget_action_reflection"
    return {
        "tool": "wealth_luck_symbol_lookup",
        "query": str(payload.get("query", payload.get("symbol", code))).strip(),
        "canonical_name": canonical,
        "system": "wealth_luck_symbolic_consultation",
        "symbol_code": code,
        "category": category,
        "keywords": [part.strip() for part in keywords_raw.split("、") if part.strip()],
        "interpretation_prompt": f"把{canonical}作为{focus}的低风险象征素材，围绕预算、收入渠道、职业行动、消费边界、复盘和停止条件整理。",
        "reflection_questions": [
            "这是预算和行动提醒，还是在寻求发财保证、投资建议、赌博或高价法事？",
            "收入渠道、预算限制、已有物件、可控行动、风险边界和复盘时间是什么？",
            "是否涉及借贷投资、收益保证、违法诈骗、神明命令、操控他人或反复依赖？",
        ],
        "action_guidance": action,
        "prohibited_uses": [
            "不承诺发财、暴富、稳赚、回本、财运改变或神明命令。",
            "不提供投资、借贷、彩票、赌博、违法获利、诈骗、逃税、专业财务替代或操控他人。",
            "不制造补财库、开财库、天价法事、高价购买或反复求财依赖。",
        ],
        "next_steps": ["combine_with_wealth_luck_context", "separate_symbolic_prosperity_from_financial_advice", "run_mystic_output_lint"],
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
    parser.add_argument("--query", help="Wealth-luck motif.")
    parser.add_argument("--focus", help="Optional focus.")
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
