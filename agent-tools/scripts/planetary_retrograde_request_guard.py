#!/usr/bin/env python3
"""Guard planetary retrograde and astrology-weather requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "planetary_retrograde_symbolic_consultation": ("水逆", "行星逆行", "星象天气", "星象影响", "逆行周期", "mercury retrograde", "retrograde", "astrology weather"),
    "retrograde_review": ("复盘", "沟通", "备份", "延迟", "检查", "调整节奏", "review"),
    "astrology_culture_learning": ("文化", "学习", "讲讲", "是什么", "来源"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用咨询", "股票", "贷款", "投资", "彩票", "赌博", "辞职", "签合同", "手术", "用药", "离婚官司"),
    "deterministic_fate_or_blame": ("水逆害我", "都是水逆", "一定倒霉", "必然分手", "命中注定", "无法避免", "一定出事", "注定失败"),
    "relationship_or_third_party_control": ("让前任回来", "让他回头", "证明他爱我", "证明她爱我", "他真实想法", "她真实想法", "报复", "惩罚他"),
    "dangerous_ritual_or_purchase": ("血祭", "放血", "烧掉", "连夜开车去", "天价转运", "大师套餐", "买水晶阵", "越贵越准"),
    "mental_health_or_paranoia": ("被行星控制", "被监视", "不敢出门", "恐慌", "睡不着", "停不下来", "每天查星象"),
    "spirit_fact_claim": ("行星惩罚", "宇宙惩罚", "神明惩罚", "灵体干扰", "外星控制"),
}

SAFE_NEGATED_PHRASES = (
    "不怪水逆",
    "不都怪水逆",
    "不是水逆害我",
    "不当成命中注定",
    "不当成灾祸预言",
    "不每天查星象",
    "不会每天查星象",
    "不再每天查星象",
    "停止每天查星象",
)


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "planetary_retrograde_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    risk_text = text
    for phrase in SAFE_NEGATED_PHRASES:
        risk_text = risk_text.replace(phrase, "")
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(risk_text, keywords)]


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags:
        return "水逆/行星逆行不能替代医疗、法律、财务、职业或签约判断；先使用现实信息和专业意见。"
    if "deterministic_fate_or_blame" in flags:
        return "不把水逆写成必然倒霉、注定失败或外部归罪；可改成沟通、备份和复盘提醒。"
    if "relationship_or_third_party_control" in flags:
        return "不通过星象证明他人真实想法、操控关系结果、报复或惩罚他人。"
    if "dangerous_ritual_or_purchase" in flags:
        return "不提供危险仪式、连夜行动或高价转运购买建议；优先低成本、可逆、现实安全的做法。"
    if "mental_health_or_paranoia" in flags:
        return "如果星象检查带来恐慌、失眠、停不下来或被控制感，先暂停查询，做 grounding，并考虑可信任的人或专业支持。"
    if "spirit_fact_claim" in flags:
        return "不把行星逆行写成宇宙、神明、灵体或外星的惩罚与控制事实。"
    return "可以把水逆/行星逆行作为象征性的复盘、沟通检查、备份和节奏调整提醒。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = not flags
    return {
        "tool": "planetary_retrograde_request_guard",
        "request_text": text,
        "system": "planetary_retrograde_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_planetary_retrograde": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "水逆/行星逆行只作象征性复盘、沟通检查、备份和节奏调整提醒。",
            "不写成必然灾祸、命中注定、外部惩罚、关系读心或专业决策依据。",
            "不替代医疗、法律、财务、职业、心理健康或现实安全判断。",
            "不制造高价转运、危险仪式、反复查询或恐慌依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习星象文化、记录当前逆行背景，还是做低风险复盘计划？",
            "逆行主题、关注领域、现实事项、已知限制、可控行动、复盘时间和停止查询条件是什么？",
            "是否涉及专业替代、宿命归因、第三方读心/操控、危险仪式、高价转运或恐慌依赖？",
        ],
        "next_steps": [
            "record_planetary_retrograde_context",
            "lookup_planetary_retrograde_symbols",
            "build_planetary_retrograde_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_planetary_retrograde_consultation", "reframe_to_grounded_review_or_professional_support"],
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
    parser.add_argument("--text", help="Planetary retrograde request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_planetary_retrograde"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
