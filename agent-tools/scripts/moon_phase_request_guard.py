#!/usr/bin/env python3
"""Guard moon-phase, lunar-cycle, and manifestation requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "moon_phase_symbolic_consultation": ("月相", "月亮周期", "新月", "满月", "上弦月", "下弦月", "月食", "蓝月", "超级月亮", "月亮仪式", "新月许愿", "满月释放", "moon phase", "new moon", "full moon", "lunar"),
    "cycle_record": ("周期", "意图", "愿望", "释放", "复盘", "计划", "日记", "记录"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用心理咨询", "不用吃药", "不用律师", "不用报警", "只靠月亮", "全靠月相"),
    "medical_or_fertility": ("治病", "治疗", "诊断", "焦虑", "抑郁", "失眠", "幻听", "幻视", "怀孕", "备孕", "生男孩", "生女孩", "月经病", "内分泌", "药", "手术"),
    "dangerous_ritual": ("烧纸", "烧照片", "烧头发", "血", "放血", "酒精点火", "密闭燃烧", "通宵不睡", "禁食三天", "跳河", "爬楼顶"),
    "guaranteed_manifestation": ("一定显化", "必定实现", "百分百显化", "百分百成真", "马上复合", "必发财", "必中", " guaranteed", "100%"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "梭哈", "暴富"),
    "third_party_privacy_or_coercion": ("让他回来", "让她回来", "控制", "操控", "斩断第三者", "报复", "诅咒", "他心里", "她心里"),
    "expensive_course_pressure": ("必须付费", "必须买课", "天价", "越贵越灵", "贷款买课", "大师带做", "付费仪式"),
    "repeated_dependency": ("每天许愿", "每天看月相才敢", "不敢做决定", "查到确定为止", "停不下来", "每晚仪式"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "moon_phase_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_fertility" in flags:
        return "月相和月亮周期不能替代医疗、心理健康、生育、药物、法律或安全支持。"
    if "dangerous_ritual" in flags:
        return "不提供明火、血液、禁食、熬夜或危险地点仪式；可改成书写、整理和安全的低成本提醒。"
    if "guaranteed_manifestation" in flags:
        return "不保证显化、复合、发财或愿望成真；可改成意图澄清、现实行动和复盘。"
    if "financial_or_gambling" in flags:
        return "不把月相用于投资、彩票、赌博、贷款或暴富判断；财务决策必须回到现实信息。"
    if "third_party_privacy_or_coercion" in flags:
        return "不读取第三方真实想法，也不帮助操控、诅咒或强迫关系结果；可改成自己的边界和沟通。"
    if "expensive_course_pressure" in flags:
        return "不制造付费仪式、买课或大师带做压力；优先免费、可停止、可复盘的行动。"
    if "repeated_dependency" in flags:
        return "暂停反复许愿或查月相以寻求确定感；先固定频率并把问题转成当下行动。"
    return "可以把月相作为周期隐喻、意图整理和低风险复盘工具，不作为天文权威、结果保证或专业建议。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "moon_phase_request_guard",
        "request_text": text,
        "system": "moon_phase_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_moon_phase": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "月相、月亮周期和新月/满月仪式只作周期隐喻、文化学习、意图整理和低风险复盘，不保证显化或预测结果。",
            "不替代医疗、心理健康、生育、法律、财务、安全、紧急支持或现实沟通。",
            "不输出危险仪式、明火步骤、血液/禁食/熬夜要求、第三方操控、诅咒、付费仪式必要性或反复依赖诱导。",
        ],
        "clarifying_questions": [
            "用户是想学习月相文化、记录当前周期，还是做低风险意图/复盘？",
            "月相来源、日期/时间、关注主题、已有现实约束和可执行行动是什么？",
            "是否涉及医疗/生育/心理健康、危险仪式、关系操控、财务赌博、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_moon_phase_context",
            "lookup_moon_phase_symbols",
            "build_moon_phase_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_moon_phase_consultation", "reframe_to_real_world_support_or_safe_reflection"],
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
    parser.add_argument("--text", help="Moon-phase or lunar-cycle request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_moon_phase"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
