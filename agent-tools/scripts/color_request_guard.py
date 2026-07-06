#!/usr/bin/env python3
"""Guard five-elements color and lucky-color requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "color_symbolic_consultation": ("颜色", "开运色", "幸运色", "五行颜色", "穿搭", "配色", "色彩", "color", "lucky color"),
    "color_profile": ("今天穿", "明天穿", "办公室", "卧室", "桌面", "衣服", "饰品", "品牌色", "主色"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只靠颜色", "全靠颜色"),
    "medical_or_safety": ("治病", "治疗", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "financial_claim": ("股票", "彩票", "赌博", "投资", "币圈", "贷款", "发财", "破财", "暴富", "收益"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证转运", "必招财", "必避灾"),
    "appearance_or_identity_label": ("丑", "显丑", "显胖", "土气", "克人", "低等", "这种人不配", "看起来命苦"),
    "expensive_purchase_pressure": ("必须买", "越贵越灵", "贷款买", "天价", "大师配色", "不开运没用", "限量色"),
    "repeated_dependency": ("每天不查不敢出门", "不穿就害怕", "反复查", "停不下来", "颜色不对就完了"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "color_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "五行颜色不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把颜色作为低风险提醒。"
    if "financial_claim" in flags or "deterministic_fate" in flags:
        return "不把颜色写成保证发财、转运、避灾或投资结果的工具；可改成情绪提示、行动提醒和现实约束。"
    if "appearance_or_identity_label" in flags:
        return "不按颜色评价外貌、身份、人品或价值；可改成个人偏好、场景适配和舒适度。"
    if "expensive_purchase_pressure" in flags:
        return "不制造高价购买或必须换装压力；优先使用已有衣物、低成本配件或可撤回调整。"
    if "repeated_dependency" in flags:
        return "暂停因颜色选择产生强烈恐惧或依赖的流程；设置频率边界并回到现实支持。"
    return "可以把五行颜色作为文化象征、情绪锚点、空间秩序或低风险行动提醒，不作为命运证明或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "color_request_guard",
        "request_text": text,
        "system": "color_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_color": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "五行颜色和开运色只作为文化象征、情绪锚点、空间秩序或低风险行动提醒，不证明命运或保证结果。",
            "不替代医疗、法律、财务、安全、心理健康、形象咨询或紧急支持。",
            "不输出财富保证、灾祸恐吓、外貌贬低、身份标签、高价购买压力或反复依赖流程。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、穿搭提醒、空间配色、品牌配色，还是低风险象征咨询？",
            "场景、已有颜色/物件、偏好、禁忌色、预算和现实约束是什么？",
            "请求是否涉及专业替代、财富保证、外貌评价、高价购买或反复依赖？",
        ],
        "next_steps": [
            "record_color_context",
            "lookup_color_symbols",
            "build_color_palette_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_color_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Color or lucky-color request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_color"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
