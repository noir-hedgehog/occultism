#!/usr/bin/env python3
"""Guard Lenormand card requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "lenormand_symbolic_reading": ("雷诺曼", "lenormand", "雷诺曼卡", "36张", "36 张", "骑士牌"),
    "spread_or_card_record": ("九宫格", "三张", "五张", "牌阵", "抽牌", "牌组"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用看合同", "只听牌", "全听牌"),
    "deterministic_fate": ("一定会", "必然", "注定", "命中注定", "最终答案", "唯一答案", "必须照做"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "收益"),
    "health_or_safety": ("怀孕", "生病", "吃药", "手术", "自杀", "自残", "危险", "报警"),
    "third_party_privacy": ("他心里", "她心里", "老板会不会", "真实想法", "内心想法", "心里怎么想", "对方真实想法", "偷偷看", "监视"),
    "coercion": ("让他回来", "让她回来", "操控", "控制", "复合咒", "诅咒别人"),
    "spirit_fear_claim": ("附身", "鬼", "邪灵", "诅咒", "中邪", "被害"),
    "repeated_dependency": ("一直抽", "反复抽", "抽到满意", "每天抽几十次", "停不下来"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "lenormand_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = {
        "professional_replacement",
        "deterministic_fate",
        "financial_claim",
        "health_or_safety",
        "third_party_privacy",
        "coercion",
        "spirit_fear_claim",
        "repeated_dependency",
    }
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "health_or_safety" in flags:
        return "雷诺曼不能替代医疗、法律、财务、安全或紧急判断；先处理现实支持，再把问题改成低风险反思。"
    if "financial_claim" in flags:
        return "不让雷诺曼决定投资、贷款、彩票或赌博；可改成梳理风险承受度和需要核查的信息。"
    if "third_party_privacy" in flags or "coercion" in flags:
        return "不使用雷诺曼读取第三方隐私或操控他人；可改成自己的边界、沟通选择和可控行动。"
    if "spirit_fear_claim" in flags:
        return "不确认附身、邪灵、诅咒或超自然伤害；可转成安全感、环境整理和可信任支持。"
    if "repeated_dependency" in flags:
        return "暂停反复抽到满意为止；把本轮牌作为一次记录，并设置停止追问条件。"
    if "deterministic_fate" in flags:
        return "把命运断言改写为选项澄清：雷诺曼只作象征提示，结论回到现实证据和本人价值排序。"
    return "可以把雷诺曼作为象征反思、问题排序和低风险行动整理，不作为事实证明或最终决定。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "lenormand_request_guard",
        "request_text": text,
        "system": "lenormand_divination",
        "reading_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_lenormand": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "雷诺曼只作为象征性自我反思和问题整理，不证明事实、不替代专业判断、不做最终决定。",
            "医疗、法律、财务、安全、紧急情况和第三方隐私/操控请求必须暂停雷诺曼流程。",
            "反复抽到满意、命运恐吓或超自然伤害确认，应转向现实标准和支持资源。",
        ],
        "clarifying_questions": [
            "用户是想学习雷诺曼文化、记录已有抽牌，还是做低风险象征反思？",
            "问题是否涉及医疗、法律、财务、安全、第三方隐私、操控或超自然恐惧？",
            "本轮是三张、五张、九宫格，还是用户已有外部抽牌结果？",
        ],
        "next_steps": [
            "record_lenormand_draw",
            "lookup_lenormand_symbols",
            "build_lenormand_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_lenormand_reading", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Lenormand request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_lenormand"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
