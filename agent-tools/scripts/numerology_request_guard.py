#!/usr/bin/env python3
"""Guard numerology and number-symbol requests before interpretation."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


INTENT_KEYWORDS = {
    "number_symbol_reflection": ("数字能量", "数字象征", "数字占卜", "生命灵数", "灵数", "手机号", "车牌号", "门牌号", "幸运数字"),
    "number_selection": ("选号码", "选号", "号码比较", "手机号比较", "车牌比较"),
    "cultural_learning": ("来源", "文化", "讲讲", "是什么意思", "怎么理解"),
}

RISK_KEYWORDS = {
    "financial_claim": ("发财", "旺财", "股票", "彩票", "赌博", "投资", "贷款", "币圈", "收益"),
    "deterministic_fate": ("一定", "必然", "注定", "必发财", "必倒霉", "命不好", "改命"),
    "professional_replacement": ("不用医生", "不用律师", "不用看合同", "只看数字", "全听号码"),
    "privacy_sensitive_identifier": ("身份证", "银行卡", "账号", "密码", "验证码", "完整手机号"),
    "third_party_profiling": ("他是不是", "她是不是", "这个人人品", "老板", "同事", "前任", "筛人"),
    "minor_labeling": ("孩子命", "宝宝命", "小孩性格注定", "学生命不好"),
}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_intent(text: str) -> str:
    for intent, keywords in INTENT_KEYWORDS.items():
        if contains_any(text, keywords):
            return intent
    return "symbolic_reflection"


def risk_flags_for(text: str) -> list[str]:
    return [flag for flag, keywords in RISK_KEYWORDS.items() if contains_any(text, keywords)]


def can_continue(flags: list[str]) -> bool:
    blocking = {"financial_claim", "professional_replacement", "privacy_sensitive_identifier", "third_party_profiling"}
    return not bool(blocking.intersection(flags))


def reframe(flags: list[str]) -> str:
    if "privacy_sensitive_identifier" in flags:
        return "不要提供身份证、银行卡、验证码、密码或完整手机号；可改为只讨论尾号、脱敏片段或数字偏好。"
    if "financial_claim" in flags:
        return "不把数字当作发财、投资或彩票保证；可改为整理个人偏好、记忆度和现实使用成本。"
    if "professional_replacement" in flags:
        return "不让数字替代医疗、法律、合同或安全判断；可改为现实条件优先、数字象征辅助。"
    if "third_party_profiling" in flags:
        return "不通过号码判断第三方人品或真实想法；可改为匿名文化学习或自己的偏好选择。"
    if "deterministic_fate" in flags:
        return "把注定和改命改写为象征提醒、偏好排序和可控行动。"
    if "minor_labeling" in flags:
        return "不把数字贴成未成年人命运或性格标签；可讨论命名/号码的现实使用舒适度。"
    return "可以把数字作为文化象征、偏好整理和低风险选择辅助。"


def guard(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("request_text", payload.get("text", ""))).strip()
    if not text:
        raise ValueError("request_text or text is required")
    flags = risk_flags_for(text)
    allowed = can_continue(flags)
    return {
        "tool": "numerology_request_guard",
        "request_text": text,
        "system": "number_symbolism",
        "reading_intent": detect_intent(text),
        "risk_flags": flags,
        "can_continue_numerology": allowed,
        "reframed_question": reframe(flags),
        "required_boundaries": [
            "数字象征只能作为文化联想、偏好整理和低风险选择辅助，不保证财富、关系、健康或命运。",
            "不得收集身份证、银行卡、验证码、密码或完整手机号等敏感标识。",
            "不得用号码判断第三方人品、隐私、职业适配或命运好坏。",
        ],
        "clarifying_questions": [
            "用户想讨论的是数字含义、号码比较、生命灵数，还是文化学习？",
            "是否已对号码做脱敏，只保留尾号或非敏感片段？",
            "现实优先条件是什么：记忆度、读音、价格、可用性、隐私还是个人偏好？",
        ],
        "next_steps": [
            "record_number_material",
            "lookup_number_symbols",
            "build_numerology_interpretation_plan",
            "lint_final_output_with_mystic_output_lint",
        ] if allowed else ["pause_numerology_reading", "reframe_to_privacy_or_real_world_support"],
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
    parser.add_argument("--text", help="Numerology request text.")
    parser.add_argument("--json", help="JSON object input.")
    parser.add_argument("--file", help="Path to JSON input.")
    args = parser.parse_args()
    try:
        result = guard(load_payload(args))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["can_continue_numerology"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
