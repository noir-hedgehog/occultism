#!/usr/bin/env python3
"""Guard zodiac, Chinese zodiac, and Tai Sui requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "zodiac_symbolic_consultation": ("生肖", "属相", "本命年", "太岁", "犯太岁", "冲太岁", "十二生肖", "zodiac"),
    "zodiac_record": ("出生年", "年份", "属什么", "流年", "今年", "明年", "关系", "合不合"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看生肖", "全靠生肖"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "破财", "暴富"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "肯定倒霉", "必有灾", "大灾", "血光"),
    "fear_taisui": ("犯太岁会死", "冲太岁会出事", "太岁害我", "太岁报复", "躲不过", "化解不了"),
    "relationship_discrimination": ("生肖不合不能结婚", "属相不合必须分手", "克夫", "克妻", "克父母", "克孩子"),
    "third_party_labeling": ("他属", "她属", "老板属", "孩子一定", "这个人一定", "对方一定"),
    "expensive_purchase_pressure": ("必须买", "越贵越灵", "贷款买", "天价", "大师化太岁", "不开光没用", "限量法物"),
    "repeated_dependency": ("每天查运势", "不查不敢出门", "反复算", "停不下来", "一直害怕"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "zodiac_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "生肖/太岁不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把生肖作为文化象征。"
    if "financial_claim" in flags:
        return "不把生肖或太岁写成投资、贷款、彩票或财富结果判断；可改成预算、风险和现实约束清单。"
    if "deterministic_fate" in flags or "fear_taisui" in flags:
        return "不确认犯太岁必有灾、血光、死亡或报复；可改成文化学习、风险预案和低风险提醒。"
    if "relationship_discrimination" in flags or "third_party_labeling" in flags:
        return "不按生肖给人贴命运、人品、婚恋或亲子标签；可改成沟通偏好、边界和现实相处观察。"
    if "expensive_purchase_pressure" in flags:
        return "不制造化太岁或开光购买压力；优先记录预算、已有物件和可撤回选择。"
    if "repeated_dependency" in flags:
        return "暂停反复查生肖运势或因不查而恐惧的依赖模式；设置使用频率和现实支持。"
    return "可以把生肖/太岁作为民俗文化、时间象征和低风险自我提醒，不作为命运证明或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "zodiac_request_guard",
        "request_text": text,
        "system": "zodiac_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_zodiac": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "生肖、属相、本命年和太岁只作为民俗文化、时间象征和低风险提醒，不证明命运或保证结果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
            "不输出灾祸恐吓、合婚歧视、第三方标签、高价化解压力或反复依赖流程。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录年份资料，还是做低风险象征咨询？",
            "涉及本人还是第三方；年份、生肖、关注主题和现实背景是什么？",
            "请求是否涉及灾祸恐吓、专业替代、关系歧视、高价化解或反复依赖？",
        ],
        "next_steps": [
            "record_zodiac_profile_and_context",
            "lookup_zodiac_or_taisui_symbols",
            "build_zodiac_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_zodiac_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Zodiac or Tai Sui request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_zodiac"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
