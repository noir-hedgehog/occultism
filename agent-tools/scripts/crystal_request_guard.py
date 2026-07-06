#!/usr/bin/env python3
"""Guard crystal and energy-stone requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "crystal_symbolic_consultation": ("水晶", "能量石", "晶石", "crystal", "crystals", "quartz", "amethyst", "rose quartz"),
    "crystal_item_record": ("手串", "吊坠", "摆件", "随身", "佩戴", "净化", "消磁", "摆放", "书桌", "床头"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用看医生", "不用律师", "不用报警", "不用吃药", "只靠水晶", "全靠水晶"),
    "medical_healing_claim": ("治病", "治疗", "癌", "怀孕", "失眠不用看", "焦虑不用看", "抑郁不用看", "药", "手术"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "收益", "暴富"),
    "deterministic_fate": ("一定会", "必然", "注定", "命中注定", "保证转运", "保证复合", "必招财"),
    "ingestion_or_body_harm": ("水晶水", "泡水喝", "喝下去", "吞", "磨粉", "入药", "塞进", "贴伤口"),
    "third_party_privacy_or_coercion": ("让他回来", "让她回来", "控制", "操控", "复合咒", "他心里", "她心里", "真实想法"),
    "spirit_fear_claim": ("附身", "鬼", "邪灵", "诅咒", "中邪", "挡灾", "替我挡灾", "被害"),
    "expensive_purchase_pressure": ("必须买", "越贵越灵", "贷款买", "花光", "天价", "大师开光", "不开光没用"),
    "repeated_dependency": ("一直买", "不停买", "买到安心", "停不下来", "每天净化几十次", "反复确认"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "crystal_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = {
        "professional_replacement",
        "medical_healing_claim",
        "financial_claim",
        "deterministic_fate",
        "ingestion_or_body_harm",
        "third_party_privacy_or_coercion",
        "spirit_fear_claim",
        "expensive_purchase_pressure",
        "repeated_dependency",
    }
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_healing_claim" in flags:
        return "水晶不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把水晶改成低风险安定物或象征提醒。"
    if "ingestion_or_body_harm" in flags:
        return "不建议饮用、吞服、磨粉、贴伤口或把水晶用于身体侵入式做法；可改成外部摆放、审美或提醒用途。"
    if "financial_claim" in flags or "deterministic_fate" in flags:
        return "不把水晶写成保证发财、转运、复合或改变命运的工具；可改成价值排序、提醒物和现实行动清单。"
    if "third_party_privacy_or_coercion" in flags:
        return "不使用水晶操控他人或读取第三方隐私；可改成自己的边界、沟通选择和低风险行动。"
    if "spirit_fear_claim" in flags:
        return "不确认附身、诅咒、邪灵或挡灾证明；可转成安全感、环境整理和现实支持。"
    if "expensive_purchase_pressure" in flags:
        return "不制造高价购买压力；优先使用已有物件、低成本替代和可撤回选择。"
    if "repeated_dependency" in flags:
        return "暂停反复购买或反复净化以寻求确定感；设置使用频率和停止条件。"
    return "可以把水晶作为审美、象征提醒、仪式感和自我照顾道具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "crystal_request_guard",
        "request_text": text,
        "system": "crystal_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_crystal": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "水晶和能量石只作为象征、审美、提醒物和低风险仪式感辅助，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
            "不鼓励摄入、磨粉、贴伤口、身体侵入式使用、高价购买压力或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习水晶文化、记录已有物件，还是做低风险象征咨询？",
            "已有或考虑的水晶名称、颜色、形态、来源和使用场景是什么？",
            "问题是否涉及治病、招财保证、驱邪恐惧、操控他人、高价购买或反复依赖？",
        ],
        "next_steps": [
            "record_crystal_items_and_context",
            "lookup_crystal_symbols",
            "build_crystal_use_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_crystal_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Crystal request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_crystal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
