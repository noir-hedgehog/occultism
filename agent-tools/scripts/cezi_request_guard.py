#!/usr/bin/env python3
"""Guard Chinese character-divination requests before symbolic consultation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "character_divination_symbolic_consultation": ("测字", "拆字", "字占", "字测", "测一个字", "拆一个字", "character divination", "chinese character divination"),
    "character_record": ("写了", "抽到", "想到", "这个字", "字形", "偏旁", "部首", "笔画", "结构"),
    "cultural_learning": ("文化", "讲讲", "是什么意思", "学习", "来历", "传统"),
}

RISK_KEYWORDS = {
    "professional_replacement": ("不用医生", "不用律师", "不用报警", "不用吃药", "只看字", "全靠测字"),
    "financial_or_gambling": ("股票", "彩票", "赌博", "下注", "投资", "币圈", "贷款", "发财", "梭哈", "收益"),
    "medical_or_safety": ("治病", "治疗", "怀孕", "癌", "手术", "失眠", "焦虑", "抑郁", "安全事故"),
    "deterministic_fate": ("一定会", "必然", "注定", "百分百", "保证", "必成", "必失败", "必分手", "命定"),
    "third_party_privacy": ("他真实想法", "她真实想法", "老板真实想法", "前任现在", "前任是不是", "第三者", "偷窥"),
    "coercion_or_control": ("让他回来", "让她回来", "控制", "操控", "复合咒", "报复"),
    "spirit_fear_or_curse": ("附身", "撞邪", "恶灵", "鬼跟着", "被诅咒", "下咒", "蛊", "驱鬼", "驱邪"),
    "identity_or_lifespan_label": ("寿命", "短命", "命苦", "克夫", "克妻", "克父母", "天生坏", "人格缺陷", "低贱"),
    "minor_labeling": ("孩子命不好", "宝宝命不好", "小孩命苦", "孩子克", "宝宝克"),
    "repeated_dependency": ("反复测", "测到满意", "一直测", "停不下来", "不测不敢决定"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "character_divination_symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    return not bool(set(RISK_KEYWORDS).intersection(flags))


def reframe(flags: list[str]) -> str:
    if "professional_replacement" in flags or "medical_or_safety" in flags:
        return "测字不能替代医疗、法律、安全或心理健康支持；先处理现实专业支持，再把字形作为象征提醒。"
    if "financial_or_gambling" in flags:
        return "不使用测字决定投资、贷款、彩票、赌博或高风险财务行为；可改成风险清单和现实约束。"
    if "spirit_fear_or_curse" in flags:
        return "不通过测字确认附身、诅咒、撞邪或驱邪效果；可改成安抚、现实安全检查和低风险整理。"
    if "identity_or_lifespan_label" in flags or "minor_labeling" in flags:
        return "不把一个字用于判断寿命、命苦、人格优劣、亲属相克或儿童人生标签；可改成文化象征和现实支持。"
    if "deterministic_fate" in flags:
        return "不把字形拆解写成确定预言或命运证明；可改成可能性、现实证据和低风险下一步。"
    if "third_party_privacy" in flags or "coercion_or_control" in flags:
        return "不使用测字窥探、操控或强迫他人；可改成自己的边界、沟通和可控行动。"
    if "repeated_dependency" in flags:
        return "暂停反复测字直到满意的依赖模式；先固定问题、字例和现实验证步骤。"
    return "可以把测字/拆字作为汉字象征和问题整理工具，不作为事实证明、专业建议或结果保证。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "cezi_request_guard",
        "request_text": text,
        "system": "character_divination_symbolic_reflection",
        "consultation_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_cezi": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "测字/拆字只作为汉字象征、问题整理和低风险行动提醒，不证明事实、不保证结果。",
            "不替代医疗、法律、财务、安全、心理健康或紧急支持。",
            "不用于寿命判断、人格优劣、儿童标签、第三方窥探、操控、驱邪证明、确定预言或反复依赖。",
        ],
        "clarifying_questions": [
            "用户是想文化学习、记录已有字例，还是做低风险象征咨询？",
            "字从哪里来：用户写下、随机抽取、他人给出、梦中出现，还是 agent 经同意模拟？",
            "请求是否涉及专业替代、财务赌博、寿命/人格标签、儿童标签、灵异恐惧、第三方隐私、操控或反复依赖？",
        ],
        "next_steps": [
            "record_cezi_character",
            "lookup_cezi_symbols",
            "build_cezi_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_cezi_consultation", "reframe_to_real_world_support"],
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
    parser.add_argument("--text", help="Chinese character-divination request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_cezi"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
