#!/usr/bin/env python3
"""Guard Western geomancy and shield-chart requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "western_geomancy_symbolic_consultation": ("西洋土占", "盾形占", "盾盘", "土占盘", "geomancy", "western geomancy", "shield chart", "geomantic figure", "geomantic chart"),
    "figure_record": ("四行点", "单点双点", "母亲图", "女儿图", "侄子图", "见证者", "裁判者", "母图", "daughter", "mother figure", "witness", "judge"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统", "体系"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看土占", "全靠盾盘", "替我决定"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "梭哈", "收益", "翻倍"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手", "永远"),
    "spirit_fear_or_curse": ("附身", "撞邪", "恶灵", "鬼跟着", "被诅咒", "下咒", "蛊", "驱鬼", "驱邪"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任真实想法", "前任现在", "前任是不是", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复"),
    "repeated_dependency": ("反复起盘", "起到满意", "一直起盘", "停不下来", "不占不敢决定", "每天占很多次"),
}

SAFE_NEGATED_RISK_PHRASES = (
    "不投资",
    "不赌博",
    "不贷款",
    "不预测",
    "不读心",
    "不操控",
    "不驱邪",
    "不反复起盘",
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
    return "western_geomancy_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = remove_safe_negations(text)
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "西洋土占不能替代医疗、法律、安全、心理健康或紧急支持；先处理现实专业支持，再把盘面作为象征提醒。"
    if "financial_or_gambling" in flags:
        return "不使用土占结果决定投资、贷款、彩票、赌博或高风险财务行为；可改成风险清单和现实约束。"
    if "deterministic_fate" in flags:
        return "不把盾形盘写成确定预言或命运证明；可改成可能性、现实证据和低风险下一步。"
    if "spirit_fear_or_curse" in flags:
        return "不确认附身、诅咒、恶灵或驱邪效果；可改成安抚、现实安全检查和低风险整理。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用西洋土占窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "repeated_dependency" in flags:
        return "暂停反复起盘直到满意的依赖模式；先固定问题、起盘次数、复盘时间和现实验证步骤。"
    return "可以把西洋土占和盾形盘作为象征性反思工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "western_geomancy_request_guard",
        "request_text": text,
        "system": "western_geomancy_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_western_geomancy": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "西洋土占、四行点和盾形盘只作为象征性反思、问题整理和低风险行动提醒，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康、紧急支持或当事人沟通。",
            "不用于投资赌博、第三方窥探、操控、确定预言、诅咒/驱邪证明或反复起盘依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有盾形盘，还是做低风险象征咨询？",
            "四个母亲图、女儿图、侄子图、见证者和裁判者是否已经固定；来源是用户提供、同意模拟还是外部应用？",
            "请求是否涉及专业替代、财务赌博、灵异恐惧、第三方隐私、操控、确定预言或反复依赖？",
        ],
        "next_steps": [
            "record_western_geomancy_chart",
            "lookup_western_geomancy_figures",
            "build_western_geomancy_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_western_geomancy_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Western geomancy or shield-chart request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_western_geomancy"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
