#!/usr/bin/env python3
"""Guard wish, intention, manifestation, and low-risk prayer ritual requests."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "manifestation_symbolic_consultation": ("祈愿", "许愿", "愿望仪式", "显化", "心愿", "愿望清单", "意图设定", "manifestation", "manifest", "intention setting", "wish ritual"),
    "intention_planning": ("目标", "行动计划", "复盘", "找工作", "学习", "项目", "习惯", "关系边界", "整理"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "学习", "象征"),
}

RISK_KEYWORDS = {
    "guaranteed_result_or_fate": ("保证实现", "一定实现", "百分百", "必成", "立刻成真", "命中注定", "宇宙必须"),
    "professional_replacement": ("不用医生", "不用律师", "不用咨询师", "不用报警", "不用治疗", "不用吃药", "替代医生", "替代律师"),
    "financial_or_lottery": ("股票", "彩票", "中奖", "赌博", "投资", "币圈", "贷款", "暴富", "财富自由"),
    "medical_or_fertility": ("治病", "治疗", "癌", "怀孕", "求子", "生男孩", "生女孩", "失眠", "抑郁", "焦虑"),
    "third_party_coercion": ("让他回来", "让她回来", "让前任回来", "控制", "操控", "复合必成", "让他爱我", "让她爱我", "真实想法"),
    "curse_or_revenge": ("诅咒", "报复", "下咒", "惩罚", "让他倒霉", "让她倒霉"),
    "dangerous_ritual": ("放血", "血祭", "割手", "割手指", "喝灰", "喝符水", "密闭燃烧", "烧炭", "酒精点火"),
    "expensive_purchase_pressure": ("必须付费", "天价", "贷款买课", "9999", "越贵越灵", "大师套餐", "能量课"),
    "spirit_fact_claim": ("宇宙命令", "神明保证", "灵体保证", "祖先命令", "天使命令"),
    "repeated_dependency": ("每天确认", "反复显化", "停不下来", "不显化就害怕", "每件事都许愿"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "manifestation_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "dangerous_ritual" in flags:
        return "祈愿/显化不能包含放血、摄入、密闭燃烧、酒精点火或其他危险仪式；先停止危险做法。"
    if "professional_replacement" in flags or "medical_or_fertility" in flags:
        return "祈愿/显化不能替代医疗、心理健康、法律、报警或其他专业支持；可改成就医准备、求助计划或情绪记录。"
    if "financial_or_lottery" in flags:
        return "不把祈愿/显化用于股票、彩票、赌博、贷款或投资判断；可改成预算、学习和风险控制计划。"
    if "third_party_coercion" in flags or "curse_or_revenge" in flags:
        return "不通过祈愿/显化控制第三方、强迫复合、读取真实想法、报复或诅咒。"
    if "guaranteed_result_or_fate" in flags or "spirit_fact_claim" in flags:
        return "不承诺愿望必然实现，也不确认宇宙、神明、灵体或祖先命令；可改成现实行动和停止条件。"
    if "expensive_purchase_pressure" in flags:
        return "不制造付费压力或高价课程/物件依赖；优先使用零成本、可逆、低风险做法。"
    if "repeated_dependency" in flags:
        return "暂停反复许愿以寻求确定感；把显化改成一次记录、一个行动和一个复盘时间。"
    return "可以把祈愿、显化和意图设定作为文化象征、情绪整理和现实行动规划，不保证结果、不替代专业支持、不控制他人。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "manifestation_request_guard",
        "request_text": text,
        "system": "manifestation_symbolic_consultation",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_manifestation": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "祈愿/显化只作文化学习、意图整理和低风险行动规划，不保证愿望实现或命运结果。",
            "不替代医疗、法律、财务、心理健康、报警、求助或现实专业支持。",
            "不控制第三方、不诅咒报复、不制造高价购买压力、不鼓励危险仪式或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想学习祈愿/显化文化、记录一个愿望，还是把意图转成现实行动计划？",
            "愿望主题、现实约束、可控行动、复盘时间和停止条件是什么？",
            "是否涉及结果保证、专业替代、财务投机、医疗生育、第三方操控、危险仪式、付费压力或反复依赖？",
        ],
        "next_steps": [
            "record_manifestation_intention",
            "lookup_manifestation_symbols",
            "build_manifestation_reflection_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_manifestation_consultation", "reframe_to_grounded_action_or_real_world_support"],
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
    parser.add_argument("--text", help="Manifestation request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_manifestation"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
