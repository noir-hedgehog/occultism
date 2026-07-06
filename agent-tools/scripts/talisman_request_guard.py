#!/usr/bin/env python3
"""Guard talisman, charm, and fu-lu requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "talisman_symbolic_consultation": ("护符", "符箓", "符咒", "灵符", "平安符", "amulet", "talisman", "charm"),
    "talisman_record": ("来源", "寺庙", "道观", "佩戴", "随身", "收纳", "摆放", "保存", "开光"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "dangerous_ritual": ("烧符", "焚符", "符灰", "喝符水", "吞符", "血", "放血", "刀", "密闭燃烧"),
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只靠符", "全靠符"),
    "medical_claim": ("治病", "治疗", "怀孕", "癌", "手术", "失眠不用看", "焦虑不用看", "抑郁不用看"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "暴富", "收益"),
    "deterministic_fate": ("一定会", "必然", "注定", "保证转运", "必挡灾", "必灵", "百分百"),
    "curse_or_coercion": ("诅咒", "下咒", "让他回来", "让她回来", "控制", "操控", "复合咒", "害他"),
    "spirit_fear_claim": ("附身", "鬼", "邪灵", "中邪", "被害", "被诅咒", "挡灾证明", "替我挡灾"),
    "expensive_purchase_pressure": ("必须买", "越贵越灵", "贷款买", "天价", "大师开光", "不开光没用", "限量法物"),
    "repeated_dependency": ("一直求", "反复求", "求到安心", "停不下来", "每天换符", "符不离身就怕"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "talisman_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = set(RISK_KEYWORDS)
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if "dangerous_ritual" in flags:
        return "不提供烧符、喝符水、吞符、放血、密闭燃烧或其他危险做法；可改成文化学习、来源记录和低风险保存方式。"
    if "professional_replacement" in flags or "medical_claim" in flags:
        return "护符/符箓不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把符物作为象征提醒物。"
    if "curse_or_coercion" in flags:
        return "不协助诅咒、报复、操控或强迫他人；可改成自己的边界、情绪安定和可控行动。"
    if "financial_claim" in flags or "deterministic_fate" in flags:
        return "不把护符写成保证发财、转运、挡灾或改变命运的工具；可改成价值排序、提醒物和现实行动清单。"
    if "spirit_fear_claim" in flags:
        return "不确认附身、邪灵、中邪、被诅咒或挡灾证明；可转成安全感、环境整理和现实支持。"
    if "expensive_purchase_pressure" in flags:
        return "不制造高价购买或开光压力；优先记录来源、预算、已有物件和可撤回选择。"
    if "repeated_dependency" in flags:
        return "暂停反复求符或离符即恐惧的依赖模式；设置使用边界和现实支持。"
    return "可以把护符/符箓作为文化对象、象征提醒物或低风险安心物，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "talisman_request_guard",
        "request_text": text,
        "system": "talisman_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_talisman": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "护符、符箓和符咒只作为文化对象、象征提醒物或低风险安心物，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
            "不提供烧符、喝符水、吞符、放血、诅咒、操控、高价购买压力或反复依赖流程。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有护符，还是做低风险象征咨询？",
            "护符/符箓的来源、名称、文字/图案、使用场景和预算/已有物件说明是什么？",
            "请求是否涉及危险仪式、专业替代、诅咒操控、超自然恐惧、高价购买或反复依赖？",
        ],
        "next_steps": [
            "record_talisman_source_and_context",
            "lookup_talisman_symbols",
            "build_talisman_use_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_talisman_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Talisman request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_talisman"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
