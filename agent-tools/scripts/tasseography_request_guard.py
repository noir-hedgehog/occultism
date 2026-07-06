#!/usr/bin/env python3
"""Guard tea-leaf and coffee-ground reading requests before consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "tasseography_symbolic_consultation": ("茶叶占卜", "茶渣占卜", "咖啡渣占卜", "杯底占卜", "茶占", "咖啡占卜", "咖啡渣", "茶叶形状", "茶渣", "杯底", "杯壁", "tasseography", "tea leaf reading", "coffee grounds"),
    "pattern_record": ("杯底", "茶叶形状", "咖啡渣形状", "残渣", "图案", "形状", "杯壁"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看杯底", "全靠茶叶"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "发财", "梭哈", "收益"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任现在", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复"),
    "repeated_dependency": ("反复看", "看到满意", "一直看", "停不下来", "不看不敢决定", "每天占"),
    "unsafe_ingestion": ("喝下残渣", "吃掉茶叶", "吞咖啡渣", "霉", "发霉", "不明液体"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "tasseography_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "茶叶/咖啡渣占卜不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把图案作为象征提醒。"
    if "financial_or_gambling" in flags:
        return "不使用杯底图案决定投资、贷款、彩票、赌博或高风险财务行为；可改成风险清单和现实约束。"
    if "unsafe_ingestion" in flags:
        return "不建议饮用、吞食或继续使用变质、不明来源的茶叶/咖啡残渣；先处理食品安全和清洁。"
    if "deterministic_fate" in flags:
        return "不把图案写成确定预言或命运证明；可改成可能性、现实证据和低风险下一步。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用杯底图案窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "repeated_dependency" in flags:
        return "暂停反复看图案直到满意的依赖模式；先固定问题、观察次数和现实验证步骤。"
    return "可以把茶叶/咖啡渣图案作为象征性反思工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "tasseography_request_guard",
        "request_text": text,
        "system": "tasseography_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_tasseography": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "茶叶/咖啡渣占卜只作为象征性反思、问题整理和低风险行动提醒，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
            "不用于赌博、投资决策、第三方窥探、操控、确定预言、反复依赖或不安全摄入。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有杯底图案，还是做低风险象征咨询？",
            "问题是否已经收束为一事一问；图案来自茶叶、咖啡渣、杯壁还是照片描述？",
            "请求是否涉及财务赌博、专业替代、第三方隐私、操控、反复依赖或食品安全？",
        ],
        "next_steps": [
            "record_cup_pattern",
            "lookup_tasseography_symbols",
            "build_tasseography_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_tasseography_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Tea-leaf or coffee-ground reading request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_tasseography"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
