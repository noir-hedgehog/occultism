#!/usr/bin/env python3
"""Guard flower-language and plant-symbolism requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "flower_symbolic_consultation": ("花语", "花占", "花卜", "花签", "花牌", "植物象征", "送花", "花束", "flower language", "floriography", "flower divination"),
    "flower_item_record": ("玫瑰", "百合", "向日葵", "薰衣草", "莲花", "梅花", "兰花", "菊花", "植物", "盆栽", "花材"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只靠花", "全靠花语"),
    "medical_healing_claim": ("治病", "治疗", "治焦虑", "治抑郁", "治失眠", "怀孕", "癌", "失眠不用看", "焦虑不用看", "抑郁不用看", "药", "手术"),
    "allergy_or_toxicity": ("花粉过敏", "会不会过敏", "判断过敏", "有毒", "猫能吃", "狗能吃", "宠物吃", "误食", "入口", "泡水喝", "入药"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "发财", "收益", "暴富"),
    "deterministic_fate": ("一定会", "必然", "注定", "保证复合", "必招桃花", "必招财", "保证转运"),
    "third_party_privacy_or_coercion": ("让他回来", "让她回来", "控制", "操控", "复合咒", "他心里", "她心里", "真实想法"),
    "spirit_fear_claim": ("附身", "鬼", "邪灵", "诅咒", "中邪", "挡灾", "驱邪", "被害"),
    "expensive_purchase_pressure": ("必须买", "越贵越灵", "贷款买", "花光", "天价", "大师开光", "不开光没用"),
    "repeated_dependency": ("一直买", "不停买", "买到安心", "反复抽花", "抽到满意", "停不下来"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "flower_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_healing_claim" in flags:
        return "花语/植物象征不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把花材作为象征提醒。"
    if "allergy_or_toxicity" in flags:
        return "不使用花语判断过敏、毒性、宠物安全、摄入或药用；先查可靠安全来源或咨询专业人士。"
    if "financial_or_gambling" in flags or "deterministic_fate" in flags:
        return "不把花语写成保证发财、复合、转运或投资决策；可改成偏好、关系表达和现实行动清单。"
    if "third_party_privacy_or_coercion" in flags:
        return "不使用花语操控他人或读取第三方隐私；可改成自己的表达、边界和沟通选择。"
    if "spirit_fear_claim" in flags:
        return "不确认附身、诅咒、邪灵、挡灾或驱邪效果；可转成安全感、环境整理和现实支持。"
    if "expensive_purchase_pressure" in flags:
        return "不制造高价购买压力；优先使用已有花材、低成本替代和可撤回选择。"
    if "repeated_dependency" in flags:
        return "暂停反复抽花或反复购买以寻求确定感；先固定问题、次数和现实验证步骤。"
    return "可以把花语/植物象征作为审美、表达、提醒物和低风险反思工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "flower_request_guard",
        "request_text": text,
        "system": "flower_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_flower": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "花语、花占和植物象征只作为文化、审美、表达和低风险反思，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康、宠物安全或紧急支持。",
            "不鼓励摄入、药用、过敏/毒性判断、高价购买压力、第三方窥探、操控、驱邪证明或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习花语文化、记录已有花材，还是做低风险象征咨询？",
            "已有或考虑的花材、颜色、数量、场景、对象、预算和安全约束是什么？",
            "问题是否涉及医疗疗愈、过敏/毒性/宠物安全、招财/复合保证、驱邪恐惧、高价购买或反复依赖？",
        ],
        "next_steps": [
            "record_flower_items_and_context",
            "lookup_flower_symbols",
            "build_flower_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_flower_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Flower-language or plant-symbolism request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_flower"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
