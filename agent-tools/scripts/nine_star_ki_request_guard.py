#!/usr/bin/env python3
"""Guard Nine Star Ki and nine-palace star requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "nine_star_ki_symbolic_consultation": ("九星气学", "九宫命星", "本命星", "月命星", "年命星", "九星命理", "九星流年", "九星方位", "nine star ki", "nine star astrology"),
    "star_profile": ("一白水星", "二黑土星", "三碧木星", "四绿木星", "五黄土星", "六白金星", "七赤金星", "八白土星", "九紫火星", "一白", "二黑", "三碧", "四绿", "五黄", "六白", "七赤", "八白", "九紫"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统", "体系"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "全靠九星", "替我决定"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故", "急诊"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "梭哈", "收益", "翻倍"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手", "永远", "今年必倒霉"),
    "direction_fear_or_costly_cure": ("五黄煞必出事", "这个方位会死人", "不能出门", "高价化解", "买法器", "做法事", "破灾"),
    "relationship_label_or_discrimination": ("克夫", "克妻", "旺夫", "旺妻", "天生不合", "不能结婚", "命不好", "筛掉"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任真实想法", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复"),
    "repeated_dependency": ("反复算", "算到满意", "一直算", "停不下来", "不算不敢决定", "每天看九星"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不投资",
    "不赌博",
    "不贷款",
    "不预测",
    "不读心",
    "不操控",
    "不做法事",
    "不高价化解",
    "不反复算",
    "不替代医生",
    "不替代医疗",
    "不替代心理咨询",
    "只整理现实下一步",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def remove_safe_negations(text: str) -> str:
    cleaned = text
    for phrase in SAFE_NEGATED_RISK_PHRASES:
        cleaned = cleaned.replace(phrase, "")
    return cleaned


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "nine_star_ki_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "九星气学不能替代医疗、法律、安全、心理健康或紧急支持；先处理现实专业支持，再把星象作为象征提醒。"
    if "financial_or_gambling" in flags:
        return "不使用九星气学决定投资、贷款、彩票、赌博或高风险财务行为；可改成预算、风险清单和现实约束。"
    if "deterministic_fate" in flags:
        return "不把本命星、年星或方位写成确定命运；可改成可能性、现实证据和低风险下一步。"
    if "direction_fear_or_costly_cure" in flags:
        return "不制造方位恐吓或高价化解压力；可改成低成本、可撤回的空间整理和行动复盘。"
    if "relationship_label_or_discrimination" in flags:
        return "不使用九星给人贴关系优劣、克制或筛选标签；可改成沟通边界和现实相处证据。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用九星窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "repeated_dependency" in flags:
        return "暂停反复计算直到满意的依赖模式；先固定问题、复盘时间和现实验证步骤。"
    return "可以把九星气学作为象征性反思工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "nine_star_ki_request_guard",
        "request_text": text,
        "system": "nine_star_ki_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_nine_star_ki": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "九星气学、本命星、年星和方位只作为象征性反思、问题整理和低风险行动提醒，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康、紧急支持、搬迁决策或当事人沟通。",
            "不用于投资赌博、关系贴标签、第三方窥探、操控、确定预言、方位恐吓、高价化解或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已知命星/年星，还是做低风险象征咨询？",
            "出生年份、节气边界、使用体系、本命星、月命星、年星、关注主题和复盘时间是否清楚？",
            "请求是否涉及专业替代、财务赌博、关系歧视、方位恐吓、高价化解、第三方隐私、操控、确定预言或反复依赖？",
        ],
        "next_steps": [
            "record_nine_star_ki_profile",
            "lookup_nine_star_ki_symbols",
            "build_nine_star_ki_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_nine_star_ki_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Nine Star Ki or nine-palace star request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_nine_star_ki"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
