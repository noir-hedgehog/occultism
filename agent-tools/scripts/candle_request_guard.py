#!/usr/bin/env python3
"""Guard candle flame and wax-symbol reading requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "candle_symbolic_consultation": ("蜡烛占卜", "蜡泪占卜", "火焰占卜", "烛火占卜", "蜡烛火焰", "蜡泪", "烛泪", "candle reading", "ceromancy", "candle wax reading"),
    "observation_record": ("火焰", "烛火", "蜡泪", "蜡烛形状", "蜡油", "烟", "熄灭"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "active_fire_instruction": ("怎么点", "点几根", "烧多久", "通宵点", "无人看管", "睡觉时点", "床边点", "窗帘旁", "纸堆旁"),
    "dangerous_ritual": ("密闭燃烧", "密闭房间点", "烧纸", "烧符", "酒精", "汽油", "放血", "血祭", "头发烧掉"),
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看蜡烛", "全靠烛火"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "发财", "梭哈", "收益"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手"),
    "spirit_fear_claim": ("有鬼", "中邪", "附身", "被诅咒", "邪灵", "驱鬼", "驱邪保证"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任现在", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复", "诅咒"),
    "repeated_dependency": ("反复点", "点到满意", "一直点", "停不下来", "不点不敢决定"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "candle_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "active_fire_instruction" in flags or "dangerous_ritual" in flags:
        return "不提供点火、燃烧、烧纸、烧符、放血或密闭燃烧步骤；可改为记录已经安全结束后的观察，或使用无火替代反思。"
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "蜡烛火焰/蜡泪象征不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持。"
    if "financial_or_gambling" in flags:
        return "不使用蜡烛或蜡泪决定投资、贷款、彩票、赌博或高风险财务行为；可改成风险清单和现实约束。"
    if "spirit_fear_claim" in flags:
        return "不确认鬼神、诅咒或驱邪效果；可转为安抚、空间整理和现实安全检查。"
    if "deterministic_fate" in flags:
        return "不把火焰或蜡泪写成确定预言或命运证明；可改成可能性、现实证据和低风险下一步。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用蜡烛窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "repeated_dependency" in flags:
        return "暂停反复点蜡烛直到满意的依赖模式；先固定问题、观察来源和现实验证步骤。"
    return "可以把已安全完成的蜡烛火焰/蜡泪观察作为象征性反思，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "candle_request_guard",
        "request_text": text,
        "system": "candle_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_candle": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "只处理已经安全结束或无需点火的观察记录；不提供点火、燃烧、烧纸、烧符、放血或密闭燃烧步骤。",
            "蜡烛火焰/蜡泪只作为象征反思，不证明事实、不保证结果、不确认鬼神或驱邪效果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有观察，还是做低风险象征咨询？",
            "观察是否已经安全结束；是否涉及明火、密闭燃烧、烧纸、烧符、酒精、无人看管或危险环境？",
            "请求是否涉及财务赌博、专业替代、第三方隐私、操控、鬼神恐惧或反复依赖？",
        ],
        "next_steps": [
            "record_candle_observation",
            "lookup_candle_symbols",
            "build_candle_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_candle_consultation", "reframe_to_fire_safety_or_real_world_support"],
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
    parser.add_argument("--text", help="Candle flame or wax-symbol request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_candle"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
