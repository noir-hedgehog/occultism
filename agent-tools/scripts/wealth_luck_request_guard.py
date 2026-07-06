#!/usr/bin/env python3
"""Guard wealth-luck, prosperity, and money-ritual requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "wealth_luck_symbolic_consultation": ("招财", "财运", "求财", "旺财", "开财库", "补财库", "财库", "财神", "貔貅", "金蟾", "聚宝盆", "prosperity", "wealth luck", "abundance"),
    "budget_action_reflection": ("预算", "收入", "现金流", "记账", "工作机会", "客户", "业绩", "副业", "省钱"),
    "symbolic_reminder_use": ("提醒物", "低风险", "不投资", "不赌博", "不买法事", "不保证发财"),
}

RISK_KEYWORDS = {
    "financial_professional_replacement": ("股票", "基金", "期货", "币圈", "比特币", "彩票", "赌博", "博彩", "贷款", "借贷", "信用卡套现", "梭哈", "投资建议", "买哪只"),
    "guaranteed_wealth_claim": ("一定发财", "保证发财", "稳赚", "暴富", "财运暴涨", "必赚", "百分百回本", "翻倍", "躺赚"),
    "debt_or_desperation": ("负债", "还不上", "债务", "欠债", "没钱吃饭", "走投无路", "破产", "催收"),
    "expensive_ritual_pressure": ("天价法事", "补财库套餐", "开财库套餐", "必须请大师", "必须买", "越贵越灵", "贷款做法事"),
    "fraud_or_illegal_action": ("骗", "诈骗", "骗客户", "偷", "逃税", "洗钱", "内幕消息", "灰产", "传销"),
    "spirit_command_or_fear": ("财神命令", "神明保证", "祖先说会发财", "不做就破财", "被夺财运", "财库被封"),
    "coercion_or_third_party": ("让客户必须买", "操控老板", "让竞争对手倒闭", "诅咒同行", "抢别人财运"),
    "repeated_dependency": ("每天求财", "反复补财库", "停不下来", "不做就害怕", "每单都问财运", "一直查财运"),
}

SAFE_NEGATED_PHRASES = (
    "不投资",
    "不赌博",
    "不买彩票",
    "不买法事",
    "不保证发财",
    "不借贷",
    "不贷款",
    "不操控别人",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "wealth_luck_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "financial_professional_replacement" in flags:
        return "不提供投资、借贷、彩票、赌博或具体金融决策建议；可改成预算、收入渠道和风险承受边界整理。"
    if "guaranteed_wealth_claim" in flags:
        return "不承诺发财、稳赚、暴富或回本；招财语言只能作为行动提醒和资源整理象征。"
    if "debt_or_desperation" in flags:
        return "涉及债务、破产、催收或基本生活压力时，优先现实财务/法律/社会支持，不用仪式替代。"
    if "expensive_ritual_pressure" in flags:
        return "不制造补财库、开财库、天价法事或大师套餐压力；优先低成本、可撤回的提醒物和预算动作。"
    if "fraud_or_illegal_action" in flags:
        return "不协助诈骗、逃税、洗钱、偷窃、内幕交易、传销或任何违法不诚实行为。"
    if "spirit_command_or_fear" in flags:
        return "不确认财神、神明、祖先命令或财库被封事实；可改成资源盘点和现实计划。"
    if "coercion_or_third_party" in flags:
        return "不把招财用于操控客户、老板、竞争对手或抢夺他人资源。"
    if "repeated_dependency" in flags:
        return "如果反复求财、查财运或补财库已经加重焦虑，先设置固定复盘频率和停止条件。"
    return "可以把招财/财运/财神/财库象征作为预算、收入渠道、职业行动、消费边界和复盘提醒。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "wealth_luck_request_guard",
        "request_text": text,
        "system": "wealth_luck_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_wealth_luck": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "招财、财运、财库、财神和求财物件只作预算、收入渠道、职业行动、消费边界和复盘提醒。",
            "不承诺发财、暴富、稳赚、回本、财运改变或财神/祖先/神明命令。",
            "不提供投资、借贷、彩票、赌博、违法获利、诈骗、逃税、专业财务替代或操控他人。",
            "不制造补财库、开财库、天价法事、高价购买或反复求财依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、已有招财物件解释，还是把求财愿望转成预算和行动计划？",
            "现实目标、收入渠道、预算限制、已有物件、可控行动、复盘时间和停止条件是什么？",
            "是否涉及投资赌博借贷、收益保证、债务压力、违法诈骗、高价法事、神明命令、操控他人或反复依赖？",
        ],
        "next_steps": [
            "record_wealth_luck_context",
            "lookup_wealth_luck_symbols",
            "build_wealth_luck_action_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_wealth_luck_consultation", "reframe_to_budget_action_or_professional_support"],
    }


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.json:
        return json.loads(args.json)
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return json.load(f)
    if args.text:
        return {"request_text": args.text}
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return {"request_text": raw}
    raise ValueError("Provide --text, --json, --file, or stdin input")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", help="Wealth-luck request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_wealth_luck"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
